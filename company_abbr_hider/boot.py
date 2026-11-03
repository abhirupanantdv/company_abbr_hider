from company_abbr_hider.labels import DISPLAY_DOCTYPES, get_company_abbreviations


def boot_session(bootinfo):
	bootinfo.company_abbr_hider = {
		"abbreviations": get_company_abbreviations(),
		"display_doctypes": DISPLAY_DOCTYPES,
	}
