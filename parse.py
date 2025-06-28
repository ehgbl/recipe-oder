import regex as re 

def extract_ingredient_lines(recipe_text):
    """
    Extract lines that look like ingredients from a recipe text.
    Assumes each ingredient is on its own line, starting with a quantity (number, fraction, or word like 'one').
    """
    pattern = re.compile(r"^\s*(\d+[\/\d\s\.,-]*|one|two|three|four|five|six|seven|eight|nine|ten)\s+.+", re.IGNORECASE | re.MULTILINE)
    matches = pattern.findall(recipe_text)
    lines = [m.group(0).strip() for m in pattern.finditer(recipe_text)]
    return lines

if __name__ == "__main__":
    sample_recipe = """
    2 cups flour
    1/2 cup sugar
    1 tsp salt
    3 large eggs
    1 cup milk
    1 tbsp olive oil
    Mix all ingredients and cook on a skillet.
    """
    ingredients = extract_ingredient_lines(sample_recipe)
    print("Extracted ingredient lines:")
    for line in ingredients:
        print(line)
