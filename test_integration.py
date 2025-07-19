import pytest
from parse import extract_ingredient_lines
from ingredient_mapper import IngredientMapper

class TestIntegration:
    def setup_method(self):
        """Set up mapper for integration tests"""
        self.mapper = IngredientMapper()

    def test_full_workflow_pancake_recipe(self):
        """Test complete workflow with a pancake recipe"""
        recipe_text = """
        Pancake Recipe
        
        2 cups flour
        1/2 cup sugar
        1 tsp salt
        3 large eggs
        1 cup milk
        1 tbsp olive oil
        
        Mix all ingredients and cook on a skillet.
        """
        
        # Step 1: Extract ingredient lines
        ingredient_lines = extract_ingredient_lines(recipe_text)
        expected_lines = ["2 cups flour", "1/2 cup sugar", "1 tsp salt", "3 large eggs", "1 cup milk", "1 tbsp olive oil"]
        assert ingredient_lines == expected_lines
        
        # Step 2: Map each ingredient to a product
        products = []
        for line in ingredient_lines:
            result = self.mapper.process(line)
            products.append(result["product"])
        
        # Step 3: Verify expected products
        expected_products = [
            "All-Purpose Flour",
            "Granulated Sugar", 
            "Kosher Salt",
            "Large Eggs",
            "Whole Milk",
            "Extra Virgin Olive Oil"
        ]
        assert products == expected_products

    def test_full_workflow_cookie_recipe(self):
        """Test complete workflow with a cookie recipe"""
        recipe_text = """
        Chocolate Chip Cookies
        
        2-1/4 cups flour
        1 cup brown sugar
        1/2 cup butter
        2 eggs
        1 tsp vanilla
        1 tsp baking soda
        """
        
        # Extract and map
        ingredient_lines = extract_ingredient_lines(recipe_text)
        products = []
        for line in ingredient_lines:
            result = self.mapper.process(line)
            products.append(result["product"])
        
        # Should have 6 products
        assert len(products) == 6
        assert "All-Purpose Flour" in products
        assert "Brown Sugar" in products
        assert "Unsalted Butter" in products
        assert "Large Eggs" in products
        assert "Pure Vanilla Extract" in products
        assert "Baking Soda" in products

    def test_workflow_with_unknown_ingredients(self):
        """Test workflow when some ingredients aren't in the mapping"""
        recipe_text = """
        Exotic Recipe
        
        1 cup quinoa
        2 tbsp coconut oil
        1 tsp turmeric
        """
        
        ingredient_lines = extract_ingredient_lines(recipe_text)
        products = []
        for line in ingredient_lines:
            result = self.mapper.process(line)
            products.append(result["product"])
        
        # Unknown ingredients should return as-is
        assert "quinoa" in products  # Not in mapping, so returns original
        assert "coconut oil" in products  # Not in mapping
        assert "turmeric" in products  # Not in mapping

    def test_workflow_empty_recipe(self):
        """Test workflow with empty recipe"""
        recipe_text = ""
        
        ingredient_lines = extract_ingredient_lines(recipe_text)
        assert ingredient_lines == []
        
        products = []
        for line in ingredient_lines:
            result = self.mapper.process(line)
            products.append(result["product"])
        
        assert products == []

    def test_workflow_recipe_with_only_instructions(self):
        """Test workflow with recipe that has no ingredients"""
        recipe_text = """
        Simple Instructions
        
        Mix everything together.
        Cook until done.
        Serve immediately.
        """
        
        ingredient_lines = extract_ingredient_lines(recipe_text)
        assert ingredient_lines == []
        
        products = []
        for line in ingredient_lines:
            result = self.mapper.process(line)
            products.append(result["product"])
        
        assert products == []

    def test_workflow_quantity_parsing_accuracy(self):
        """Test that quantities are parsed correctly through the workflow"""
        recipe_text = """
        1/4 cup flour
        1-1/2 cups sugar
        2.5 tsp salt
        """
        
        ingredient_lines = extract_ingredient_lines(recipe_text)
        results = []
        for line in ingredient_lines:
            result = self.mapper.process(line)
            results.append(result)
        
        # Check quantities are parsed correctly
        assert results[0]["quantity"] == "1/4"
        assert results[0]["unit"] == "cup"
        assert results[0]["ingredient"] == "flour"
        
        assert results[1]["quantity"] == "1-1/2"
        assert results[1]["unit"] == "cups"
        assert results[1]["ingredient"] == "sugar"
        
        assert results[2]["quantity"] == "2.5"
        assert results[2]["unit"] == "tsp"
        assert results[2]["ingredient"] == "salt" 