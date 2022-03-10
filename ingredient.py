

class Ingredient:
    def __init__(self, name="", qty=-1, unit="", is_optional=False) -> None:
        self.name = name
        self.is_optional = is_optional
        if len(name) > 0:
            if (name[0] == '(' or name[0] == '[') and (name[-1] == ')' or name[-1] == ']'):
                self.name = name[1:-1]
                self.is_optional = True
        
        try:
            self.qty = float(qty)
        except:
            print('wrong qty value for %s' % self.name)
            self.qty = -1
        self.unit = unit
        if self.unit == '()':
            self.unit = ''
        
        self.mixed_qty = '' #when mixing different units
    
    def __add__(self, other):
        if self == other:
            if self.unit == other.unit:
                qty = self.qty + other.qty
                return Ingredient(self.name, qty, self.unit)
            else:#TODO implement conversion functions
                print('conversion needed to add %s and %s' % (self, other))
                mixed_ing = Ingredient(self.name)
                mixed_ing.mixed_qty = '%f%s + %f%s' % (self.qty, self.unit, other.qty, other.unit)
                return mixed_ing
                # return [self, other]
        else:
            print('Unable to add apples and oranges ! (%s and %s)' % (self, other))
            return [self, other]
    
    def __eq__(self, other):
        if isinstance(other, Ingredient):
            self_name = self.name.lower()
            other_name = other.name.lower()
            if self_name[-1] == 's':
                self_name = self_name[:-1]
            if other_name[-1] == 's':
                other_name = other_name[:-1]
            return self_name == other_name

        return False

    def __str__(self) -> str:
        output = self.name
        if self.mixed_qty != '':
            output += ' (%s)' % self.mixed_qty
        elif self.qty != -1 and self.qty != 0:
            output += ' (%.1f%s)' % (self.qty, self.unit)
        return output

    def get_generic_version(self):
        #will be enhanced with image
        return Ingredient(self.name)


def debug():
    ing = Ingredient('patate', 2, 'kg')
    ing2 = Ingredient('patates', 3, 'kg')
    print(ing+ing2)

if __name__ == "__main__":
    debug()