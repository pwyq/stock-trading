import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone

import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator

from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
from sklearn.ensemble import GradientBoostingClassifier

# ---- Sentiment (FinBERT) ----
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

def load_news(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # normalize expected cols
    if "published_at" not in df.columns or "headline" not in df.columns:
        raise ValueError("news.csv must have columns: published_at, headline")
    # parse datetime; keep date in UTC for simplicity and convert to date
    df["published_at"] = pd.to_datetime(df["published_at"], utc=True, errors="coerce")
    df = df.dropna(subset=["published_at", "headline"])
    df["date"] = df["published_at"].dt.date
    return df[["date", "headline"]]

def build_finbert_pipeline():
    model_name = "ProsusAI/finbert"
    tok = AutoTokenizer.from_pretrained(model_name)
    mdl = AutoModelForSequenceClassification.from_pretrained(model_name)
    return TextClassificationPipeline(model=mdl, tokenizer=tok, return_all_scores=True, truncation=True)

def score_sentiment(df_news: pd.DataFrame, pipe: TextClassificationPipeline, batch_size: int = 32) -> pd.DataFrame:
    texts = df_news["headline"].astype(str).tolist()
    scores = []
    # batch for speed
    for i in range(0, len(texts), batch_size):
        out = pipe(texts[i:i+batch_size])
        for row in out:
            # FinBERT labels: ['positive','negative','neutral']
            lab2p = {d["label"].lower(): d["score"] for d in row}
            # sentiment score: positive - negative (neutral ignored)
            s = lab2p.get("positive", 0.0) - lab2p.get("negative", 0.0)
            scores.append(s)
    df_news = df_news.copy()
    df_news["sent_score"] = scores
    # aggregate to daily features
    daily = df_news.groupby("date").agg(
        sent_mean=("sent_score", "mean"),
        sent_median=("sent_score", "median"),
        sent_std=("sent_score", "std"),
        sent_n=("sent_score", "count")
    ).fillna(0.0)
    # rolling sentiment momentum
    daily["sent_3d_ma"] = daily["sent_mean"].rolling(3, min_periods=1).mean()
    daily["sent_5d_ma"] = daily["sent_mean"].rolling(5, min_periods=1).mean()
    daily["sent_mom"] = daily["sent_3d_ma"] - daily["sent_5d_ma"]
    return daily

def load_prices(ticker: str, start: str = "2019-01-01") -> pd.DataFrame:
    df = yf.download(ticker, start=start, auto_adjust=True, progress=False)
    if df.empty:
        raise RuntimeError(f"No price data for {ticker}")
    df = df.rename_axis("Date").reset_index()
    df["date"] = df["Date"].dt.date
    # technical features
    df["ret_1d"] = df["Close"].pct_change()
    df["ret_5d"] = df["Close"].pct_change(5)
    df["vol_chg"] = df["Volume"].pct_change().replace([np.inf, -np.inf], 0).fillna(0)

    rsi = RSIIndicator(close=df["Close"], window=14)
    df["rsi_14"] = rsi.rsi()

    macd = MACD(close=df["Close"], window_slow=26, window_fast=12, window_sign=9)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    sma_5 = SMAIndicator(close=df["Close"], window=5)
    sma_20 = SMAIndicator(close=df["Close"], window=20)
    df["sma_5"] = sma_5.sma_indicator()
    df["sma_20"] = sma_20.sma_indicator()
    df["sma_spread"] = (df["sma_5"] - df["sma_20"]) / df["sma_20"]

    # label: next-day up/down (classification)
    df["close_next"] = df["Close"].shift(-1)
    df["y_up"] = (df["close_next"] > df["Close"]).astype(int)
    return df

def assemble_dataset(prices: pd.DataFrame, daily_sent: pd.DataFrame) -> pd.DataFrame:
    feat = prices.merge(daily_sent.reset_index(), on="date", how="left")
    # forward-fill sentiment to cover weekends/holidays (carry last known sentiment)
    for col in [c for c in feat.columns if c.startswith("sent_")]:
        feat[col] = feat[col].fillna(method="ffill").fillna(0.0)
    # drop rows where label is nan (last row)
    feat = feat.dropna(subset=["y_up"])
    return feat

def train_eval(feat: pd.DataFrame):
    # choose features
    X = feat[[
        "ret_1d", "ret_5d", "vol_chg",
        "rsi_14", "macd", "macd_signal", "sma_spread",
        "sent_mean", "sent_median", "sent_std", "sent_n",
        "sent_3d_ma", "sent_5d_ma", "sent_mom"
    ]].fillna(0.0)
    y = feat["y_up"].astype(int)

    # time-series split (e.g., 5 folds)
    tscv = TimeSeriesSplit(n_splits=5)
    accs, f1s, rocs = [], [], []
    clf = GradientBoostingClassifier(random_state=42)

    for train_idx, test_idx in tscv.split(X):
        Xtr, Xte = X.iloc[train_idx], X.iloc[test_idx]
        ytr, yte = y.iloc[train_idx], y.iloc[test_idx]

        clf.fit(Xtr, ytr)
        pred = clf.predict(Xte)
        proba = clf.predict_proba(Xte)[:, 1]

        accs.append(accuracy_score(yte, pred))
        f1s.append(f1_score(yte, pred))
        rocs.append(roc_auc_score(yte, proba))

    print(f"TimeSeries CV — Accuracy: {np.mean(accs):.3f} ± {np.std(accs):.3f}, "
          f"F1: {np.mean(f1s):.3f} ± {np.std(f1s):.3f}, "
          f"ROC-AUC: {np.mean(rocs):.3f} ± {np.std(rocs):.3f}")

    # final fit on all data
    clf.fit(X, y)
    return clf

if __name__ == "__main__":
    TICKER = "AAPL"
    NEWS_CSV = "news.csv"
    START = "2021-01-01"

    print("Loading news…")
    news = load_news(NEWS_CSV)

    print("Loading FinBERT… (first time may download model)")
    finbert = build_finbert_pipeline()

    print("Scoring sentiment…")
    daily_sent = score_sentiment(news, finbert)

    print("Loading prices…")
    prices = load_prices(TICKER, start=START)

    print("Merging features…")
    feat = assemble_dataset(prices, daily_sent)

    print("Training & evaluating…")
    model = train_eval(feat)

    # Example: predict last 10 days
    X_latest = feat[[
        "ret_1d", "ret_5d", "vol_chg",
        "rsi_14", "macd", "macd_signal", "sma_spread",
        "sent_mean", "sent_median", "sent_std", "sent_n",
        "sent_3d_ma", "sent_5d_ma", "sent_mom"
    ]].tail(10).fillna(0.0)
    proba_up = model.predict_proba(X_latest)[:, 1]
    print("Last 10 days — P(up) =", np.round(proba_up, 3))
