# Copyright 2026 OmniaSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
# v16 -> v18 migration helper.
#
# Several v16 l10n_it modules are deprecated in v18 (their functionality moved
# to Odoo core / l10n_it_edi_* or are kept only as empty stubs). Their old
# views remain in the database and reference fields that no longer exist in
# v18 (e.g. res.partner.electronic_invoice_obliged_subject from
# l10n_it_fatturapa). When a still-loading module (such as l10n_it_account)
# re-validates an inheritance tree that contains these orphan views, the
# missing field raises a ParseError and the whole upgrade build fails.
#
# This pre-migration runs before l10n_it_account loads its own views and
# ARCHIVES (active = false) the obsolete views owned by those deprecated
# modules. Archived views are excluded from the inheritance/validation tree
# but are NOT deleted, so they remain fully recoverable (just set active back
# to true if ever needed). No business data is touched - only UI view records.

import logging

_logger = logging.getLogger(__name__)

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


def migrate(cr, version):
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
    _logger.info(
        "v18 migration: archived %s obsolete views from deprecated "
        "l10n_it modules (active=false, not deleted)",
        cr.rowcount,
    )
