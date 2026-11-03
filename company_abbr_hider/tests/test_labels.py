import unittest

from company_abbr_hider.labels import strip_company_abbreviations


class TestCompanyLabels(unittest.TestCase):
	def test_strips_verified_suffixes(self):
		abbreviations = ["PAF", "PAFL", "PWR"]
		self.assertEqual(strip_company_abbreviations("Stores - PAF", abbreviations), "Stores")
		self.assertEqual(strip_company_abbreviations("Sales - PAFL", abbreviations), "Sales")
		self.assertEqual(strip_company_abbreviations("Main - PWR", abbreviations), "Main")
		self.assertEqual(
			strip_company_abbreviations("0021-99 - ANZ EFTPOS Account - PAFL", abbreviations),
			"0021-99 - ANZ EFTPOS Account",
		)

	def test_handles_multiple_values_and_html(self):
		abbreviations = ["PAF", "PAFL"]
		value = '<a href="/Sales%20-%20PAF">Sales - PAF</a>, Cash - PAFL'
		self.assertEqual(
			strip_company_abbreviations(value, abbreviations),
			'<a href="/Sales%20-%20PAF">Sales</a>, Cash',
		)

	def test_preserves_unverified_text(self):
		abbreviations = ["PAF"]
		self.assertEqual(strip_company_abbreviations("PAF", abbreviations), "PAF")
		self.assertEqual(strip_company_abbreviations("Product - PAFCO", abbreviations), "Product - PAFCO")
		self.assertEqual(strip_company_abbreviations("Reference - XYZ", abbreviations), "Reference - XYZ")

	def test_prefers_longer_abbreviations(self):
		self.assertEqual(strip_company_abbreviations("Sales - PAFL", ["PAF", "PAFL"]), "Sales")
