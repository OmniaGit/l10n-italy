# Copyright 2026 OmniaSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
# v16 -> v18 migration helper. Runs before l10n_it_account loads its own
# views (and before later modules such as plm_license_management), so it can
# neutralise stale views that would otherwise break view validation during
# the upgrade build. It only ARCHIVES views (active = false) - nothing is
# deleted and no business data is touched, so everything is recoverable.
#
# Two cases are handled:
#
# 1) DEPRECATED v16 l10n_it modules (fatturapa family, withholding, etc.):
#    their functionality moved to Odoo core / l10n_it_edi_* (or they are kept
#    only as empty stubs). Their old views reference fields removed in v18
#    (e.g. res.partner.electronic_invoice_obliged_subject) and break the
#    inheritance tree. They have no v18 code, so they stay archived.
#
# 2) KEPT custom modules whose website_sale.cart_lines customisations still
#    use the v16 table/td layout (v18 cart is div-based). Their v18 code is
#    already correct, but the stale DB arch breaks validation when a sibling
#    view loads first. We archive them here; the module's own v18 data files
#    then reload them with the correct div-based arch and re-activate them.

import logging

_logger = logging.getLogger(__name__)

# Case 1 - deprecated modules (28 verified deprecated in v18)
DEPRECATED_MODULES = [
    "l10n_it_fatturapa",
    "l10n_it_fatturapa_in",
    "l10n_it_fatturapa_out",
    "l10n_it_fatturapa_in_rc",
    "l10n_it_fatturapa_in_purchase",
    "l10n_it_fatturapa_out_di",
    "l10n_it_fatturapa_out_rc",
    "l10n_it_fatturapa_out_sp",
    "l10n_it_fatturapa_out_stamp",
    "l10n_it_fatturapa_out_wt",
    "l10n_it_fatturapa_sale",
    "l10n_it_fatturapa_export_zip",
    "l10n_it_fatturapa_pec",
    "l10n_it_sdi_channel",
    "l10n_it_fiscalcode",
    "l10n_it_fiscal_document_type",
    "l10n_it_fiscal_payment_term",
    "l10n_it_ipa",
    "l10n_it_rea",
    "l10n_it_vat_payability",
    "l10n_it_account_tax_kind",
    "l10n_it_withholding_tax",
    "l10n_it_withholding_tax_payment",
    "l10n_it_withholding_tax_reason",
    "l10n_it_payment_reason",
    "l10n_it_reverse_charge",
    "l10n_it_split_payment",
    "l10n_it_declaration_of_intent",
]

# Case 2 - stale views from KEPT modules; reactivated by their own v18 code.
# (module, xml_id) pairs.
#
# Only the view that is still stale *while a sibling loads* needs archiving.
# plm_trial_product_add_d_none (6974) loads first and updates its own arch to
# the v18 div layout before validation, so it never breaks. Its sibling
# website_sale_cart_line_plm_license_uuid (6986) is still on the v16
# table/thead arch at that moment and breaks the cart_lines tree -> archive it
# so it is excluded; plm reloads it afterwards with the correct arch.
STALE_KEPT_VIEWS = [
    ("plm_license_management", "website_sale_cart_line_plm_license_uuid"),
]


def migrate(cr, version):
    # Case 1: archive obsolete views owned by deprecated modules
    cr.execute(
        """
        UPDATE ir_ui_view
        SET active = false
        WHERE active = true
          AND id IN (
              SELECT res_id
              FROM ir_model_data
              WHERE model = 'ir.ui.view'
                AND module = ANY(%s)
          )
        """,
        (DEPRECATED_MODULES,),
    )
    deprecated_count = cr.rowcount

    # Case 2: archive stale website_sale cart views from kept modules
    kept_count = 0
    if STALE_KEPT_VIEWS:
        cr.execute(
            """
            UPDATE ir_ui_view
            SET active = false
            WHERE active = true
              AND id IN (
                  SELECT res_id
                  FROM ir_model_data
                  WHERE model = 'ir.ui.view'
                    AND (module, name) IN %s
              )
            """,
            (tuple(STALE_KEPT_VIEWS),),
        )
        kept_count = cr.rowcount

    _logger.info(
        "v18 migration: archived %s obsolete views from deprecated l10n_it "
        "modules and %s stale cart views from kept modules (active=false, "
        "not deleted)",
        deprecated_count,
        kept_count,
    )
