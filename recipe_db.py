
from recipe import Recipe
from pandas_ods_reader import read_ods
from pandas import read_csv, read_excel, DataFrame, ExcelWriter
import pandas as pd
import os
from datetime import datetime
import csv


class RecipeDB:
    def __init__(self, recipe_file, history_file, recipe_list = [], background = {}, history = []):
        self.recipe_file = recipe_file
        self.history_file = history_file

        if os.path.isfile(recipe_file):
            self.recipe_list = read_recipe(recipe_file)
        if os.path.isfile(history_file):
            self.background, self.history = read_history(history_file)
        else:
            self.recipe_list = recipe_list
            self.background = background
            self.history = history
        
        # self.compute_background_score()
    
    # def compute_background_score(self):
    #     for recipe in self.recipe_list:
    #         if recipe.name in self.background:
    #             recipe.background_score = len(self.background[recipe.name])
    
    def get_recipe_object(self, recipe_name):
        try:
        # print([recipe.name for recipe in self.recipe_list])
            index_of_recipe = get_recipe_names(self.recipe_list).index(recipe_name)
            return self.recipe_list[index_of_recipe]
        except:
            print('! Recipe %s not in Database !' % recipe_name)
            return None
    
    def remove_recipe(self, recipe_name):
        if self.contains(recipe_name):
            self.recipe_list.remove(self.get_recipe_object(recipe_name))
            # print('successfully removed from DB :')
            # print(not self.contains(recipe_name))
        else:
            print('%s not found in DB' % recipe_name)
    
    def consider_history_update(self, new_history_appendix):
        for i, h in enumerate(new_history_appendix):
            if text_to_date(h[0]) > text_to_date(self.history[-1][0]):#append
                h.append(-1) #index to be inserted, end of list
            else:#find insertion and/or replacement
                for j, current_h in enumerate(self.history):
                    if text_to_date(h[0]) <= text_to_date(current_h[0]):
                        h.append(j) #index j to be replaced
                        break
        return new_history_appendix
    
    def update_history(self, new_history_appendix):
        # print('before update')
        # print(self.history)
        #new_history_appendix = self.consider_history_update(new_history_appendix)

        for h in new_history_appendix:
            date_text, lunch_recipe_name, dinner_recipe_name, index = h
            
            if index != -1:
                if date_text in [j[0] for j in self.history]:
                    self.history[index] = [self.history[index][0], lunch_recipe_name, dinner_recipe_name]
                    
                else:
                    self.history.insert(index, [date_text, lunch_recipe_name, dinner_recipe_name])
                
            else:
                self.history.append([date_text, lunch_recipe_name, dinner_recipe_name])
        # print('after update')
        # print(self.history)
        
        #update sheet
        write_history(self.history_file, 'Historique', self.history)
    
    def get_recipe_string_list(self):
        return [r.toString_cells() for r in self.recipe_list]
    
    def update_recipe_file(self):
        # print('update recipe file')
        write_recipe(self.recipe_file, self.get_recipe_string_list())
    

    def background_score(self, recipe_object, date):
        if recipe_object.name not in self.background:#max score, recipe not in history
            return 10
        else:

            self.background[recipe_object.name].sort()
            days_since_last_time = (date - self.background[recipe_object.name][-1]).days

            for (score, days) in [(i, 8 + 2*i) for i in range(10)]:
                if days_since_last_time < days:
                    return score
            return 10
    
    def find_links(self, ingredient):
        if ingredient.lower() in list(map(str.lower, get_recipe_names(self.recipe_list))):
            return "<a href='%s'>%s</a>" % (ingredient, ingredient)
        return ingredient

    def get_ingredients_units_list(self):
        ingredients_list = []
        units_list = []
        for recipe in self.recipe_list:
            if recipe.ingredients_list_qty is not None:
                for ing, qty_unit in recipe.ingredients_list_qty.items():
                    qty, unit = qty_unit
                    if ing != '':
                        if ing[0] == '[' and ing[-1] == ']':
                            ing = ing[1:-1]
                        if ing not in ingredients_list:
                            ingredients_list.append(ing)
                        if unit not in units_list:
                            units_list.append(unit)
        return sorted(ingredients_list, key=str.lower), sorted(units_list, key=str.lower)

    def contains(self, recipe_name):
        return recipe_name in get_recipe_names(self.recipe_list)

    
def get_recipe_sublist(recipe_list, tagsIn = [], tagsOut = []):
    # #1- remove tagsOut
    # sublist = list(recipe_list)
    # for recipe in sublist:
    #     for tag in tagsOut:
    #         if recipe.isTagged(tag):
    #             sublist.remove(recipe)


    # #2- include tagsIn only
    # for recipe in sublist:
    #     for tag in tagsIn:
    #         if not recipe.isTagged(tag):
    #             print(recipe.name)
    #             print(get_recipe_names(sublist))
    #             sublist.remove(recipe)
    # return sublist
    extract_list = []
    if tagsOut != []:
        extract_list = list(recipe_list)
        to_be_removed_list = get_recipe_sublist(recipe_list, tagsIn = tagsOut)
        for recipe in to_be_removed_list:
            extract_list.remove(recipe)

    if tagsIn != []:
        for tag in tagsIn:
            extract_list += [recipe for recipe in recipe_list if recipe.isTagged(tag)]

    # print(tagsIn, get_recipe_names(extract_list))
    return extract_list

def get_recipe_names(recipe_list = []):
    return [recipe.name for recipe in extract_recipes(recipe_list)]

def date_to_text(date_object):
    return date_object.strftime('%Y-%m-%d')

def text_to_date(date_text):
    return datetime.strptime(date_text, '%Y-%m-%d').date()

def read_recipe(input_csv):
    recipe_list = []
    #read input_csv file to extract list of recipes
    #load a sheet based on its name
    sheet_name = "Liste_Recettes"
    if input_csv[-4:] == '.ods':
        df = read_ods(input_csv, sheet_name)
    elif input_csv[-4:] in ['.xls', 'xlsx']:
        df = read_excel(input_csv, sheet_name)
    elif input_csv[-4:] in ['.csv']:
        df = read_csv(input_csv, sep=";")
    else:
        print('unsupported (yet) file format for %s' % input_csv)
        df = DataFrame()
    for row in df.itertuples(index=True, name=None):
        i, uid, name, ingredients_list_qty_cell, time_cell, tags_cell, image_cell, preparation = row
        ingredients_list_qty = cell_to_recipe_input(ingredients_list_qty_cell, 'dict')
        time = cell_to_recipe_input(time_cell, 'time')
        tags = cell_to_recipe_input(tags_cell, 'tags')
        image = ''
        if image_cell is not None and not pd.isna(image_cell):
            image = '/images/' + image_cell
        recipe_list.append(Recipe(uid, name, ingredients_list_qty, preparation, time, tags, image))
    return recipe_list

def cell_to_recipe_input(cell_value, recipe_input_type):
    recipe_input = None
    if cell_value is not None and cell_value != '' and not pd.isna(cell_value):
        if recipe_input_type == 'dict': #ingredients
            recipe_input = {}
            ingredients = cell_value.split('/')
            #iterate over ingredients
            for ingredient in ingredients:
                ingredient += ',1,()' #append default optional values to string
                name, qty, unit = ingredient.split(',')[:3]
                recipe_input[name] = [qty, unit]

        elif recipe_input_type == 'tags':
            recipe_input = cell_value.split('/')
        
        elif recipe_input_type == 'time':
            try:
                recipe_input = int(cell_value)
            except:
                # print('Wrong format for cell in column "Temps (mn)", must be an integer, "%s" instead' % cell_value)
                # print("Unexpected error:", sys.exc_info())
                recipe_input = None
    
    return recipe_input

def read_history(input_csv):
    background = {}
    history = []
    if os.path.isfile(input_csv):
        sheet_name = 'Historique'
        if input_csv[-4:] == '.ods':
            df = read_ods(input_csv, sheet_name)
        elif input_csv[-4:] in ['.xls', 'xlsx']:
            df = read_excel(input_csv, sheet_name)
        elif input_csv[-4:] == '.csv':
            df = read_csv(input_csv, delimiter=";")
        else:
            print('unsupported (yet) file format for %s' % input_csv)
            df = DataFrame()
        #iterate over rows
        # print(df)
        for row in df.itertuples(index=True, name=None):
            i, date, recipe_name = row[:3]

            if not recipe_name in background:
                background[recipe_name] = []
            background[recipe_name].append(datetime.strptime(date, '%Y-%m-%d').date())

            if i % 2 == 0:
                history.append([date, recipe_name])
            else:
                history[int((i-1)/2)].append(recipe_name)

    return background, history

def write_history(input_csv, sheet_name, input_list):
    df = DataFrame()
    for h in input_list:#output_list should be self.history
        date, lunch, dinner = h
        df = df.append([[date, lunch]], ignore_index=True)
        df = df.append([[date, dinner]], ignore_index=True)
    df = df.set_axis(['Date', 'Recette'], axis='columns')
    if input_csv[-4:] == '.csv':
        df.to_csv(input_csv, sep=';', index=False)
    else:
        with ExcelWriter(input_csv) as writer:
            df.to_excel(writer, sheet_name = sheet_name, index = False)


def write_recipe(input_csv, input_list, sheet_name=""):
    df = DataFrame()
    for r in input_list:
        # name, ingredients, preparation, time, tags, image = r
        df = df.append([r], ignore_index=True)
    
    df = df.set_axis(['UID', 'Nom', 'Ingredients (nom,qty,unit/...)', 'Temps (mn)', 'Tags', 'Image', 'Preparation'], axis = 'columns')
    if input_csv[-4:] == '.csv':
        df.to_csv(input_csv, sep=';', index=False)
    else:
        with ExcelWriter(input_csv) as writer:
            df.to_excel(writer, sheet_name = sheet_name, index = False)

def extract_recipes(initial_list):
    recipe_list = []
    for element in initial_list:
        if type(element) == Recipe:
            recipe_list.append(element)
        elif type(element) == list:
            recipe_list = recipe_list + extract_recipes(element)
    return recipe_list

def debug():
    input_csv = '/home/jv/Documents/MyScripts/VSCODE/PY/Recipe/MesRecettes.ods'
    myRecipeDB = RecipeDB(input_csv)
    print(myRecipeDB.get_recipe_object('Omelette').name)

    # b = full_background(input_csv)
    # print(b)

if __name__ == "__main__":
    debug()