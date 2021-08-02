import requests
import csv
import re
import os

def scrape_categories():
    # Scrapping Categories
    page = requests.get("http://books.toscrape.com/")
    scrape = page.text

    # Regex pour trouver les noms des catégories
    category_pattern = re.compile(r"\s+(.*)\s+</a>")
    category_name = category_pattern.findall(scrape)
    category_name.pop(0)

    # Regex pour trouver l'url de chaque catégories
    url_category = []
    url_category_pattern = re.compile(r"(\w+(\_|\-))*\w+\_\d{0,2}\/index\.html")
    matches = url_category_pattern.finditer(scrape)

    for match in matches:
        if "books_1" in match.group(0):
            lien = "https://books.toscrape.com/catalogue/category/{}".format(match.group(0))
        else:
            lien = "https://books.toscrape.com/catalogue/category/books/{}".format(match.group(0))
        url_category.append(lien)
    # Suppression de la catégorie Books qui contient tous les livres du site
    url_category.pop(0)

    return url_category,category_name

def scrape_url(lien): 
    url = "http://books.toscrape.com/catalogue/"
    # Scrapping URL produit
    books_url = []
    page_count = 1
    page = requests.get(lien)
    #Vérifie si la catégorie a plusieurs page#
    running = True
    while running == True:
        if page.status_code == 200:
            if page_count != 1:
                fixed_lien = lien.replace("index","page-{}".format(page_count))
            else:
                fixed_lien = lien
            #Scraping des urls des livres contenu dans la page#
            page = requests.get(fixed_lien)
            txt = page.text
            h3_pattern = re.compile(r"<h3>(.*?)</h3")
            h3_match = h3_pattern.finditer(txt)
            liens_pattern = re.compile(r"(\w+\-)*(\w*)+\_\d+/\w+\.\w+")
            for match in h3_match:
                liens_match = liens_pattern.finditer(match.group(0))
                for clean_url in liens_match:
                    books_url.append(url + clean_url.group(0))
            page_count += 1
        else:
            running = False

    return books_url

def scrape(lien,category):

    product_page_url = lien
    page = requests.get(lien)
    text_url = page.text

    #Scraping du titre du livre#
    titre_pattern = re.compile(r"<h1>(.*?)</h1")
    title = titre_pattern.finditer(text_url)

    for match in title:
        title = match.group(1)

    #Scraping du tableau qui contient l'UPC, prix HT, prix TTC et Stock#
    tableau_pattern = re.compile(r"<td>(.*?)</td>")
    tableau = tableau_pattern.findall(text_url) 
    #Scraping du prix HT#
    price_excluding_tax = re.sub(r"[Â£]","",tableau[2]) + '£'
    #Scraping du prix TTC#
    price_including_tax = re.sub(r"[Â£]","",tableau[3]) + '£'

    #Scraping UPC#
    universal_product_code = tableau[0]
    stock_pattern = re.compile(r"\d+")
    stock = stock_pattern.findall(tableau[5])

    #Scraping stock#
    number_available = stock[0]

    #Scrapping de la description#
    desc_pattern = re.compile(r"<p>(.*?)</p")
    description = desc_pattern.findall(text_url)

    if len(description) == 0:
        product_description = "il n'y a pas de description"
    else:
        product_description = description[0]

    # Scrapping du rating#
    rating_pattern = re.compile(r"(star\-rating).(\w+)")
    rating = rating_pattern.findall(text_url)

    review_rating = rating[0][1]

    #Scraping de l'image#
    image_pattern = re.compile(r"img.src\=\"(.*).jpg")
    image = image_pattern.findall(text_url)
    fixed_img = image[0].replace("../","")
    lien_image = "http://books.toscrape.com/" + fixed_img + '.jpg'

    image_url = lien_image

    #Création du dossier d'images
    directory = category + "_images"
    parent_dir ="D:\Dev\_OpenClassRooms\Projet_2"
    path = os.path.join(parent_dir,directory)
    if not os.path.exists(path):
        os.mkdir(path)
    os.chmod(path,0o777)

    #Enregistrement des images dans le bon répertoire
    image_request = requests.get(image_url)
    if image_request.status_code == 200:
        img_title = re.sub(r'[^\w_.)( -]',"", title)
        with open(path +"\{}.jpg".format(img_title),'wb') as f:
            f.write(image_request.content)

    #Ajout des informations dans les CSV correspondants#
    books_stats = [title,universal_product_code,price_excluding_tax,price_including_tax,number_available,product_description,category,review_rating,image_url,product_page_url]
    with open('D:\Dev\_OpenClassRooms\Projet_2\{}.csv'.format(str(category)),"a",encoding="UTF-8") as livre_csv:
        writer = csv.writer(livre_csv)
        writer.writerow(books_stats)

def create_csv(category):
    if type(category) == str :
        en_tete = ["titre","upc","ht","ttc","stock","description","categorie","rating","img","url"]
        with open('D:\Dev\_OpenClassRooms\Projet_2\{}.csv'.format(str(category)),"w",encoding="UTF-8") as livre_csv:
            write = csv.writer(livre_csv)
            write.writerow(en_tete)
    else:
        for i in category:
            en_tete = ["titre","upc","ht","ttc","stock","description","categorie","rating","img","url"]
            with open('D:\Dev\_OpenClassRooms\Projet_2\{}.csv'.format(str(i)),"w",encoding="UTF-8") as livre_csv:
                write = csv.writer(livre_csv)
                write.writerow(en_tete)

def main():

    #Renvoie une liste des liens et une liste des noms de chaque catégorie du site#
    categorie = scrape_categories()
    liens_categories = categorie[0]
    noms_categories = categorie[1]

    #Choix de l'index qui sera scrappé dans chaque liste#
    choix = input("Choisissez le(s) index à traiter (format slice -> index:index) : ")
    index = 0
    if ":" in choix :
        index_split = choix.split(":")
        index = slice(int(index_split[0]),int(index_split[1]))
    else:
        index = int(choix)
    #Permet de scrape les catégories choisies dans une slice
    if type(index) == slice:
        liens_to_scrape = liens_categories[index]
        noms_cat = noms_categories[index]
        for liens,noms in zip (liens_to_scrape,noms_cat):
            liens_livres = scrape_url(liens)
            for lien in liens_livres:
                scrape(lien,noms)
    # Permet de scrape une unique catégorie
    else:
        liens_livres = scrape_url(liens_categories[index])
        for lien in liens_livres:
            scrape(lien,noms_categories[index])
            
if __name__ == '__main__':
    main()
