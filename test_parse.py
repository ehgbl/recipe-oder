import pytest
from parse import extract_ingredient_lines

class TestParse:
    def test_extract_ingredient_lines_basic(self):
        """Test basic ingredient extraction"""
        recipe = """
        2 cups flour
        1/2 cup sugar
        1 tsp salt
        """
        result = extract_ingredient_lines(recipe)
        expected = ["2 cups flour", "1/2 cup sugar", "1 tsp salt"]
        assert result == expected

    def test_extract_ingredient_lines_with_instructions(self):
        """Test extraction when recipe has instructions mixed in"""
        recipe = """
        Pancake Recipe
        
        2 cups flour
        1/2 cup sugar
        Mix ingredients together
        1 tsp salt
        Cook on skillet
        """
        result = extract_ingredient_lines(recipe)
        expected = ["2 cups flour", "1/2 cup sugar", "1 tsp salt"]
        assert result == expected

    def test_extract_ingredient_lines_with_words(self):
        """Test extraction with word numbers"""
        recipe = """
        one cup milk
        two large eggs
        three tbsp oil
        """
        result = extract_ingredient_lines(recipe)
        expected = ["one cup milk", "two large eggs", "three tbsp oil"]
        assert result == expected

    def test_extract_ingredient_lines_empty(self):
        """Test with empty recipe"""
        recipe = ""
        result = extract_ingredient_lines(recipe)
        assert result == []

    def test_extract_ingredient_lines_no_ingredients(self):
        """Test with recipe that has no ingredient lines"""
        recipe = """
        Mix all ingredients together.
        Cook until done.
        Serve hot.
        """
        result = extract_ingredient_lines(recipe)
        assert result == []

    def test_extract_ingredient_lines_complex_fractions(self):
        """Test with complex fractions and measurements"""
        recipe = """
        1-1/2 cups flour
        3/4 cup sugar
        1.5 tsp salt
        2-3 tbsp oil
        """
        result = extract_ingredient_lines(recipe)
        expected = ["1-1/2 cups flour", "3/4 cup sugar", "1.5 tsp salt", "2-3 tbsp oil"]
        assert result == expected 