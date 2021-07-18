import requests
from bs4 import BeautifulSoup
import csv

# class Livre():
#     def __init__(self):
#         self.title = ""
#         self.universal_product_code = "[]"
#         self.price_including_tax = 0
#         self.price_excluding_tax = 0
#         self.number_available = 0
#         self.product_description = ""
#         self.category = ""
#         self.review_rating = 0
#         self.image_url = ""

title = []
universal_product_code = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url = []
product_page_url = []


# Scrapping page principale
url = "http://books.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content,'html.parser')
livres_soup = soup.find_all("h3")
for i in livres_soup:
    a = i.find("a")
    link = a["href"]
    product_page_url.append(url + link)

def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    # Scrapping du titre
    titre = soup.find_all("h1")
    for titres in titre:
        title.append(titres.string)

    # Scrapping de l'UPC, prix HT,prix TTC, Stock disponible
    tableau_soup = soup.find_all("tr")
    for i in tableau_soup:
        th = i.find("th")
        td = i.find("td")
        if th.string == "UPC":
            universal_product_code.append(td.string)
        elif th.string == "Price (excl. tax)":
            price_excluding_tax.append(td.string)
        elif th.string == "Price (incl. tax)":
            price_including_tax.append(td.string)
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
            number_available.append(n_stock)

    # Scrapping de la description
    desc_soup = soup.find("h2")
    description = desc_soup.find_next("p")
    product_description.append(description.string)

    # Scrapping de la catégorie
    category_soup = soup.find(class_="breadcrumb")
    active = category_soup.find(class_="active")
    book_category = active.find_previous("a")
    for content in book_category:
        category.append(content)

    # Scrapping du rating
    rating_soup = soup.find("p",class_="star-rating")
    star = rating_soup["class"]
    final_rating = star[1]

    if final_rating == "One":
        review_rating.append(1)
    elif final_rating == "Two":
        review_rating.append(2)
    elif final_rating == "Three":
        review_rating.append(3)
    elif final_rating == "Four":
        review_rating.append(4)
    elif final_rating == "Five":
        review_rating.append(5)

    # Scrapping image
    image_soup = soup.find(class_="carousel")
    src_img = image_soup.img["src"]
    fixed_img = src_img.replace("../", "")
    lien_image = "http://books.toscrape.com/" + fixed_img
    image_url.append(lien_image)

# Création CSV
def csv_file():
    en_tete = ["titre","upc","ht","ttc","stock","description","categorie","rating","img","url"]
    with open('D:\Dev\_OpenClassRooms\Projet_2\Livres.csv',"w") as livre_csv:
        writer = csv.writer(livre_csv,delimiter =",")
        writer.writerow(en_tete)

        for titre,upc,ht,ttc,stock,description,categorie,rating,img,url in zip(title,universal_product_code,
        price_including_tax,price_excluding_tax,number_available,
        product_description,category,review_rating,image_url,product_page_url):
            writer.writerow([titre,upc,ht,ttc,stock,description,categorie,rating,img,url])

if __name__ == '__main__':
    for liens in product_page_url:
        scrape(liens)

    csv_file()