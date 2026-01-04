from requests import get
from bs4 import BeautifulSoup as bs
import pandas as pd

# DataFrame global            # Liste pour stocker les dictionnaires

def scrape_data(url, fin=10):
    Df = pd.DataFrame()
    if "moto-and-scooters" in url and fin > 10:
            fin = 10
    
    for page in range(1, fin+1):
        data = []
        url_page = f'{url}?&page={page}'
        contenu = get(url_page)                      
        soup = bs(contenu.content, 'html.parser')

        containers = soup.find_all('div', 'listings-cards__list-item mb-md-3 mb-3')

        for item in containers:
            try:
                # Marque
                marque = item.find('h2', 'listing-card__header__title').a.text.strip()

                # Prix
                prix = item.find('h3', 'listing-card__header__price font-weight-bold text-uppercase mb-0').text.strip().replace('F CFA', '').replace('\n', '')

                # Adresse
                # adresse = item.find('span', 'town-suburb d-inline-block').text.strip().replace(',', '')
                adresse = item.find('div', 'col-12 entry-zone-address').text.strip().replace(',', '').replace('\n',' ')

                # Propriétaire
                propriétaire = item.find('p', 'time-author m-0').a.text.strip().replace('Par', '')
                
                annee = None
                for mot in marque.split():
                    if mot.isdigit() and len(mot) == 4:
                        annee = mot
                        break
                
                element = {
                    "Marque": marque,
                    "Prix": prix,
                    "Adresse": adresse,
                    "Année": annee,
                    "Propriétaire": propriétaire
                }
                
                if "voitures-4" in url:
                    # Attributs
                    recu = item.find_all('li', 'listing-card__attribute list-inline-item')
                    boite = recu[2].text.strip()
                    carburant = recu[3].text.strip()

                    # Kilométrage
                    km = item.find(string=lambda text: text and "km" in text).strip().replace('km', '')
                    
                    element["Boite"] = boite
                    element["carburant"]=carburant
                    element["kilométrage"]=km
                
                data.append(element)
            except:
                pass
        df = pd.DataFrame(data)
        Df = pd.concat([Df, df], axis=0).reset_index(drop=True)
    
    return Df