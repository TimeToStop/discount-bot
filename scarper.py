import json

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.biglion.ru"

HEALTH_URL = "/services/health/"
BEAUTY_URL = "/services/beauty/"
RESTAURANT_URL = "/services/restaurant/"

HEALTH = "health"
BEAUTY = "beauty"
RESTAURANT = "restaurant"

FILEPATH = "./data.json"


def fix_str(s):
    return " ".join(s.split())


def make_url(category, page_id):
    return f'{BASE_URL}{category}?page={page_id}'


def scarp(category, page_id):
    url = make_url(category, page_id)
    request = requests.get(url)

    if request.status_code // 100 != 2:
        return []

    results = []
    soup = BeautifulSoup(request.text, "html.parser")
    cards = soup.findAll("div", class_="card-item")

    for card in cards:
        try:
            # For fix/dev/debug
            # if card.attrs["data-id"] == "5289135":
            #     print(card)

            # skip, if it is ad banner (a tag only)
            if len(list(filter(lambda x: x.name is not None, card.contents))) == 1:
                continue

            picture = card.a.img.attrs["data-src"]
            discount = card.a.span.span.get_text()
            link = card.div.contents[2].attrs["href"]
            description = card.div.contents[2].get_text()
            price_spans = card.div.div.div.a.contents
            price = price_spans[len(price_spans) - 1].get_text()
            results.append({
                "id": card.attrs["data-id"],
                "picture": "https:" + picture,
                "discount": fix_str(discount),
                "link": BASE_URL + link,
                "description": fix_str(description),
                "price": fix_str(price)
            })
        except:
            print('Failed to parse card')
            print(card)

    return results


def gather(discount_type, category):
    data = []
    index = 1

    while True:
        # Print progress
        print(f"Page {index}")
        results = scarp(category, index)
        index += 1

        if len(results) == 0:
            break

        for result in results:
            result["type"] = discount_type
            data.append(result)

    return data


def main():
    categories = [
        [HEALTH, HEALTH_URL],
        [BEAUTY, BEAUTY_URL],
        [RESTAURANT, RESTAURANT_URL]
    ]

    data = []

    for [category, url] in categories:
        print(category, url)

        for result in gather(category, url):
            data.append(result)

    print('Discounts found ' + str(len(data)))

    with open('data.json', 'w') as f:
        json.dump(data, f)
        f.close()


if __name__ == "__main__":
    main()
