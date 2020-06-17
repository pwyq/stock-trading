from datetime import date

import extractor as ext
import constants as const


def extract_bloomberg(path):
    # header article
    tag = 'single-story-module__headline-link'
    raw_1 = ext.extract_web(const.URL_BLOOMBERG, tag)
    ext.write_to_csv(path, raw_1, 0.9, const.URL_BLOOMBERG)

    # related header article 
    tag = 'single-story-module__related-story-link'
    raw_2 = ext.extract_web(const.URL_BLOOMBERG, tag)
    ext.append_to_csv(path, raw_2, 0.8, const.URL_BLOOMBERG)

    # non-header article
    tag = 'story-package-module__story__headline-link'
    raw_3 = ext.extract_web(const.URL_BLOOMBERG, tag)
    ext.append_to_csv(path, raw_3, 0.5, const.URL_BLOOMBERG)


def extract_financial_times(path):
    tag = 'js-teaser-heading-link'
    raw = ext.extract_web(const.URL_FT, tag)
    ext.write_to_csv(path, raw, 1, const.URL_FT)


if __name__ == "__main__":
    d = date.today().strftime("%y-%m-%d")
    
    output_path = "../data/" + "financial-times-" + d + ".csv"
    extract_financial_times(output_path)

    output_path = "../data/" + "bloomberg-" + d + ".csv"
    extract_bloomberg(output_path)