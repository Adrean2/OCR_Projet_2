import requests
from bs4 import BeautifulSoup
import csv


def scrape_categories():
    # Scrapping Categories
    category_list = []
    category_url = []
    iteration = 2

    url = "http://books.toscrape.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    nav_soup = soup.find("ul", class_="nav nav-list")
    list = nav_soup.find_all("li")
    for i in list:
        a = i.find("a")
        for y in a :
            fixed_y = y.strip().lower()
            category_list.append(fixed_y)
    category_list.pop(0)

    for i in category_list:
        link = "http://books.toscrape.com/catalogue/category/books/{}_{}/index.html".format(i,iteration)
        iteration += 1
        category_url.append(link)

    return category_list, category_url

def scrape_url(): 
    url = "http://books.toscrape.com/catalogue/"
    # Scrapping URL produit
    books_url = []
    page_count = 2

    def scrap_livre(lien):
        page = requests.get(lien)
        soup = BeautifulSoup(page.content,"html.parser")
        livres_soup = soup.find_all("h3")   
        for i in livres_soup:
            a = i.find("a")
            link = a["href"]
            flink = link.replace("../","")
            final_link =  url + flink
            books_url.append(final_link)

    categories = scrape_categories()
    for i in categories[1]:
        scrap_livre(i)
        page_check = i.replace("/index.html","/page-{}.html".format(page_count))
        test = requests.get(page_check)
        if test is True:
            scrap_livre(page_check)
        
    return books_url

def scrape(lien):

    title = ''
    universal_product_code = 0
    price_including_tax = 0
    price_excluding_tax = 0
    number_available = 0
    product_description = ""
    category = ""
    review_rating = 0
    image_url = ""
    product_page_url = lien

    page = requests.get(lien)
    soup = BeautifulSoup(page.content,'html.parser')
    
    # Scrapping du titre
    titre = soup.find("h1")
    title = titre.string

    # Scrapping de l'UPC, prix HT,prix TTC, Stock disponible
    tableau_soup = soup.find_all("tr")
    for i in tableau_soup:
        th = i.find("th")
        td = i.find("td")
        if th.string == "UPC":
            universal_product_code = td.string
        elif th.string == "Price (excl. tax)":
            price_excluding_tax = td.string
        elif th.string == "Price (incl. tax)":
            price_including_tax = td.string
        # Je dois extraire le nombre d'une chaîne de charactères(str)
        elif th.string == "Availability":
            stock = []
            # Je sépare chaque charactère de la chaîne
            for y in td.string:
                # S'il  s'agit d'un int, je l'extrait.
                if y.isdigit():
                    stock.append(y)
            # Je fusionne les int que j'ai extrait pour trouver le nombre final.
            n_stock = "".join(stock)
            number_available = n_stock

    # Scrapping de la description
    desc_soup = soup.find("h2")
    description = desc_soup.find_next("p")
    product_description = description.string

    # Scrapping de la catégorie
    category_soup = soup.find(class_="breadcrumb")
    active = category_soup.find(class_="active")
    book_category = active.find_previous("a")
    for content in book_category:
        category = content

    # Scrapping du rating
    rating_soup = soup.find("p",class_="star-rating")
    star = rating_soup["class"]
    final_rating = star[1]

    if final_rating == "One":
        review_rating = 1
    elif final_rating == "Two":
        review_rating = 2
    elif final_rating == "Three":
        review_rating = 3
    elif final_rating == "Four":
        review_rating = 4
    elif final_rating == "Five":
        review_rating = 5

    # Scrapping image
    image_soup = soup.find(class_="carousel")
    src_img = image_soup.img["src"]
    fixed_img = src_img.replace("../", "")
    lien_image = "http://books.toscrape.com/" + fixed_img
    image_url = lien_image

    # Création CSV
    en_tete = ["titre","upc","ht","ttc","stock","description","categorie","rating","img","url"]
    with open('D:\Dev\_OpenClassRooms\Projet_2\{}.csv'.format(str(category)),"w") as livre_csv:
        writer = csv.writer(livre_csv,delimiter =",")
        writer.writerow(en_tete)
        writer.writerow([title,universal_product_code,price_excluding_tax,price_including_tax,number_available,product_description,category,review_rating,image_url,product_page_url])

url = scrape_url()

for lien in url:
    scrape(lien)


# if __name__ == '__main__':
#     for url,categorie in zip (category_url,category_list):
#         scrape(url,categorie)