from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests

driver = webdriver.Chrome(ChromeDriverManager().install())
set_names=[] #List to store name of the product
total_set_card_counts=[] #List to store price of the product
card_numbers=[]
card_names=[]
rarities=[]
mid_prices=[]
evolutions=[]
image_names=[]
image_links=[]




driver.get("https://pkmncards.com/set/darkness-ablaze/")
content = driver.page_source
soup = BeautifulSoup(content)
for a in soup.findAll('div', attrs={'class':'entry-content'}):
    
    set_name=a.find('a', attrs={'class':'set'})
    card_number = a.find('a', attrs={'class':'number'})

    artist = a.find('p', attrs={'class':'artist-set'})

    card_name = a.find('a', attrs={'class':'name'})
    raritie = a.find('a', attrs={'class':'rarity'})
    mid_price = a.find('a', attrs={'title':'Mid Price'})
    evolution = a.find('a', attrs={'class':'stage'})
    image_link = a.find('div', attrs={'class':'card-image'})



    # price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
    # rating=a.find('div', attrs={'class':'hGSR34'})
    try:
        set_names.append(set_name.text)
    except:
        set_names.append("-----")

    try:
        # This code is vunarable, for totoal card counts. because it's just plain text on the webpage
        artist_list = list(artist.children)
        for i in artist_list:
            if str(i)[0] == '/':
                index = artist_list.index(i)
                if artist_list[index-1].find('number') != -1:
                    total_set_card_count = i[1:].split(" ")[0]
        total_set_card_counts.append(total_set_card_count)
    except:
        total_set_card_counts.append('-----')  

    try:
        card_names.append(card_name.text)
    except:
        card_names.append('-----')

    try:
        card_numbers.append(card_number.text)
    except:
        card_numbers.append('-----')

    try:
        rarities.append(raritie.text)
    except:
        rarities.append('-----')

    try:
        mid_prices.append(mid_price.text)
    except:
        mid_prices.append('-----')
    
    try:
        evolutions.append(evolution.text)
    except:
        evolutions.append('-----')

    try:
        image_link = image_link.a['href']
        image_links.append(image_link)
        image_name = image_link.split("uploads/")[1]
        image_names.append(image_name)
        # get image
        image = open("images/"+image_name,"wb")
        image.write(requests.get(image_link).content)
        image.close()


    except:
        image_names.append('-----')        


    # try:
    #     ratings.append(rating.text)
    # except:
    #     ratings.append('-----')


df = pd.DataFrame({'SetName':set_names,'TotalSetCardCount':total_set_card_counts,'CardName':card_names,'CardNumber':card_numbers,'Rarity':rarities,'MedPrice':mid_prices,'Evolution':evolutions,'ImageName':image_names}) 
df.to_csv('products.csv', index=False, encoding='utf-8')
print(df)
