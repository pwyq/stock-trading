import extractor as ext
from datetime import date


if __name__ == "__main__":
    URL = 'https://www.bloomberg.com'
    output_path = "../data"

    d = date.today().strftime("%y-%m-%d")
    output_path += "/" + "bloomberg-" + d + ".csv"

    # header
    tag = 'single-story-module__headline-link'
    raw_1 = ext.extract_web(URL, tag)
    ext.write_to_csv(output_path, raw_1, 0.9, URL)

    # header related 
    tag = 'single-story-module__related-story-link'
    raw_2 = ext.extract_web(URL, tag)
    ext.append_to_csv(output_path, raw_2, 0.8, URL)

    # non-header
    tag = 'story-package-module__story__headline-link'
    raw_3 = ext.extract_web(URL, tag)
    ext.append_to_csv(output_path, raw_3, 0.5, URL)

    # End of File