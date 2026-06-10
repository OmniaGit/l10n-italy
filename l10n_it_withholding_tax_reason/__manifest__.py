# Deprecated stub kept for the v16 -> v18 migration.
# Withholding payment reasons ("Causali pagamento per ritenute") are now
# covered by Odoo 18 core withholding. This empty module preserves the
# installed-module record so the database upgrade does not uninstall it.
{
    "name": "ITA - Causali pagamento per ritenute d'acconto (deprecated stub)",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Deprecated: moved to Odoo 18 core. "
    "Empty stub kept to preserve the module record during migration.",
    "author": "OmniaSolutions",
    "website": "https://www.omniasolutions.eu",
    "license": "AGPL-3",
    "depends": ["l10n_it_withholding_tax", "l10n_it_payment_reason"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
