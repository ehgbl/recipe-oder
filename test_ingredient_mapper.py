import pytest
from ingredient_mapper import IngredientMapper

class TestIngredientMapper:
    def setup_method(self):
        """Set up a fresh mapper for each test"""
        self.mapper = IngredientMapper()

    def test_parse_line_basic(self):
        """Test basic ingredient line parsing"""
        line = "2 cups flour"
        qty, unit, ingredient = self.mapper.parse_line(line)
        assert qty == "2"
        assert unit == "cups"
        assert ingredient == "flour"

    def test_parse_line_fraction(self):
        """Test parsing with fractions"""
        line = "1/2 cup sugar"
        qty, unit, ingredient = self.mapper.parse_line(line)
        assert qty == "1/2"
        assert unit == "cup"
        assert ingredient == "sugar"

    def test_parse_line_no_unit(self):
        """Test parsing when no unit is specified"""
        line = "3 eggs"
        qty, unit, ingredient = self.mapper.parse_line(line)
        assert qty == "3"
        assert unit == ""
        assert ingredient == "eggs"

    def test_parse_line_complex_quantity(self):
        """Test parsing complex quantities"""
        line = "1-1/2 cups milk"
        qty, unit, ingredient = self.mapper.parse_line(line)
        assert qty == "1-1/2"
        assert unit == "cups"
        assert ingredient == "milk"

    def test_find_product_exact_match(self):
        """Test finding product with exact match"""
        result = self.mapper.find_product("flour")
        assert result == "All-Purpose Flour"

    def test_find_product_partial_match(self):
        """Test finding product with partial match"""
        result = self.mapper.find_product("all purpose flour")
        assert result == "All-Purpose Flour"

    def test_find_product_no_match(self):
        """Test when no product match is found"""
        result = self.mapper.find_product("unicorn meat")
        assert result == "unicorn meat"  # Returns original if no match

    def test_find_product_removes_descriptors(self):
        """Test that descriptors like 'large' are removed"""
        result = self.mapper.find_product("large eggs")
        assert result == "Large Eggs"

    def test_process_complete_line(self):
        """Test processing a complete ingredient line"""
        line = "2 cups flour"
        result = self.mapper.process(line)
        
        assert result["original"] == "2 cups flour"
        assert result["quantity"] == "2"
        assert result["unit"] == "cups"
        assert result["ingredient"] == "flour"
        assert result["product"] == "All-Purpose Flour"

    def test_process_multiple_ingredients(self):
        """Test processing multiple ingredient lines"""
        lines = [
            "2 cups flour",
            "1/2 cup sugar",
            "1 tsp salt"
        ]
        
        results = [self.mapper.process(line) for line in lines]
        
        assert results[0]["product"] == "All-Purpose Flour"
        assert results[1]["product"] == "Granulated Sugar"
        assert results[2]["product"] == "Kosher Salt"

    def test_process_edge_cases(self):
        """Test edge cases in processing"""
        # Empty line
        result = self.mapper.process("")
        assert result["original"] == ""
        assert result["quantity"] == ""
        assert result["unit"] == ""
        assert result["ingredient"] == ""
        
        # Line with only ingredient
        result = self.mapper.process("salt")
        assert result["original"] == "salt"
        assert result["quantity"] == ""
        assert result["unit"] == ""
        assert result["ingredient"] == "salt" 