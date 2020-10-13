from bs4 import BeautifulSoup
import requests
import re

def scraper():

    ret = {}

    states = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ha', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky',
              'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'nc', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'nd',
              'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy']

    base_link = "https://vote.gov/register/"

    for state in states:
        url = "{}{}".format(base_link, state)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        links = soup.find_all(class_="reg-link")
        init = []
        for link in links:
            href = re.findall(r"<a href=\"(.*)\"", str(link))
            try:
                init.append(href[0])
            except IndexError:
                classhref = re.findall(r"<a class=\"reg-link\" href=\"(.*)\"", str(link))
                try:
                    init.append(classhref[0])
                except IndexError:
                    pass

        ret[state] = init

    return ret



print(scraper())