import re

class IngredientMapper:
    def __init__(self):
        # Map common ingredients to Instacart product names
        self.mapping = {
            # Basic baking items
            "flour": "All-Purpose Flour",
            "sugar": "Granulated Sugar", 
            "brown sugar": "Brown Sugar",
            "salt": "Kosher Salt",
            "eggs": "Large Eggs",
            "milk": "Whole Milk",
            "butter": "Unsalted Butter",
            "olive oil": "Extra Virgin Olive Oil",
            "vegetable oil": "Vegetable Oil",
            
            # Spices and extracts
            "pepper": "Black Pepper",
            "vanilla": "Pure Vanilla Extract",
            "baking powder": "Baking Powder",
            "baking soda": "Baking Soda",
            
            # Common produce
            "onion": "Yellow Onion",
            "garlic": "Fresh Garlic",
            "tomato": "Roma Tomatoes",
            "lettuce": "Iceberg Lettuce",
            "carrot": "Carrots",
            "apple": "Gala Apples",
            "banana": "Bananas",
        }
    
    def parse_line(self, line):
        """Split ingredient line into quantity, unit, ingredient"""
        line = line.strip()
        
        # Common units we see in recipes
        units = ["cup", "cups", "tbsp", "tsp", "oz", "lb", "large", "medium", "small"]
        
        # Try to match: number + unit + ingredient
        pattern = r"^(\d+[\/\d\s\.,-]*)\s+(" + "|".join(units) + r")\s+(.+)$"
        match = re.match(pattern, line, re.IGNORECASE)
        
        if match:
            return match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
        
        # Try just number + ingredient
        pattern2 = r"^(\d+[\/\d\s\.,-]*)\s+(.+)$"
        match2 = re.match(pattern2, line, re.IGNORECASE)
        if match2:
            return match2.group(1).strip(), "", match2.group(2).strip()
        
        # No quantity found
        return "", "", line
    
    def find_product(self, ingredient):
        """Find the best Instacart product for this ingredient"""
        ingredient = ingredient.lower().strip()
        
        # Remove common words that don't help
        for word in ["fresh", "large", "medium", "small", "whole"]:
            ingredient = ingredient.replace(word, "").strip()
        
        # Exact match
        if ingredient in self.mapping:
            return self.mapping[ingredient]
        
        # Partial match
        for key, product in self.mapping.items():
            if key in ingredient or ingredient in key:
                return product
        
        # No match found
        return ingredient
    
    def process(self, ingredient_line):
        """Process one ingredient line"""
        qty, unit, ingredient = self.parse_line(ingredient_line)
        product = self.find_product(ingredient)
        
        return {
            "original": ingredient_line,
            "quantity": qty,
            "unit": unit, 
            "ingredient": ingredient,
            "product": product
        }

# Test 
if __name__ == "__main__":
    mapper = IngredientMapper()
    
    test_ingredients = [
        "2 cups flour",
        "1/2 cup sugar", 
        "1 tsp salt",
        "3 large eggs",
        "1 cup milk",
        "1 tbsp olive oil"
    ]
    
    print("Ingredient Mapping:")
    print("-" * 40)
    
    for ingredient in test_ingredients:
        result = mapper.process(ingredient)
        print(f"{result['original']} -> {result['product']}")
        print(f"  {result['quantity']} {result['unit']} {result['ingredient']}")
        print() 