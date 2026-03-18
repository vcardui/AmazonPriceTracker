# +----------------------------------------------------------------------------+
# | CARDUI TECH v1.0.0
# +----------------------------------------------------------------------------+
# | Copyright (c) 2026 - 2026, CARDUITECH.COM (www.carduitech.com)
# | Vanessa Reteguín <vanessa@reteguin.com>
# | Released under the MIT license
# | www.carduitech.com/license/
# +----------------------------------------------------------------------------+
# | Author.......: Vanessa Reteguín <vanessa@reteguin.com>
# | First release: March 16th, 2026
# | Last update..: March 16th, 2026
# | WhatIs.......: DataSearcher - Class
# +----------------------------------------------------------------------------++

# ------------ Resources / Documentation involved -------------
# My http header: https://myhttpheader.com
# Check regular expressions: https://regex101.com

# ------------------------- Libraries -------------------------
from bs4 import BeautifulSoup
import requests

# ------------------------- Class -------------------------
class DataSearcher:
    def __init__(self, url, headers=None):
        self.url = url

        if headers is None:
            self.headers = {}
        else:
            self.headers = headers
    def get_data(self, tag_name, tag_class, show_website_data=False, show_value=False):
        response = requests.get(self.url, headers=self.headers)
        website_html = response.text
        if show_website_data:
            print(website_html)

        soup = BeautifulSoup(website_html, 'html.parser')

        try:
            value = soup.find_all(name=tag_name, class_=tag_class)[0].get_text()

            if show_value:
                if value == '':
                    print("Empty Value")
                else:
                    print(f"value: {value}")

            return value

        except IndexError:
            if show_value:
                print(f"Tag not found: {tag_name} - {tag_class}")
            return ''