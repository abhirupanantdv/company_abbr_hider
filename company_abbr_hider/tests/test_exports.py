import unittest
from io import BytesIO

from openpyxl import Workbook, load_workbook

from company_abbr_hider.exports import _sanitize_csv, _sanitize_xlsx


class TestCleanExports(unittest.TestCase):
	def test_csv_export_removes_suffixes(self):
		content = b'Account,Warehouse\r\n"Sales - PAF","Stores - PAFL"\r\n'
		cleaned = _sanitize_csv(content, ["PAF", "PAFL"])
		self.assertEqual(cleaned, b'Account,Warehouse\r\n"Sales","Stores"\r\n')

	def test_xlsx_export_removes_suffixes_and_preserves_formulas(self):
		workbook = Workbook()
		worksheet = workbook.active
		worksheet.append(["Account", "Warehouse", "Formula"])
		worksheet.append(["Sales - PAF", "Stores - PAFL", "=1+1"])
		input_file = BytesIO()
		workbook.save(input_file)

		cleaned = _sanitize_xlsx(input_file.getvalue(), ["PAF", "PAFL"])
		result = load_workbook(BytesIO(cleaned), data_only=False).active
		self.assertEqual(result["A2"].value, "Sales")
		self.assertEqual(result["B2"].value, "Stores")
		self.assertEqual(result["C2"].value, "=1+1")
