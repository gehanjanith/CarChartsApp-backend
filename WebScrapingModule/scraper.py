import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq, Request
from urllib.parse import urljoin
import re
from datetime import datetime, timedelta


def convert_to_days(days_str):
    print('days_str', days_str)
    print(type(days_str))
    days_str = str(days_str)
    print('days_str_processed', days_str)

    if re.match(r'\d+ days?', days_str):
        days_value = int(re.search(r'\d+', days_str).group())
        current_date = datetime.now().date()
        processed_date = current_date - timedelta(days=days_value)
        return processed_date.strftime('%Y-%m-%d')
    if re.match(r'\d+ hours?', days_str):
        hours_value = int(re.search(r'\d+', days_str).group())
        current_date = datetime.now()
        processed_date = current_date - timedelta(hours=hours_value)
        return processed_date.strftime('%Y-%m-%d')
    elif re.match(r'\d+ hour?', days_str):
        hours_value = int(re.search(r'\d+', days_str).group())
        current_date = datetime.now()
        processed_date = current_date - timedelta(hours=hours_value)
        return processed_date.strftime('%Y-%m-%d')
    else:
        return 0  # You can handle other date formats as needed


def scrape_riyasewana(make, model, minYear, maxYear):
    carList = []
    carList.append(["title", "price", "img", "link", "city", "days", "supplier"])

    url = f"https://riyasewana.com/search/{make}/{model}/{minYear}-{maxYear}"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = uReq(req)
    page_soup = BeautifulSoup(page, 'html.parser')

    for link in page_soup.select('li[class*="item round"]'):
        tet = link.find('h2')
        if tet:
            heading = tet.text
        price_tag = link.select('div[class*="boxintxt b"]')[0].next

        # Skip if price is "Negotiable"
        if price_tag.strip().lower() == "negotiable":
            continue

        img = None
        img_box = link.select('div[class="imgbox"] a')
        if img_box:
            img_link = img_box[0].find('img')
            if img_link:
                img = "https://" + img_link.get('src')

        for site_link in link.findAll('a'):
            card_link = site_link.get('href')

        city = link.select('div[class*="boxintxt"]')[0].next
        days = link.select('div[class*="boxintxt s"]')[0].next

        carList.append([heading, price_tag, img, card_link, city, days, 'riyasewana'])

    return carList


def scrape_ikman(make, model, minYear, maxYear):
    carList = []
    carList.append(["title", "price", "img", "link", "city", "days", "supplier"])

    url = f"https://ikman.lk/en/ads/sri-lanka/cars/{make}/{model}?numeric.model_year.minimum={minYear}&numeric.model_year.maximum={maxYear}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.select('li[class*="normal-ad"]'):
        tet = link.find('h2')
        if tet:
            heading = tet.text
        price_tag = link.select('div[class*="price"] span')[0].next

        img = None
        img_links = link.select('div[class*="image"] img')
        for img_link in img_links:
            img_url = img_link.get('src')
            img = urljoin(url, img_url) if img_url else None

        for site_link in link.findAll('a'):
            card_link = "https://ikman.lk" + site_link.get('href')

        city = link.select('div[class*="description"]')[0].next
        days = convert_to_days(link.select('div[class*="updated-time"]')[0].next)

        carList.append([heading, price_tag, img, card_link, city, days, 'ikman'])

    return carList
