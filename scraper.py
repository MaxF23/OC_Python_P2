# All categories URL from Books index page
# All categories pages URL from categories URL
# All books URL from categories pages URL


from extract import request, img_url, upc, price_in_tax, price_ex_tax, nb_available, description, get_review_rating, \
    title, category
from load import save_image, dict_to_csv
from transform import categories_url, category_pages, review_rating_number

url = 'http://books.toscrape.com/catalogue/category/books_1/page-1.html'
books_url = category_pages(categories_url(url))
book_info = {}
title_csv = 'Travel'
dict_row_category = []
x = 0
z = 1

for j in range(len(books_url)):
    book_url = books_url[j]
    bs = request(book_url)
    save_image(img_url(bs), bs)
    book_info[j] = {'product_page_url': book_url,
                    'universal_product_code': upc(bs),
                    'title': title(bs),
                    'price_including_tax': price_in_tax(bs),
                    'price_excluding_tax': price_ex_tax(bs),
                    'number_available': nb_available(bs),
                    'product_description': description(bs),
                    'category': category(bs),
                    'review_rating': review_rating_number(get_review_rating(bs)),
                    'image_url': img_url(bs)
                    }
    x += 1
    y = int(x / 10)
    if y != z:
        print('Scraping products info ' + str(y) + '%')
    if book_info[j].get("category") != title_csv:
        dict_to_csv(book_info, title_csv, dict_row_category)
        dict_row_category = []
        title_csv = book_info[j].get("category")
    dict_row_category.append(j)
    z = y

