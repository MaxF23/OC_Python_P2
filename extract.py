from bs4 import BeautifulSoup
import requests


# All Product info from books URL
# All info into a csv file
def request(string):
    response = requests.get(string)
    if response.ok:
        return BeautifulSoup(response.text, 'html.parser')


# From book URL
# Function Title
def title(soup):
    return soup.find('h1').text.replace(',', '')


# Function Category
def category(soup):
    cat = soup.find('ul', {'class': 'breadcrumb'})
    cat_a = cat.find_all('a')
    return cat_a[2].text


# Function Review rating
def get_review_rating(soup):
    star_rating = str(soup.find('p', {'class': 'star-rating'}))
    # star rating is now a string and the number of stars is between str[22] and str[27]
    star_review = star_rating[22:27].split('"')
    return star_review[0]


# Function Image URL
def img_url(soup):
    image_url = soup.find('div', {'class': 'item active'}).find()
    # <img alt="The Black Maria" src="../../media/cache/d1/7a/d17a3e313e52e1be5651719e4fba1d16.jpg"/>
    img_url_temp = str(image_url).split('"')
    # ['<img alt=', 'The Black Maria', ' src=', '../../media/cache/d1/7a/d17a3e313e52e1be5651719e4fba1d16.jpg',
    # '/>']
    return 'http://books.toscrape.com/' + img_url_temp[3].replace('../', '')


# Description
def description(soup):
    desc = soup.find_all('p')
    return desc[3].text.replace(',', ' ')


# UPC
def upc(soup):
    product_info = soup.find_all('tr')
    # Info <td> in each <tr>
    return product_info[0].find('td').text


# price_in_tax
def price_in_tax(soup):
    product_info = soup.find_all('tr')
    price = product_info[3].find('td').text
    return str(price).replace('Â', '')


# price_ex_tax
def price_ex_tax(soup):
    product_info = soup.find_all('tr')
    price = product_info[2].find('td').text
    return str(price).replace('Â', '')


# Nb_available
def nb_available(soup):
    product_info = soup.find_all('tr')
    return product_info[5].find('td').text
