from html.parser import HTMLParser
from html.entities import name2codepoint
import os
from bs4 import BeautifulSoup
import json
import urllib3
from PySide2.QtCore import QThread
from PySide2.QtGui import *
from PySide2.QtCore import *
import re

class MySignal(QObject):
    sig = Signal(str, bool)
    
class MyHTMLParser(QThread):#QThread
    def __init__(self, url):
        QThread.__init__(self)
        self.url = url
        self.signal = MySignal()

    def run(self):
        recipe_name, ingredients_list, steps = marmiton_parser(self.url)
        okToParse = (recipe_name != '') and (ingredients_list != []) and (steps != [])
        self.signal.sig.emit(self.url, okToParse)

# 1. option to include link to web page in recipe description (easy)
# 2. option to print page as pdf and display it/link to it in recipe (medium)
# 3. implement several famous website parsers (hard)

def marmiton_parser(url):
    recipe_name = ''
    ingredients_list = []
    steps = []
    
    try:
        soup = soup_from_url(url)
        
        #method 1
        # steps = soup.find_all('h3', class_ = "Stepsstyle__StepTitle-sc-1211b9i-1 laOcon")
        # steps_details = soup.find_all('p', class_ = "Stepsstyle__Text-sc-1211b9i-3 IhwQd")
        
        # for step, step_detail in zip(steps, steps_details):
        #     print('%s - %s' % (step.text, step_detail.text))
        
        #method 2 (from json)
        recipe_name, ingredients_list, steps = extract_from_json(soup)
        # recipe_name, ingredients_list, steps = extract_from_json_v2(soup)
    except:
        return recipe_name, ingredients_list, steps
    
    return recipe_name, ingredients_list, steps
    
    # print(steps_details)

def soup_from_html(html_file):
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, "html.parser")
    return soup

def soup_from_url(url):
    http_pool = urllib3.connection_from_url(url)
    r = http_pool.urlopen('GET',url)
    soup = BeautifulSoup(r.data.decode('utf-8'), "html.parser")
    return soup

def extract_from_json(soup):
    recipe_name = ''
    ingredients_list = []
    steps = []
    
    try:
        for script_content in soup.find_all('script'):
            if script_content.get('type') == 'application/ld+json':
                # print(test.string)
                data = json.loads(script_content.string)
                # print('json_explore')
                # print(data)
                if isinstance(data, dict):
                    # print('dict')
                    # print(data)
                    if 'name' in data.keys():
                        recipe_name = data['name']
                    if 'recipeIngredient' in data.keys():
                        ingredients_list = [ing for ing in data['recipeIngredient'] if ing != '']
                    if 'recipeInstructions' in data.keys():
                        instructions = data['recipeInstructions']
                        steps = []
                        for i, step in enumerate(instructions):
                            if isinstance(step, dict):
                                steps.append(step['text'])
                            elif isinstance(step, str):
                                steps.append(step)
                elif isinstance(data, list):
                    # print('list')
                    # print(data)
                    for step in data:
                        if isinstance(step, str):
                            steps.append(step)
                        elif isinstance(step, dict):
                            # print('dict in list')
                            # print(step)
                            recipe_name, ingredients_list, steps = recursive_json_explore(step)
                            if recipe_name != '' or ingredients_list != [] or steps != []:
                                # print('stop')
                                return recipe_name, ingredients_list, steps
                    # steps = data
                    # print(data)
            
    except:
        return recipe_name, ingredients_list, steps
                
    return recipe_name, ingredients_list, steps

def extract_from_json_v2(soup):
    recipe_name = ''
    ingredients_list = []
    steps = []
    for script_content in soup.find_all('script'):
        if script_content.get('type') == 'application/ld+json':
            # print(test.string)
            data = json.loads(script_content.string)
            recipe_name, ingredients_list, steps = recursive_json_explore(data)
    return recipe_name, ingredients_list, steps

def recursive_json_explore(data):
    recipe_name = ''
    ingredients_list = []
    steps = []
    if isinstance(data, dict):
        if 'name' in data.keys():
            recipe_name = data['name']
        if 'recipeIngredient' in data.keys():
            ingredients_list = [ing for ing in data['recipeIngredient'] if ing != '']
        if 'recipeInstructions' in data.keys():
            instructions = data['recipeInstructions']
            steps = []
            for i, step in enumerate(instructions):
                if isinstance(step, dict):
                    steps.append(step['text'])
                elif isinstance(step, str):
                    steps.append(step)
    elif isinstance(data, list):
        for i, step in enumerate(data):
            if isinstance(step, dict):
                recipe_name, ingredients_list, steps = recursive_json_explore(step)
            elif isinstance(step, str):
                steps.append(step)
    return recipe_name, ingredients_list, steps

def extract_url(string):
    try:
        return re.search("(?P<url>https?://[^\s]+)", string).group("url")
    except:
        return ''

def with_clickable_links(string):
    if not '<a href=' in string: #avoid duplicate
        url = extract_url(string)
        if url != '':
            return string.replace(url, "<a href='%s'>%s</a>" % (url, url))
    return string
    
def main():
    input_html1 = os.path.dirname(__file__) + '/Mes_Fiches/test_marmiton.html'
    input_html2 = os.path.dirname(__file__) + '/Mes_Fiches/test_marmiton2.html'
    # parser = MyHTMLParser()
    
    input_url1 = 'https://www.marmiton.org/recettes/recette_lasagnes-aux-courgettes-et-au-chevre_22798.aspx'
    input_url2 = 'https://www.marmiton.org/recettes/recette_liqueur-de-cerise_214911.aspx'
    input_url3 = 'https://www.elle.fr/Elle-a-Table/Recettes-de-cuisine/Tajine-de-poulet-aux-tomates-2034856'
    
    # marmiton_parser(html_file = input_html1)
    print(marmiton_parser(url = input_url3))

if __name__ == "__main__":
    main()
    # debug()