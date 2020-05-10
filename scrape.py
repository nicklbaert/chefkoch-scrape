from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from plyer import notification

fileNames = [
    'indische-rezepte',
    'pasta-rezepte',
    'chinesische-rezepte',
    'italienische-rezepte',
    'franzoesische-rezepte',
    'vegane-rezepte',
    'party-rezepte',
    'snack-rezepte',
    'studenten-rezepte',
    'pancake-rezepte',
    'steak-rezepte',
]

siteUrls = [
    'https://www.chefkoch.de/rs/s0g97/Indische-Rezepte.html',
    'https://www.chefkoch.de/rs/s0g81/Pasta-Rezepte.html',
    'https://www.chefkoch.de/rs/s0g95/Chinesische-Rezepte.html',
    'https://www.chefkoch.de/rs/s0g88/Italienische-Rezepte.html',
    'https://www.chefkoch.de/rs/s0g91/Franzoesische-Rezepte.html',
    'https://www.chefkoch.de/rs/s0g111/Vegane-Rezepte.html',
    'https://www.chefkoch.de/rs/s0g119/Partyrezepte.html',
    'https://www.chefkoch.de/rs/s0g83/Snack-Rezepte.html',
    'https://www.chefkoch.de/rs/s0g192/Studentenkueche.html',
    'https://www.chefkoch.de/rs/s0/pancakes/Rezepte.html',
    'https://www.chefkoch.de/rs/s0/steak/Rezepte.html',
]

names = []  # List to store name of the product
times = []
urls = []
amounts = []
ingredients = []
steps = []
time = []
serves = []
tags = []
descs = []
images = []

url = input('enter valid URL of recipe result page: ')
fileName = input('enter name of output file: ')

driver = webdriver.Chrome(
    'D:/nicklbaert/desktop/scrape-chefkoch/chromedriver.exe')
driver.get(url)

# https://www.chefkoch.de/rs/s0g97/Indische-Rezepte.html
# https://www.chefkoch.de/rs/s0g81/Pasta-Rezepte.html
# https://www.chefkoch.de/rs/s0g95/Chinesische-Rezepte.html
# https://www.chefkoch.de/rs/s0g88/Italienische-Rezepte.html
# https://www.chefkoch.de/rs/s0g91/Franzoesische-Rezepte.html
# https://www.chefkoch.de/rs/s0g111/Vegane-Rezepte.html
# https://www.chefkoch.de/rs/s0g119/Partyrezepte.html
# https://www.chefkoch.de/rs/s0g83/Snack-Rezepte.html
# https://www.chefkoch.de/rs/s0g192/Studentenkueche.html
# https://www.chefkoch.de/rs/s0/pancakes/Rezepte.html
# https://www.chefkoch.de/rs/s0/steak/Rezepte.html

content = driver.page_source
soup = BeautifulSoup(content)

print('fetching page...')

for a in soup.findAll('a', attrs={'class': 'ds-mb ds-mb-row ds-card rsel-recipe bi-recipe-item'}):
    url = a['href']

    nameTemp = a.find(
        'h2', attrs={'class': 'ds-h3 ds-heading-link'}).get_text()
    names.append(nameTemp)

    print('Currently scraping: ' + nameTemp)

    # now go to recipe and scrape ingredients
    driver.get(url)
    recipeContent = driver.page_source
    recipeSoup = BeautifulSoup(recipeContent, features="html.parser")

    amountsTemp = []
    ingredientsTemp = []
    timeTemp = ""
    servesTemp = 0
    stepsTemp = []
    currentSteps = ""
    tagsTemp = []
    descsTemp = ''

    for ingredientAmount in recipeSoup.findAll('td', attrs={'class': 'td-left'}):
        amount = ingredientAmount.get_text()
        amount = amount.strip().replace('                                ', ' ')
        amountsTemp.append(amount)

    for ingredientName in recipeSoup.findAll('td', attrs={'class': 'td-right'}):
        name = ingredientName.get_text()
        name = name.strip()
        ingredientsTemp.append(name)

    timeTemp = recipeSoup.find(
        'small', attrs={'class': 'rds-recipe-meta'})

    for span in timeTemp.findAll('span'):
        text = span.get_text().strip().replace(
            '                    ', '').replace('', '').replace('\n', '')
        if(text.startswith('Gesamtzeit')):
            timeTemp = text[15:len(text)]

    servesTemp = recipeSoup.find('input', attrs={'name': 'portionen'})
    servesTemp = servesTemp['value']

    currentSteps = recipeSoup.find('article', attrs={
                                   'class': 'ds-or-3'}).find('div', attrs={'class': 'ds-box'}).get_text()

    stepsTemp = currentSteps.split("\n")

    for i in range(len(stepsTemp)):
        stepsTemp[i] = stepsTemp[i].strip()

    stepsTemp = list(filter(("").__ne__, stepsTemp))

    for tag in recipeSoup.findAll('a', attrs={'class': 'bi-tags'}):
        tagsTemp.append(tag.get_text().strip())

    descsTemp = recipeSoup.find('p', attrs={
        'class': 'recipe-text'})

    if descsTemp:
        descsTemp = descsTemp.get_text().strip().replace(
            '\n', '').replace('                ', '')
    else:
        descsTemp = 'none'

    imageUrl = recipeSoup.find(
        'img', attrs={'class': 'i-amphtml-replaced-content'})['src']

    print('IMAGE URL:'+imageUrl)

    amounts.append(amountsTemp)
    ingredients.append(ingredientsTemp)
    time.append(timeTemp)
    serves.append(servesTemp)
    steps.append(stepsTemp)
    tags.append(tagsTemp)
    descs.append(descsTemp)
    images.append(imageUrl)


df = pd.DataFrame(
    {'title': names, 'desc': descs, 'amounts': amounts, 'ingredients': ingredients, 'time': time, 'serves': serves, 'steps': steps, 'tags': tags})
df.to_csv(fileName+'.csv', index=False, encoding='utf-8')

print('Done')
