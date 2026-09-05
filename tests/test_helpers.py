"""
Unit tests for the helpers module.

Tests cover:
- ID generation
- Timestamp generation
- Text formatting
- Text capitalization
- Text truncation
- Empty/None checking
"""

import unittest
from app.utils.helpers import (
    generate_unique_id,
    get_current_timestamp,
    format_text,
    capitalize_words,
    truncate_text,
    is_empty_or_none,
)


class TestIdGeneration(unittest.TestCase):
    """Test ID generation functionality."""
    
    def test_generate_unique_id_returns_string(self):
        """Generated ID should be a string."""
        uid = generate_unique_id()
        self.assertIsInstance(uid, str)
    
    def test_generate_unique_id_is_not_empty(self):
        """Generated ID should not be empty."""
        uid = generate_unique_id()
        self.assertTrue(len(uid) > 0)
    
    def test_generate_unique_id_is_unique(self):
        """Generated IDs should be unique."""
        id1 = generate_unique_id()
        id2 = generate_unique_id()
        self.assertNotEqual(id1, id2)


class TestTimestampGeneration(unittest.TestCase):
    """Test timestamp generation functionality."""
    
    def test_get_current_timestamp_returns_string(self):
        """Timestamp should be a string."""
        ts = get_current_timestamp()
        self.assertIsInstance(ts, str)
    
    def test_get_current_timestamp_is_not_empty(self):
        """Timestamp should not be empty."""
        ts = get_current_timestamp()
        self.assertTrue(len(ts) > 0)
    
    def test_get_current_timestamp_format(self):
        """Timestamp should follow expected format."""
        ts = get_current_timestamp()
        # Check if it matches YYYY-MM-DD HH:MM:SS format
        parts = ts.split()
        self.assertEqual(len(parts), 2)
        self.assertIn("-", parts[0])
        self.assertIn(":", parts[1])


class TestTextFormatting(unittest.TestCase):
    """Test text formatting functionality."""
    
    def test_format_text_with_normal_text(self):
        """Text formatting should lowercase and strip whitespace."""
        result = format_text("  Hello World  ")
        self.assertEqual(result, "hello world")
    
    def test_format_text_with_already_formatted(self):
        """Already formatted text should remain unchanged."""
        result = format_text("hello")
        self.assertEqual(result, "hello")
    
    def test_format_text_with_uppercase(self):
        """Formatting should convert to lowercase."""
        result = format_text("HELLO")
        self.assertEqual(result, "hello")
    
    def test_format_text_with_non_string(self):
        """Non-string values should be returned as-is."""
        result = format_text(123)
        self.assertEqual(result, 123)


class TestCapitalizeWords(unittest.TestCase):
    """Test word capitalization functionality."""
    
    def test_capitalize_words_with_multiple_words(self):
        """Each word should be capitalized."""
        result = capitalize_words("john doe")
        self.assertEqual(result, "John Doe")
    
    def test_capitalize_words_with_single_word(self):
        """Single word should be capitalized."""
        result = capitalize_words("hello")
        self.assertEqual(result, "Hello")
    
    def test_capitalize_words_with_already_capitalized(self):
        """Already capitalized text should remain unchanged."""
        result = capitalize_words("John Doe")
        self.assertEqual(result, "John Doe")
    
    def test_capitalize_words_with_non_string(self):
        """Non-string values should be returned as-is."""
        result = capitalize_words(123)
        self.assertEqual(result, 123)


class TestTruncateText(unittest.TestCase):
    """Test text truncation functionality."""
    
    def test_truncate_text_within_limit(self):
        """Text within limit should not be truncated."""
        result = truncate_text("hello", max_length=10)
        self.assertEqual(result, "hello")
    
    def test_truncate_text_exceeds_limit(self):
        """Text exceeding limit should be truncated with ellipsis."""
        result = truncate_text("hello world", max_length=5)
        self.assertEqual(result, "hello...")
    
    def test_truncate_text_default_max_length(self):
        """Default max length should be 100."""
        long_text = "x" * 150
        result = truncate_text(long_text)
        self.assertTrue(result.endswith("..."))
        self.assertTrue(len(result) <= 103)  # 100 + "..."
    
    def test_truncate_text_with_non_string(self):
        """Non-string values should be returned as-is."""
        result = truncate_text(123, max_length=10)
        self.assertEqual(result, 123)


class TestEmptyOrNoneCheck(unittest.TestCase):
    """Test empty or None checking functionality."""
    
    def test_is_empty_or_none_with_none(self):
        """None should be considered empty."""
        self.assertTrue(is_empty_or_none(None))
    
    def test_is_empty_or_none_with_empty_string(self):
        """Empty string should be considered empty."""
        self.assertTrue(is_empty_or_none(""))
    
    def test_is_empty_or_none_with_whitespace(self):
        """Whitespace-only string should be considered empty."""
        self.assertTrue(is_empty_or_none("   "))
        self.assertTrue(is_empty_or_none("\t\n"))
    
    def test_is_empty_or_none_with_valid_value(self):
        """Valid value should not be considered empty."""
        self.assertFalse(is_empty_or_none("hello"))
        self.assertFalse(is_empty_or_none("x"))
    
    def test_is_empty_or_none_with_zero(self):
        """Zero should not be considered empty (not a string)."""
        self.assertFalse(is_empty_or_none(0))
    
    def test_is_empty_or_none_with_false(self):
        """False should not be considered empty (not a string)."""
        self.assertFalse(is_empty_or_none(False))


if __name__ == "__main__":
    unittest.main()
