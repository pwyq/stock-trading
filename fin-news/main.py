from datetime import datetime

import extractor as ext
import constants as const


def extract_bloomberg(path):
    # header article
    tag = 'single-story-module__headline-link'
    ts = get_timestamp()
    raw_1 = ext.extract_web_with_class_tag(const.URL_BLOOMBERG, tag)
    ext.write_to_csv(path, raw_1, 0.9, ts, const.URL_BLOOMBERG)

    # related header article 
    tag = 'single-story-module__related-story-link'
    ts = get_timestamp()
    raw_2 = ext.extract_web_with_class_tag(const.URL_BLOOMBERG, tag)
    ext.append_to_csv(path, raw_2, 0.8, ts, const.URL_BLOOMBERG)

    # non-header article
    tag = 'story-package-module__story__headline-link'
    ts = get_timestamp()
    raw_3 = ext.extract_web_with_class_tag(const.URL_BLOOMBERG, tag)
    ext.append_to_csv(path, raw_3, 0.5, ts, const.URL_BLOOMBERG)


def extract_financial_times(path):
    tag = 'js-teaser-heading-link'
    ts = get_timestamp()
    raw = ext.extract_web_with_class_tag(const.URL_FT, tag)
    ext.write_to_csv(path, raw, 1, ts, const.URL_FT)


def extract_marketwatch(path):
    tag = 'link'
    ts = datetime.now().timestamp()
    raw = ext.extract_web_with_class_tag(const.URL_MARKETWATCH, tag)
    ext.write_to_csv_marketwatch(path, raw, 1, ts)


def extract_yahoo_finances(path):
    attr_1 = "h3"
    ts = get_timestamp()
    raw_1 = ext.extract_web_with_attr(const.URL_YAHOO, attr_1)
    ext.write_to_csv(path, raw_1, 0.9, ts, const.URL_YAHOO)

    attr_2 = "h2"
    ts = get_timestamp()
    raw_2 = ext.extract_web_with_attr(const.URL_YAHOO, attr_2)
    ext.append_to_csv(path, raw_1, 0.8, ts, const.URL_YAHOO)


def get_timestamp():
    return int(datetime.now().timestamp())


if __name__ == "__main__":
    d = datetime.now().strftime("%y-%m-%d")
    
    output_path = "../data/" + "financial-times-" + d + ".csv"
    extract_financial_times(output_path)

    output_path = "../data/" + "bloomberg-" + d + ".csv"
    extract_bloomberg(output_path)

    output_path = "../data/" + "yahoo-" + d + ".csv"
    extract_yahoo_finances(output_path)

    output_path = "../data/" + "marketwatch-" + d + ".csv"
    extract_marketwatch(output_path)

    # End of File