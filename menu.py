from datetime import datetime
from datetime import timedelta
import random
from ingredient import Ingredient
import recipe_db
from recipe import Recipe
import custom_widgets as cw
import os

class Menu:
    def __init__(self, start_day = datetime.now().date(), number_of_days = 7, table = [], options = [], desserts = [], shopping_list = {}):
        self.start_day: datetime
        self.start_day = start_day
        self.number_of_days = number_of_days
        self.table = table
        self.options = options
        self.desserts = desserts
        self.shopping_list = shopping_list

    def __str__(self):
        description = 'du %s' % self.start_day.strftime('%d_%m_%Y')
        description += ' au %s\n' % (self.start_day + timedelta(self.number_of_days)).strftime('%d_%m_%Y')
        for i, stack in enumerate(self.table):
            if type(stack) is Recipe:
                stack = [stack]
            recipes = ' | '.join([str(r) for r in stack])
            description += '%i-%s\n' % (i, recipes)

        return description

    def generate_random_menu(self, my_recipe_db):#basic random function
        length = self.number_of_days * 2
        self.table = random_sublist(my_recipe_db.recipe_list, length)
    
    #table = [recipe1lunch, recipe1dinner, recipe2lunch, recipe2dinner...]

    def use_double(self):
        #if 'double' tag found, leftovers are used within 2-3 days (only once)
        list_of_double = []
        for i, recipe in enumerate(self.table):
            if recipe.isTagged('double'):
                if not recipe.name in list_of_double:
                    try:#try to replace recipe 2 days after, only once, except when leftovers
                        if self.table[i+4].name != 'Restes':
                            self.table[i+4] = recipe
                            list_of_double.append(recipe.name)
                    except:
                        try:#if unsuccessful, try to replace 2 days before
                            self.table[i-4] = recipe
                            list_of_double.append(recipe.name)
                        except:#if still unsuccessful, do nothing
                            pass
    
    def generate_smart_menu(self, my_recipe_db, options = []):
        smart_table = []
        #remove 'dessert', 'leftovers', 'tips' from list
        smart_table = recipe_db.get_recipe_sublist(my_recipe_db.recipe_list, tagsOut = ['dessert', 'restes', 'tips'])
        #seasons
        y = self.start_day.year
        if datetime(y, 6, 1).date() <= self.start_day <= datetime(y, 10, 1).date():
            #summer -> remove winter tags
            smart_table = recipe_db.get_recipe_sublist(smart_table, tagsOut = ['hiver'])
        elif datetime(y, 12, 1).date() <= self.start_day or self.start_day <= datetime(y, 4, 1).date():
            #winter -> remove summer tags
            smart_table = recipe_db.get_recipe_sublist(smart_table, tagsOut = ['ete'])
        else:
            #out of winter and summer
            smart_table = recipe_db.get_recipe_sublist(smart_table, tagsOut = ['ete', 'hiver'])
        #generate randomly alternating lunch/dinner
        full_lunch_list = recipe_db.get_recipe_sublist(smart_table, tagsOut = ['soir'])
        lunch_list = random_sublist(full_lunch_list, self.number_of_days)
        full_dinner_list = recipe_db.get_recipe_sublist(smart_table, tagsOut = ['midi'])
        dinner_list = random_sublist(full_dinner_list, self.number_of_days)
        smart_table = [j for i in zip(lunch_list, dinner_list) for j in i]

        #option leftovers (last meal of table is 'leftovers')
        if 'leftovers' in options:
            smart_table[-1] = my_recipe_db.get_recipe_object('Restes')

        #assign this smart table to menu
        self.table = smart_table
    
    def generate_dessert_full_menu(self, my_recipe_db, number):
        full_dessert_list = recipe_db.get_recipe_sublist(my_recipe_db.recipe_list, tagsIn = ['dessert'])
        dessert_list = random_sublist(full_dessert_list, number)
        self.desserts = dessert_list
        return dessert_list
    
    def generate_smart_menu_v2(self, my_recipe_db, options = {}):
        #skip protected indexes defined in options
        table = generate_smart_menu_v2(my_recipe_db, self.start_day, self.number_of_days, options)
        if 'protected' in options:
            for idx in options['protected']:
                #replace with protected recipes
                table[idx] = self.table[idx]
        # self.table = generate_smart_menu_v2(my_recipe_db, self.start_day, self.number_of_days, options)
        self.table = list(table)

    def full_menu(self):
        full_menu = []
        if len(self.table) == self.number_of_days * 2: #table has been generated correctly
            for i in range(self.number_of_days):
                day = (self.start_day + timedelta(i))
                #short french version of day
                day_str = toFrench(day.strftime('%A'))[:2] + day.strftime(' %d/%m')
                full_menu.append([day_str, self.table[2*i], self.table[2*i+1]])
        
        return full_menu
    
    #full_menu = [[day1, recipe1lunch, recipe1dinner], [day2, recipe2lunch, recipe2dinner], ...]
    #table = full_menu[0][1], full_menu[0][2], full_menu[1][1], full_menu[1][2], ...

    def get_recipe_list(self, no_double=False):
        recipe_list = recipe_db.extract_recipes(self.table + self.desserts)
        if no_double:
            recipe_list = list(dict.fromkeys(recipe_list))
        return recipe_list
      
    def tag_score(self, tag):
        score = 0
        for recipe in recipe_db.extract_recipes(self.table):
            if recipe.isTagged(tag):
                score += 1
        #percentage with number of recipes
        max = len(self.table) - ('leftovers' in self.options)
        score_8 = int(score / max * 8)
        return score_8
    
    def to_day(self):
        return self.start_day + timedelta(days = self.number_of_days - 1)
    
    def get_shopping_list(self): #TODO return list of string with ingredients and qty with units converted when needed
        shopping_list = {}
        shopping_list['missing information'] = []
        
        #count recipe once when tagged double (appears twice in table)
        recipe_double = []
        missing_recipe_double = []
        recipe_list = self.get_recipe_list()
        for recipe in recipe_list:
            
            if len(recipe.ing_list) > 0:
                if recipe.name not in recipe_double:
                    recipe_double.append(recipe.name)

                    for ingredient in recipe.ing_list:
                        qty = ingredient.qty
                        unit = ingredient.unit
                        if not ingredient.name in shopping_list:
                            shopping_list[ingredient.name] = ingredient
                            
                        else:
                            shopping_list[ingredient.name] += ingredient
            else:
                if recipe.name not in missing_recipe_double:
                    missing_recipe_double.append(recipe.name)
                    shopping_list['missing information'].append(recipe.name)

        self.shopping_list = shopping_list
        return shopping_list
    
    def update(self, my_recipe_db, number_of_days = 0, table = [], options = [], desserts = []):
        diff = number_of_days - self.number_of_days
        adding = diff > 0
        # print(len(self.table))
        if adding:
            additional_menu = generate_smart_menu_v2(my_recipe_db, self.start_day + timedelta(self.number_of_days + 1), diff)
            self.table += additional_menu
        else:
            self.table = self.table[:-(abs(diff)*2)]
        # print('from %s to %s' % (self.number_of_days, number_of_days))
        # print(len(self.table))
        # print([recipe.name for recipe in self.table])
        self.number_of_days = number_of_days
                    
    
    # def toHtml(self, html_source_file):
    #     #create email body in HTML containing full menu and shopping list
    #     '''
    #     [TITLE]
    #     [ICON_MENU_PATH] #to be replaced within GUI class
    #     [TABLE_DAYS]
    #     [TABLE_MENUS_LUNCH]
    #     [TABLE_MENUS_DINNER]
    #     [TABLE_MENUS_DESSERTS]
    #     [ICON_SHOPPING_PATH] #to be replaced within GUI class
    #     [INGREDIENTS]
    #     [OPTIONS]
    #     [ICON_TABLE_PATH] #to be replaced within GUI class
    #     '''
    #     from_day_str = full_date_to_french(self.start_day)
    #     to_day = self.start_day + timedelta(days = self.number_of_days - 1)
    #     to_day_str = full_date_to_french(to_day)
    #     TITLE = 'du %s au %s' % (from_day_str, to_day_str)
    #     subject = 'Nouveaux menus (%s-%s)' % (self.start_day.strftime('%d/%m/%Y'), to_day.strftime('%d/%m/%Y'))

    #     table_days = '<td style="width: 12.5%; text-align: center;"><span style="color: #5c3c92;"><strong>[DAY]</strong></span></td>'
    #     table_menus = '<td style="width: 12.5%; text-align: center;"><span style="color: #077b8a;">[MENU]</span></td>'
        
    #     TABLE_DAYS = ''
    #     TABLE_MENUS_LUNCH = ''
    #     TABLE_MENUS_DINNER = ''
    #     TABLE_MENUS_DESSERTS = ''

    #     for col in self.full_menu():
    #         day_str, lunch_recipe, dinner_recipe = col
    #         lunch_str = lunch_recipe.name
    #         dinner_str = dinner_recipe.name

    #         TABLE_DAYS += table_days.replace('[DAY]', day_str)
    #         TABLE_MENUS_LUNCH += table_menus.replace('[MENU]', lunch_str)
    #         TABLE_MENUS_DINNER += table_menus.replace('[MENU]', dinner_str)
        
    #     for dessert in self.desserts:
    #         dessert_str = dessert.name

    #         TABLE_MENUS_DESSERTS += table_menus.replace('[MENU]', dessert_str)

    #     ingredients = '<li>[ING]</li>'
    #     table_style = '<table style="background: #a2d5c6;" width="450" cellspacing="0" cellpadding="4" bgcolor="#a2d5c6"><tbody><tr style="background: transparent;"><td style="border: 1.30pt solid #077b8a; padding: 0.1cm;" valign="top" width="470">'
    #     table_style_ = '</td></tr></tbody></table>'
    #     options_html = '<li>[ING]</li>'

    #     INGREDIENTS = ''
    #     OPTIONS = ''

    #     options = []
    #     missing = []
    #     for ingredient, qty_unit in self.get_shopping_list().items():
    #         if ingredient != 'missing information':
    #             string = ''
    #             string_option = ''
    #             qty, unit = qty_unit
    #             if ingredient[0] == '[' and ingredient[-1] == ']':
    #                 string_option += '%s : %s' % (ingredient, qty)
    #                 if unit != '()':
    #                     string_option += unit
    #                 options.append(string_option)
    #             else:
    #                 string += '%s : %s' % (ingredient, qty)
    #                 if unit != '()':
    #                     string += unit
    #                 INGREDIENTS += ingredients.replace('[ING]', string)
    #         else:
    #             missing.append(qty_unit) #in that case qty_unit is recipe name
        
    #     if len(options) > 0:
    #         OPTIONS += '<p><span style="color: #077b8a; font-size: large;"><strong>Optionnel :</strong></span></p>%s<ul>' % table_style
    #         for option in options:
    #             OPTIONS += options_html.replace('[ING]', option)
    #         OPTIONS += '</ul>' + table_style_
        
    #     if len(missing) > 0:
    #         OPTIONS += '<p><span style="color: #077b8a; font-size: large;"><strong>Ingr&eacute;dients manquants pour :</strong></span></p>%s<ul>' % table_style
    #         for recipe_name in missing[0]:
    #             OPTIONS += options_html.replace('[ING]', recipe_name)
    #         OPTIONS += '</ul>%s<p>&nbsp;</p>' % table_style_
        
    #     with open(html_source_file, 'r') as f:
    #         data = f.readlines()
        
    #     core_text = ''.join(map(str.strip, data))

    #     rep = {'[TITLE]': TITLE} #define desired replacements here
    #     rep['[TABLE_DAYS]'] = TABLE_DAYS
    #     rep['[TABLE_MENUS_LUNCH]'] = TABLE_MENUS_LUNCH
    #     rep['[TABLE_MENUS_DINNER]'] = TABLE_MENUS_DINNER
    #     rep['[TABLE_MENUS_DESSERTS]'] = TABLE_MENUS_DESSERTS
    #     rep['[INGREDIENTS]'] = INGREDIENTS
    #     rep['[OPTIONS]'] = OPTIONS
        
    #     text = replace_multiple(core_text, rep)

    #     return subject, text

def toFrench(daymonth):
    english = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    english += ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    french = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    french += ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    index = english.index(daymonth)
    return french[index]

def full_date_to_french(date):
    return toFrench(date.strftime('%A')) + date.strftime(' %d ') + toFrench(date.strftime('%B'))

def random_sublist(recipe_list, length):
    random_table = []
    if len(recipe_list) > 0:
        while len(random_table) < (length):
            if len(recipe_list) < length:
                random_table += random.sample(recipe_list, len(recipe_list))
            else:
                random_table += random.sample(recipe_list, length)
    return random_table

def unit_conversion(from_unit, to_unit, value):
    to_mL = {'c. à c.': 5, 'c. à s.': 15}
    converted_value = None
    if to_unit.lower() == 'ml':
        if from_unit in to_mL:
            converted_value = int(value * to_mL[from_unit])
    
    if from_unit.lower() == 'ml':
        if to_unit in to_mL:
            converted_value = int(value / to_mL[to_unit])
    return converted_value

# def replace_multiple(string, from_to_dict):
#     # use these three lines to do the replacement
#     rep = dict((re.escape(k), v) for k, v in from_to_dict.items()) 
#     pattern = re.compile("|".join(rep.keys()))
#     text = pattern.sub(lambda m: rep[re.escape(m.group(0))], string)
#     return text

def generate_smart_menu_v2(my_recipe_db, start_day, number_of_days, options = {}, tagsOUt = ['dessert', 'restes', 'tips']):
    initial_pool = []
    #remove 'dessert', 'leftovers', 'tips' from list
    initial_pool = recipe_db.get_recipe_sublist(my_recipe_db.recipe_list, tagsOut = tagsOUt)
    #seasons
    y = start_day.year
    if datetime(y, 6, 1).date() <= start_day <= datetime(y, 10, 1).date():
        #summer -> remove winter tags
        initial_pool = recipe_db.get_recipe_sublist(initial_pool, tagsOut = ['hiver'])
    elif datetime(y, 12, 1).date() <= start_day or start_day <= datetime(y, 4, 1).date():
        #winter -> remove summer tags
        initial_pool = recipe_db.get_recipe_sublist(initial_pool, tagsOut = ['ete'])
    else:
        #out of winter and summer
        initial_pool = recipe_db.get_recipe_sublist(initial_pool, tagsOut = ['ete', 'hiver'])
    
    initial_lunch_pool = recipe_db.get_recipe_sublist(initial_pool, tagsOut = ['soir'])
    initial_dinner_pool = recipe_db.get_recipe_sublist(initial_pool, tagsOut = ['midi'])

    super_lunch_pool = []
    for lunch in initial_lunch_pool:
        super_lunch_pool += my_recipe_db.background_score(lunch, start_day) * [lunch]
    
    lunch_list = number_of_days * [None]

    super_dinner_pool = []
    for dinner in initial_dinner_pool:
        super_dinner_pool += my_recipe_db.background_score(dinner, start_day) * [dinner]
    
    dinner_list = number_of_days * [None]

    for i, (lunch_slot, dinner_slot) in enumerate(zip(lunch_list, dinner_list)):
        # print(len(super_lunch_pool))
        if lunch_slot is None:
            #take random menu from pool
            lunch_list[i] = random.choice(super_lunch_pool)                
            #use double
            if lunch_list[i].isTagged('double') and (i+2) < len(lunch_list)-1:
                lunch_list[i+2] = lunch_list[i]

            #update pools
            super_lunch_pool = list(filter(lambda l: l != lunch_list[i], super_lunch_pool))
            super_dinner_pool = list(filter(lambda l: l != lunch_list[i], super_dinner_pool))
        
        if dinner_slot is None:
            #take random menu from pool
            dinner_list[i] = random.choice(super_dinner_pool)                
            #use double
            if dinner_list[i].isTagged('double') and (i+2) < len(dinner_list)-1:
                dinner_list[i+2] = dinner_list[i]

            #update pools
            super_lunch_pool = list(filter(lambda l: l != dinner_list[i], super_lunch_pool))
            super_dinner_pool = list(filter(lambda l: l != dinner_list[i], super_dinner_pool))

    if 'leftovers' in options:
        if options['leftovers']:
            dinner_list[-1] = my_recipe_db.get_recipe_object('Restes')

    smart_table = [j for i in zip(lunch_list, dinner_list) for j in i]
    #assign this smart table to menu
    return smart_table

def debug():
    dirname = cw.dirname('')
    input_recipe = dirname + '/MesRecettes.ods'
    input_history = dirname + '/Historique.ods'
    html_source_file = dirname + '/shopping_core.html'
    myRecipeDB = recipe_db.RecipeDB(input_recipe, input_history)
    my_menu = Menu()
    my_menu.generate_random_menu(myRecipeDB)
    # my_menu.generate_dessert_full_menu(myRecipeDB, 1)
    # my_menu.get_shopping_list()
    # print(my_menu.toHtml(html_source_file))
    
    print(recipe_db.extract_recipes(my_menu.table + [[my_menu.table[0]]]))

if __name__ == "__main__":
    debug()