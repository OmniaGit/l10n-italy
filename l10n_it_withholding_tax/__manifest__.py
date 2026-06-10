# Deprecated stub kept for the v16 -> v18 migration.
# Withholding tax ("Ritenuta d'acconto") is now handled by Odoo 18 core
# (l10n_it_edi_withholding + negative-amount taxes), confirmed by the
# customer. This empty module defines no models, views or data; it only
# preserves the installed-module record so the database upgrade does not
# uninstall it (which would drop its tables and the historical
# withholding records, keeping them as orphan data instead).
{
    "name": "ITA - Ritenute d'acconto (deprecated stub)",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Deprecated: withholding moved to Odoo 18 core "
    "(l10n_it_edi_withholding). Empty stub kept to preserve the module record.",
    "author": "OmniaSolutions",
    "website": "https://www.omniasolutions.eu",
    "license": "AGPL-3",
    "depends": ["account"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
