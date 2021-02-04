import requests
from bs4 import BeautifulSoup
import csv342 as csv
import os

# All categories URL from Books index page
# All categories pages URL from categories URL
# All books URL from categories pages URL
# All Product info from books URL
# All info into a csv file


# Request
# Pull data out of a HTML page
def request(string):
    response = requests.get(string)
    if response.ok:
        return BeautifulSoup(response.text, 'html.parser')


# make_url
# Return a URL from a character string
def make_url(name, char):
    return 'http://books.toscrape.com/catalogue/' + str(name) + str(char).replace('../', '')


# Categories url
# All categories URL from Books index page
def categories_url(string):
    url_categories = []
    name = 'category/'
    all_ul = request(string).find('div', {'class': 'side_categories'})
    all_li = all_ul.find_all('li')
    for li in all_li:
        tag_a = li.find('a')
        url_temp = tag_a['href']
        url_categories.append(make_url(name, url_temp))
    del url_categories[0]  # =http://books.toscrape.com/catalogue/category/books_1/index.html
    return url_categories


# Function category_pages
# All categories pages URL from categories URL return list of books URL
def category_pages(lis):
    books = 0
    name = ''
    books_url = []
    for i in range(len(lis)):
        url2 = lis[i]
        # Page(s) per category
        soup = request(url2)
        results = soup.find('form', {'class': 'form-horizontal'})
        nb_books = results.find('strong')
        nb_page_category = int((int(nb_books.text)) / 20) + 1
        # All books URL from categories pages URL
        # All books URL per category
        if nb_page_category == 1:  # /index.html if only one page
            all_h3 = soup.find_all('h3')
            for h3 in all_h3:
                tag_h3 = h3.find('a')  # <a> in <h3> contains href=URL + title
                url_temp_2 = tag_h3['href']
                # Add http://books.toscrape.com/ to href content for complete URL
                books_url.append(make_url(name, url_temp_2))
                books += 1
                print(str(books) + ' books')
        else:  # /page-x.html if multiple page
            for j in range(nb_page_category):
                url3 = url2.replace('index.html', 'page-') + str(j + 1) + '.html'
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
    return books_url


# Get image
# Download and save an image from URL
def get_image(string):
    dir_path = os.getcwd() + '/Images'
    page = requests.get(string)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    f_ext = os.path.splitext(string)[-1]
    f_name = str(title(bs)).replace('/', '').replace(' ', '_') + '{}'.format(f_ext)
    with open(dir_path + '/' + f_name, 'wb') as file:
        file.write(page.content)


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
def review_rating(soup):
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


# Dict to csv
# Save a dictionary to csv file
def dict_to_csv(dic):
    with open('books.csv', 'w') as f:
        fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
                      'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                      'image_url']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(dic)):
            writer.writerow(dic[i])

url = 'http://books.toscrape.com/catalogue/category/books_1/page-1.html'
books_url = category_pages(categories_url(url))
book_info = {}
x = 0
z = 1
for j in range(len(books_url)):
    book_url = books_url[j]
    bs = request(book_url)
    get_image(img_url(bs))
    book_info[j] = {'product_page_url': book_url,
                    'universal_product_code': upc(bs),
                    'title': title(bs),
                    'price_including_tax': price_in_tax(bs),
                    'price_excluding_tax': price_ex_tax(bs),
                    'number_available': nb_available(bs),
                    'product_description': description(bs),
                    'category': category(bs),
                    'review_rating': review_rating(bs),
                    'image_url': img_url(bs)
                    }
    x += 1
    y = int(x / 10)
    if y != z:
        print('Scraping products info ' + str(y) + '%')
    z = y
dict_to_csv(book_info)



