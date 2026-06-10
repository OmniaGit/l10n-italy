# Deprecated stub kept for the v16 -> v18 migration.
# Payment reasons ("Causali di pagamento") are now covered by Odoo 18
# core withholding (l10n_it_edi_withholding reason selection). This empty
# module preserves the installed-module record so the database upgrade
# does not uninstall it (keeping its records as orphan data instead).
{
    "name": "ITA - Causali di pagamento (deprecated stub)",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Deprecated: moved to Odoo 18 core. "
    "Empty stub kept to preserve the module record during migration.",
    "author": "OmniaSolutions",
    "website": "https://www.omniasolutions.eu",
    "license": "AGPL-3",
    "depends": ["l10n_it_account"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
