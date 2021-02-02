import requests
from bs4 import BeautifulSoup
import csv342 as csv
import os


# All categories URL from Books index page
# All categories pages URL from categories URL
# All books URL from categories pages URL
# All Product info from books URL
# All info into a csv file

# Dictionary to csv
# Pandas lib to read csv? User input category?


# Function Title
def title(url):
    return request(url).find('h1').text.replace(',', '')


# Function Category
def category(url):
    cat = request(url).find('ul', {'class': 'breadcrumb'})
    cat_a = cat.find_all('a')
    return cat_a[2].text


# Function Review rating
def review_rating(url):
    star_rating = str(request(url).find('p', {'class': 'star-rating'}))
    # star rating is now a string and the number of stars is between str[22] and str[27]
    star_review = star_rating[22:27].split('"')
    return star_review[0]


# Function Image URL
def img_url(url):
    image_url = request(url).find('div', {'class': 'item active'}).find()
    # <img alt="The Black Maria" src="../../media/cache/d1/7a/d17a3e313e52e1be5651719e4fba1d16.jpg"/>
    img_url_temp = str(image_url).split('"')
    # ['<img alt=', 'The Black Maria', ' src=', '../../media/cache/d1/7a/d17a3e313e52e1be5651719e4fba1d16.jpg',
    # '/>']
    return 'http://books.toscrape.com/' + img_url_temp[3].replace('../', '')


# Description
def description(url):
    desc = request(url).find_all('p')
    return desc[3].text.replace(',', ' ')


# UPC
def upc(url):
    product_info = request(url).find_all('tr')
    # Info <td> in each <tr>
    return product_info[0].find('td').text


# price_in_tax
def price_in_tax(url):
    product_info = request(url).find_all('tr')
    price = product_info[3].find('td').text
    return str(price).replace('Â', '')


# price_ex_tax
def price_ex_tax(url):
    product_info = request(url).find_all('tr')
    price = product_info[2].find('td').text
    return str(price).replace('Â', '')


# Nb_available
def nb_available(url):
    product_info = request(url).find_all('tr')
    return product_info[5].find('td').text


# request
def request(url):
    response = requests.get(url)
    if response.ok:
        return BeautifulSoup(response.text, 'html.parser')


# make_url
def make_url(name, url):
    return 'http://books.toscrape.com/catalogue/' + str(name) + str(url).replace('../', '')


# Get image
def get_image(list):
    dir_path = os.getcwd() + '/Images'
    for i in range(len(list)):
        url = list[i]
        page = requests.get(url)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        f_ext = os.path.splitext(url)[-1]
        f_name = str(titles[i]).replace('/', '').replace(' ', '_') + '{}'.format(f_ext)
        print(dir_path + '/' + f_name)
        with open(dir_path + '/' + f_name, 'wb') as file:
            file.write(page.content)


# Function category_pages
def category_pages():
    books = 0
    for i in range(len(categories_url)):
        url = categories_url[i]
        # Page(s) per category
        results = request(url).find('form', {'class': 'form-horizontal'})
        nb_books = results.find('strong')
        nb_page_category = int((int(nb_books.text)) / 20) + 1
        # All books URL from categories pages URL
        # All books URL per category
        if nb_page_category == 1:  # /index.html if only one page
            all_h3 = request(url).find_all('h3')
            for h3 in all_h3:
                a = h3.find('a')  # <a> in <h3> contains href=URL + title
                url2 = a['href']
                # Add http://books.toscrape.com/ to href content for complete URL
                books_url.append(make_url(name, url2))
                books += 1
                print(str(books) + ' books')
        else:  # /page-x.html if multiple page
            for j in range(nb_page_category):
                url3 = url.replace('index.html', 'page-') + str(j + 1) + '.html'
                # All books URL in one page
                # <h3>
                #   <a href="catalogue/a-light-in-the-attic_1000/index.html"
                #      title="A Light in the Attic">A Light in the ...
                #   </a>
                # </h3>
                all_h3 = request(url3).find_all('h3')
                for h3 in all_h3:
                    a = h3.find('a')  # <a> in <h3> contains href=URL + title
                    url4 = a['href']
                    # Add http://books.toscrape.com/ to href content for complete URL
                    books_url.append(make_url(name, url4))
                    books += 1
                    print(str(books) + ' books')

# All categories URL from Books index page
categories_url = []
name = 'category/'
books_url = []
url = 'http://books.toscrape.com/catalogue/category/books_1/page-1.html'
all_ul = request(url).find('div', {'class': 'side_categories'})
all_li = all_ul.find_all('li')
for li in all_li:
    a = li.find('a')
    url = a['href']
    categories_url.append(make_url(name, url))

del categories_url[0]  # =http://books.toscrape.com/catalogue/category/books_1/index.html

# All categories pages URL from categories URL
name = ''
titles = []
categories = []
UPCs = []
prices_ex_tax = []
prices_in_tax = []
nb_in_stock = []
review_ratings = []
descriptions = []
img_urls = []
category_pages()
x = 0
z = 1
for j in range(len(books_url)):
    book_url = books_url[j]
    img_urls.append(img_url(book_url))
    titles.append(title(book_url))
    """
    categories.append(category())
    prices_ex_tax.append(price_ex_tax())
    prices_in_tax.append(price_in_tax())
    review_ratings.append(review_rating())
    nb_in_stock.append(nb_available())
    UPCs.append(upc())
    descriptions.append(description())"""
    x += 1
    y = int(x / 10)
    if y != z:
        print('Scraping products info ' + str(y) + '%')
    z = y

get_image(img_urls)
"""Books_info = {'product_page_url': books_url,
              'universal_product_code': UPCs,
              'title': titles,
              'price_including_tax': prices_in_tax,
              'price_excluding_tax': prices_ex_tax,
              'number_available': nb_in_stock,
              'product_description': descriptions,
              'category': categories,
              'review_rating': review_ratings,
              'image_url': img_urls
              }

with open('books.csv', 'w') as f:
    w = csv.writer(f)
    w.writerows(Books_info.items())"""
