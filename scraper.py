import requests
from bs4 import BeautifulSoup
import csv
import time
import re

BASE = 'https://en.wikipedia.org'

def scraping(data) :
    i = 0

    # Gets the wiki page with all the malls
    r = requests.get('https://en.wikipedia.org/wiki/List_of_shopping_malls_in_the_United_States')
    soup = BeautifulSoup(r.content, 'html.parser')

    #Creates a list with all the states
    state = soup.find_all('ul')
    del state[0]
    for s in state[:53] :

        #Creates a list with all the malls in a state
        ligne = s.find_all('li')
        for l in ligne :
            d = dict()
            links = l.find_all('a')
            d['Country'] = 'USA'
            if len(links) >= 2 :
                d['City'] = links[1].text.strip()
            else : d['City'] = ''
            d['Name'] = links[0].text.strip()

            #Gets the wiki page of the mall
            urlMall = BASE + links[0]['href']
            rMall = requests.get(urlMall)

            if rMall.status_code == 200 :
                soupWiki = BeautifulSoup(rMall.content, 'html.parser')

                #Looks for table with the info
                tableau = soupWiki.find('table', class_='infobox vcard')
                if tableau != None :
                    ligne = tableau.find_all('tr')

                    #Looks for all keys and values in table in pageWiki
                    cle = []
                    valeur = []
                    for l in ligne :
                        if l.find('th') != None and l.find('td') != None :
                            c = l.find('th').text.strip()
                            v = l.find('td').text.strip()
                            cle.append(c)
                            valeur.append(v)

                    #Creates dictionnary with the keys and values in the table
                    dico = dict(zip(cle,valeur))
                    d['Owner'] = ''
                    d['Management'] =''
                    d['Stores'] = ''
                    d['GLA'] = ''
                    d['Parking'] = ''

                    #Looks for Location in the dictionnary
                    if d['City'] == '' in dico :
                        if 'Location' in dico :
                            d['City'] = dico['Location']

                    #Looks for Owner in the dictionnary
                    if 'Owner' in dico :
                        own = dico['Owner'].split('[')
                        d['Owner'] = own[0]

                    #Looks for Management in the dictionnary
                    if 'Management' in dico :
                        manage = dico['Management'].split('[')
                        d['Management'] = manage[0]

                    #Looks for number of Stores
                    if 'No. of stores and services' in dico :
                        stores = dico['No. of stores and services'].split('[')[0]
                        STORES = re.findall(r'[0-9]+', stores)
                        if STORES != [] :
                            d['Stores'] = int(STORES[0])

                    #Looks for GLA
                    if 'Total retail floor area' in dico :
                        gla = dico['Total retail floor area'].split(',')
                        j = 0
                        GLA = ''
                        while j < len(gla) :
                            GLA = GLA + gla[j]
                            j += 1
                        area = re.findall(r'[0-9]+', GLA)
                        if area != [] :
                            area = area[0]
                            if 'million' in dico['Total retail floor area'] :
                                area = int(area) * 1000000
                            d['GLA'] = area

                    if 'Parking' in dico :
                        parking = dico['Parking'].split('[')
                        d['Parking'] = parking[0]

                data.append(d)
                i += 1
                print(i, '/1416 : ', d['Name'], "fait.")
