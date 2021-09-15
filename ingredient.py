

class Ingredient:
    def __init__(self, ing_name="", ing_qty=-1, ing_qty_unit="", ing_is_optional=False) -> None:
        self.name = ing_name
        self.qty = ing_qty
        self.qty_unit = ing_qty_unit
        self.is_optional = ing_is_optional