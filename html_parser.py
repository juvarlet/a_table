from html.parser import HTMLParser
from html.entities import name2codepoint
import os
from bs4 import BeautifulSoup
import json
import urllib3

class MyHTMLParser(HTMLParser):
    def __init__(self, input_file = None):
        self.input_file = input_file
        
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)


# 1. option to include link to web page in recipe description (easy)
# 2. option to print page as pdf and display it/link to it in recipe (medium)
# 3. implement several famous website parsers (hard)

def marmiton_parser(url):
    
    soup = soup_from_url(url)
    
    #method 1
    # steps = soup.find_all('h3', class_ = "Stepsstyle__StepTitle-sc-1211b9i-1 laOcon")
    # steps_details = soup.find_all('p', class_ = "Stepsstyle__Text-sc-1211b9i-3 IhwQd")
    
    # for step, step_detail in zip(steps, steps_details):
    #     print('%s - %s' % (step.text, step_detail.text))
    
    #method 2 (from json)
    recipe_name, ingredients_list, steps = extract_from_json(soup)
    
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
    
    for script_content in soup.find_all('script'):
        if script_content.get('type') == 'application/ld+json':
            # print(test.string)
            data = json.loads(script_content.string)
            if isinstance(data, dict):
                if 'name' in data.keys():
                    recipe_name = data['name']
                    # print(recipe_name)
                if 'recipeIngredient' in data.keys():
                    ingredients_list = [ing for ing in data['recipeIngredient'] if ing != '']
                    # print(ingredients_list)
                if 'recipeInstructions' in data.keys():
                    # print(type(data['recipeInstructions']))
                    # steps = ['Étape %s - %s' % (str(i+1), step_dict['text']) for i, step_dict in enumerate(data['recipeInstructions'])]
                    # print(steps)
                    
                    instructions = data['recipeInstructions']
                    steps = []
                    for i, step in enumerate(instructions):
                        if isinstance(step, dict):
                            # steps.append('*Étape %s*\n%s' % (str(i+1), step['text']))
                            steps.append(step['text'])
                        elif isinstance(step, str):
                            # steps.append('*Étape %s*\n%s' % (str(i+1), step))
                            steps.append(step)
            elif isinstance(data, list):
                steps = data
                
    return recipe_name, ingredients_list, steps
    
    
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