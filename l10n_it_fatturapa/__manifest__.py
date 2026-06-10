# Deprecated stub kept for the v16 -> v18 migration.
# E-invoicing (FatturaPA) is now handled by Odoo 18 core (l10n_it_edi) plus
# the OCA l10n_it_edi_extension, which migrates the historical data via its
# pre_init_hook.
#
# IMPORTANT: this stub deliberately has NO "excludes" key. The old v16
# l10n_it_fatturapa declared `excludes: l10n_it_edi`; that stale exclusion
# record blocked the upgrade because Odoo core l10n_it_edi auto-installs.
# Shipping this stub (with a clean manifest) makes update_list() refresh the
# module from the manifest and drop the obsolete exclusion, so l10n_it_edi
# can install. The stub stays "installed" so l10n_it_edi_extension's
# pre_init_hook still detects it and migrates the FatturaPA data.
{
    "name": "ITA - Fattura elettronica - Base (deprecated stub)",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Deprecated: e-invoicing moved to Odoo 18 core (l10n_it_edi). "
    "Empty stub kept to clear the obsolete exclusion and preserve the module record.",
    "author": "OmniaSolutions",
    "website": "https://www.omniasolutions.eu",
    "license": "AGPL-3",
    "depends": ["account"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
