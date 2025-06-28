from parse import extract_ingredient_lines
from ingredient_mapper import IngredientMapper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

recipe_text = """
2 cups flour
1/2 cup sugar
1 tsp salt
3 large eggs
1 cup milk
1 tbsp olive oil
"""

ingredient_lines = extract_ingredient_lines(recipe_text)
mapper = IngredientMapper()
product_names = [mapper.process(line)['product'] for line in ingredient_lines]

driver = webdriver.Chrome()  # will add more options
#getting list into instacart search works currently
driver.get("https://www.instacart.com/")

input("Log in to Instacart in the browser window, then press Enter here...")

wait = WebDriverWait(driver, 10)

for product in product_names:
    print(f"Searching and adding: {product}")
    search_box = wait.until(EC.presence_of_element_located((By.ID, "search-bar-input")))
    search_box.clear()
    search_box.send_keys(product)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    try:
        add_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[text()='Add']]")
            )
        )
        add_button.click()
        print(f"Added {product} to cart.")
    except Exception as e:
        print(f"Could not add {product}: {e}")
    time.sleep(2)

print("All products processed. Review your cart in the browser.") 