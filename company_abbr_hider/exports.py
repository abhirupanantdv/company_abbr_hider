from io import BytesIO

import frappe
from frappe import _

from company_abbr_hider.labels import get_company_abbreviations, strip_company_abbreviations


def sanitize_export_content(content: bytes, file_extension: str) -> bytes:
	abbreviations = get_company_abbreviations()
	if not abbreviations:
		return content

	if file_extension == "csv":
		return _sanitize_csv(content, abbreviations)
	if file_extension == "xlsx":
		return _sanitize_xlsx(content, abbreviations)
	return content


def _sanitize_csv(content: bytes, abbreviations: list[str]) -> bytes:
	has_bom = content.startswith(b"\xef\xbb\xbf")
	encoding = "utf-8-sig" if has_bom else "utf-8"
	text = content.decode(encoding)
	cleaned = strip_company_abbreviations(text, abbreviations)
	return cleaned.encode(encoding)


def _sanitize_xlsx(content: bytes, abbreviations: list[str]) -> bytes:
	from openpyxl import load_workbook

	workbook = load_workbook(BytesIO(content))
	for worksheet in workbook.worksheets:
		for row in worksheet.iter_rows():
			for cell in row:
				if isinstance(cell.value, str) and not cell.value.startswith("="):
					cell.value = strip_company_abbreviations(cell.value, abbreviations)

	output = BytesIO()
	workbook.save(output)
	return output.getvalue()


def _provide_clean_export(result):
	if not result:
		return None

	from frappe.desk.utils import provide_binary_file

	name, file_extension, content = result
	provide_binary_file(_(name), file_extension, content)


@frappe.whitelist()
def export_query_report():
	"""Export a query/script report with company suffixes removed from display values."""
	from frappe.desk import query_report
	from frappe.desk.utils import pop_csv_params

	form_params = frappe._dict(frappe.local.form_dict)
	csv_params = pop_csv_params(form_params)
	query_report.clean_params(form_params)
	query_report.parse_json(form_params)
	report_name = form_params.report_name
	frappe.permissions.can_export(
		frappe.get_cached_value("Report", report_name, "ref_doctype"),
		raise_exception=True,
	)

	if int(form_params.export_in_background or 0):
		user_email = frappe.get_cached_value("User", frappe.session.user, "email")
		frappe.enqueue(
			"company_abbr_hider.exports.run_query_report_export_job",
			user_email=user_email,
			form_params=form_params,
			csv_params=csv_params,
			queue="long",
			now=frappe.flags.in_test,
		)
		frappe.msgprint(
			_(
				"Your report is being generated in the background. You will receive an email on {0} with a download link once it is ready."
			).format(user_email)
		)
		return None

	result = _query_report_export(form_params, csv_params)
	return _provide_clean_export(result)


def _query_report_export(form_params, csv_params):
	from frappe.desk import query_report

	result = query_report._export_query(form_params, csv_params, populate_response=False)
	if not result:
		return None

	name, file_extension, content = result
	return name, file_extension, sanitize_export_content(content, file_extension)


def run_query_report_export_job(user_email: str, form_params, csv_params):
	from frappe.desk.utils import send_report_email

	result = _query_report_export(form_params, csv_params)
	if not result:
		return

	report_name, file_extension, content = result
	send_report_email(
		user_email,
		report_name,
		file_extension,
		content,
		attached_to_name=form_params.report_name,
	)


@frappe.whitelist()
@frappe.read_only()
def export_report_view():
	"""Export a Report Builder/list report with clean company-specific labels."""
	from frappe.desk import reportview
	from frappe.desk.utils import pop_csv_params

	form_params = reportview.get_form_params()
	form_params["limit_page_length"] = None
	form_params["as_list"] = True
	csv_params = pop_csv_params(form_params)
	export_in_background = int(form_params.pop("export_in_background", 0))

	if export_in_background:
		user_email = frappe.get_cached_value("User", frappe.session.user, "email")
		frappe.enqueue(
			"company_abbr_hider.exports.run_report_view_export_job",
			user_email=user_email,
			form_params=form_params,
			csv_params=csv_params,
			queue="long",
			now=frappe.flags.in_test,
		)
		frappe.msgprint(
			_(
				"Your report is being generated in the background. You will receive an email on {0} with a download link once it is ready."
			).format(user_email)
		)
		return None

	result = _report_view_export(form_params, csv_params)
	return _provide_clean_export(result)


def _report_view_export(form_params, csv_params):
	from frappe.desk import reportview

	result = reportview._export_query(form_params, csv_params, populate_response=False)
	if not result:
		return None

	name, file_extension, content = result
	return name, file_extension, sanitize_export_content(content, file_extension)


def run_report_view_export_job(user_email: str, form_params, csv_params):
	from frappe.desk.utils import send_report_email

	result = _report_view_export(form_params, csv_params)
	if not result:
		return

	report_name, file_extension, content = result
	send_report_email(user_email, report_name, file_extension, content, attached_to_name=report_name)
