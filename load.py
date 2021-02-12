import csv
import os
import requests
from extract import title, category


# Save image
# Download and save an image from URL
def save_image(img_url, page_url):
    img_path = os.getcwd() + '/Images'
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    dir_path = os.getcwd() + '/Images/' + category(page_url)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    page = requests.get(img_url)
    f_ext = os.path.splitext(img_url)[-1]
    f_name = str(title(page_url)).replace('/', '').replace(' ', '_') + '{}'.format(f_ext)
    with open(dir_path + '/' + f_name, 'wb') as file:
        file.write(page.content)


# Dict to csv
# Save a dictionary to csv file
def dict_to_csv(dic, category_as_title, dict_row):
    dir_path = os.getcwd() + '/CSV'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    with open(dir_path + '/' + str(category_as_title) + '.csv', 'w') as f:
        fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
                      'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                      'image_url']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in dict_row:
            writer.writerow(dic[i])
