# make_url
# Return a URL from a character string
from extract import request


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


def review_rating_number(string):
    if string[0] == 'O':
        return 1
    elif string[1] == 'w':
        return 2
    elif string[1] == 'h':
        return 3
    elif string[1] == 'o':
        return 4
    else:
        return 5

