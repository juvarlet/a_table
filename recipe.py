
class Recipe:
    def __init__(self, name, ingredients_list_qty = {}, preparation = '', time = 0, tags = [], image = ''):
        self.name = name
        self.ingredients_list_qty = ingredients_list_qty
        self.preparation = preparation
        self.time = time
        self.tags = tags
        self.image = image
    
    def isTagged(self, tag):
        try:
            return tag in self.tags
        except:
            return False
    
    def ingredients_string(self, my_recipe_db):
        string = ''
        string_option = '\nOptionnel :\n'
        options = False
        if self.ingredients_list_qty is not None:
            for ing, qty_unit in self.ingredients_list_qty.items():
                qty, unit = qty_unit
                if ing != '':
                    if ing[0] == '[' and ing[-1] == ']':
                        options = True
                        #include links
                        e_ing = my_recipe_db.find_links(ing[1:-1])
                        string_option += '- %s : %s' % (e_ing, qty)
                        if unit != '()':
                            string_option += unit
                        string_option += '\n'
                    else:
                        #include links
                        e_ing = my_recipe_db.find_links(ing)
                        string += '- %s : %s' % (e_ing, qty)
                        if unit != '()':
                            string += unit
                        string += '\n'
        if options:
            string += string_option
        
        if self.time is not None:
            string += '\nTemps de préparation : %s minutes' % self.time
        return string
    
    def ingredients_string_list(self):
        string_list = []
        string_option_list = ['', 'Optionnel :']

        if self.ingredients_list_qty is not None:
            for ing, qty_unit in self.ingredients_list_qty.items():
                qty, unit = qty_unit
                if ing != '':
                    if ing[0] == '[' and ing[-1] == ']':
                        string_option = '- %s : %s' % (ing[1:-1], qty)
                        if unit != '()':
                            string_option += unit
                        string_option_list.append(string_option)
                    else:
                        string = '- %s : %s' % (ing, qty)
                        if unit != '()':
                            string += unit
                        string_list.append(string)
        
        if len(string_option_list) > 2:
            string_list += string_option_list
        return string_list
    
    def hasIngredient(self, ingredient):
        try:
            if ingredient in self.ingredients_list_qty.keys():
                return True
            else:
                return False
        except:
            return False
    
    def meet_with_criteria(self, with_text):
        if with_text == '':
            return True
        else:
            meets = with_text in self.name.lower()
            if self.tags is not None:
                meets += with_text in list(map(str.lower, self.tags))
            if self.ingredients_list_qty is not None:
                meets += with_text in list(map(str.lower, self.ingredients_list_qty))
            if self.preparation is not None:
                meets += with_text in self.preparation.lower()
            return bool(meets)
    
    def meet_without_criteria(self, without_text):
        if without_text == '':
            return True
        return not self.meet_with_criteria(without_text)
    
    def toString_cells(self):
        cells = 6*[None]
        cells[0] = self.name
        
        # cells[1] = '/'.join(self.ingredients_string_list())
        if self.ingredients_list_qty is not None:
            ing_strings = []
            for ingredient, qty_unit in self.ingredients_list_qty.items():
                qty, unit = qty_unit
                ing_strings.append('%s,%s,%s' % (ingredient, qty, unit))
            
            cells[1] = '/'.join(ing_strings)
            
        cells[2] = self.preparation
        cells[3] = self.time
        if self.tags is not None:
            cells[4] = '/'.join(self.tags)
        cells[5] = self.image.split('/')[-1]
        
        return cells