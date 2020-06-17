import extractor as ext
from datetime import date


if __name__ == "__main__":
    URL = 'https://www.ft.com'
    output_path = "../data"
    tag = 'js-teaser-heading-link'

    d = date.today().strftime("%y-%m-%d")
    output_path += "/" + "financial-times-" + d + ".csv"

    raw = ext.extract_web(URL, tag)
    ext.write_to_csv(output_path, raw, 1, URL)

    # End of File