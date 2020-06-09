from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from plyer import notification


def scrapePage(url, fileName):

    recipes = {}

    driver = webdriver.Chrome(
        'D:/nicklbaert/desktop/scrape-chefkoch/chromedriver.exe')
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content)

    print('now scraping '+url+'...')

    recipeLinks = soup.findAll(
        'a', attrs={'class': 'ds-mb ds-mb-row ds-card rsel-recipe bi-recipe-item'})

    for a in recipeLinks:

        url = a['href']

        nameTemp = a.find(
            'h2', attrs={'class': 'ds-h3 ds-heading-link'}).get_text()

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

        if timeTemp:
            for span in timeTemp.findAll('span'):
                text = span.get_text().strip().replace(
                    '                    ', '').replace('', '').replace('\n', '')
            if(text.startswith('Gesamtzeit')):
                timeTemp = text[15:len(text)]
        else:
            timeTemp = 'none'

        servesTemp = recipeSoup.find('input', attrs={'name': 'portionen'})
        if servesTemp:
            servesTemp = servesTemp['value']
        else:
            servesTemp = 'none'

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
            'img', attrs={'class': 'i-amphtml-replaced-content'})

        if imageUrl:
            imageUrl = imageUrl['src']

        else:
            imageUrl = 'none'

        recipe = {
            'title': nameTemp,
            'subtitle': descsTemp,
            'quant': amountsTemp,
            'ingr': ingredientsTemp,
            'time': timeTemp,
            'serves': servesTemp,
            'steps': stepsTemp,
            'tags': tagsTemp,
            'img': imageUrl,
        }

        position = recipeLinks.index(a)

        recipes[position] = recipe

    df = pd.DataFrame(recipes)
    df.to_json('output/'+fileName+'.json')


fileNames = [
    'glutenfreie-rezepte',
]

siteUrls = [
    'https://www.chefkoch.de/rs/s0t1605/glutenfrei/Gluten-Rezepte.html',
]

print('Looping through sites...')

for i in range(len(siteUrls)):
    scrapePage(siteUrls[i], fileNames[i])

print('Done looping through sites...')
