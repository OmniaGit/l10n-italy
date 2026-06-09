# Deprecated stub kept for the v16 -> v18 migration.
# Declaration of Intent ("Dichiarazione di intento") is now handled by
# Odoo 18 core (l10n_it_edi_doi). This empty module defines no models,
# views or data; it only preserves the installed-module record so the
# database upgrade does not uninstall it (which would drop its orphan
# tables/columns).
{
    "name": "ITA - Dichiarazione di intento (deprecated stub)",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Deprecated: declaration of intent moved to Odoo 18 core "
    "(l10n_it_edi_doi). Empty stub kept to preserve the module record.",
    "author": "OmniaSolutions",
    "website": "https://www.omniasolutions.eu",
    "license": "AGPL-3",
    "depends": ["account", "sale"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
