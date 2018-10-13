#from flask import Flask
import requests
from bs4 import BeautifulSoup


links = []


def get_url(page):
    url = 'https://www.avito.ru/moskva/sobaki?p=%d' % (page)
    result = requests.get(url)
    if result.status_code == 200:
        return result.text
    else:
        print('smth went wrong')


def get_item_links(text):
    soup = BeautifulSoup(text, 'lxml')
    tags = soup.findAll('a', {'class': 'item-description-title-link'})
    for tag in tags:
        link = tag.attrs['href']
        links.append(link)
    return links


def get_item(url):
    result = requests.get(url)
    if result.status_code == 200:
        return result.text
    else:
        print('smth went wrong')


def get_item_params(html):
    result = {}
    soup = BeautifulSoup(html, 'lxml')

    item_id_date = soup.find('div', {'class': 'title-info-metadata'}).text
    item_id = item_id_date[6:16]
    result['item_id'] = item_id
    date = item_id_date[18:-14]
    result['date'] = date

    title = soup.find('div', {'class': 'sticky-header-prop sticky-header-title'}).text
    title = title[2:-2]
    result['title'] = title

    description_tag = soup.find('div', {'class': 'item-description'})
    description = description_tag.find('p').text
    result['description'] = description

    photo_links_tags = soup.findAll('div', {'class': 'gallery-img-frame js-gallery-img-frame'})
    photos = []
    for tag in photo_links_tags:
        photo_link = tag.attrs['data-url']
        photos.append(photo_link)
    result['photo_links'] = photos

    city_tag = soup.find('meta', {'itemprop': 'addressLocality'})
    city = city_tag.attrs['content']
    area_tag = soup.find('span', {'class': 'item-map-address'})
    area = area_tag.find('span').text
    address = [city, area]
    result['address'] = address

    return result


if __name__ == '__main__':
    page = 1
    items_params = []
    while page <= 1:
        text = get_url(page)
        items_links = get_item_links(text)
        page += 1
        for link in items_links:
            item_link = 'https://www.avito.ru' + link
            item_html = get_item(item_link)
            item_params = get_item_params(item_html)
            items_params.append(item_params)
    print(items_params[0])
