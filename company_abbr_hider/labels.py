import re
from collections.abc import Iterable
from functools import lru_cache

import frappe


DISPLAY_DOCTYPES = ("Account", "Warehouse", "Cost Center")
DISPLAY_TITLE_FIELD = "custom_company_abbr_hider_title"
TITLE_FIELDS = {
	"Account": DISPLAY_TITLE_FIELD,
	"Warehouse": DISPLAY_TITLE_FIELD,
	"Cost Center": DISPLAY_TITLE_FIELD,
}

_SUFFIX_BOUNDARY = r"(?=$|[\s,;:/|)\]}\"'<])"


def get_company_abbreviations() -> list[str]:
	"""Return unique company abbreviations, longest first."""
	abbreviations = {
		str(abbr).strip()
		for abbr in frappe.get_all("Company", pluck="abbr")
		if abbr and str(abbr).strip()
	}
	return sorted(abbreviations, key=lambda value: (-len(value), value.casefold()))


@lru_cache(maxsize=32)
def _suffix_pattern(abbreviations: tuple[str, ...]) -> re.Pattern[str] | None:
	if not abbreviations:
		return None

	alternatives = "|".join(re.escape(abbreviation) for abbreviation in abbreviations)
	return re.compile(rf"\s-\s(?:{alternatives}){_SUFFIX_BOUNDARY}")


def strip_company_abbreviations(value, abbreviations: Iterable[str] | None = None):
	"""Remove verified company suffixes from display text without changing other values."""
	if not isinstance(value, str) or not value:
		return value

	values = abbreviations if abbreviations is not None else get_company_abbreviations()
	clean_abbreviations = tuple(
		sorted(
			{str(abbreviation).strip() for abbreviation in values if str(abbreviation).strip()},
			key=lambda item: (-len(item), item.casefold()),
		)
	)
	pattern = _suffix_pattern(clean_abbreviations)
	return pattern.sub("", value) if pattern else value
