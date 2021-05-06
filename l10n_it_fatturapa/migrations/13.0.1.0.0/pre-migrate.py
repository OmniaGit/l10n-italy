# Copyright 2020 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql

# account_invoice -> account_move migration
i_m_columns = (
    ("fatturapa.payment.data", "invoice_id"),
    ("welfare.fund.data.line", "invoice_id"),
    ("withholding.data.line", "invoice_id"),
    ("discount.rise.price", "invoice_id"),
    ("fatturapa.related_document_type", "invoice_id"),
    ("fatturapa.activity.progress", "invoice_id"),
    ("fatturapa.attachments", "invoice_id"),
    ("fatturapa.related_ddt", "invoice_id"),
    ("fatturapa.summary.data", "invoice_id"),
)

invoice_data = (
    ("protocol_number"),
    ("tax_representative_id"),
    ("intermediary"),
    ("sender"),
    ("carrier_id"),
    ("transport_vehicle"),
    ("transport_reason"),
    ("number_items"),
    ("description"),
    ("unit_weight"),
    ("gross_weight"),
    ("net_weight"),
    ("pickup_datetime"),
    ("transport_date"),
    ("delivery_address"),
    ("delivery_datetime"),
    ("ftpa_incoterms"),
    ("related_invoice_code"),
    ("related_invoice_date"),
    ("vehicle_registration"),
    ("total_travel"),
    ("efatt_stabile_organizzazione_indirizzo"),
    ("efatt_stabile_organizzazione_civico"),
    ("efatt_stabile_organizzazione_cap"),
    ("efatt_stabile_organizzazione_comune"),
    ("efatt_stabile_organizzazione_provincia"),
    ("efatt_stabile_organizzazione_nazione"),
    ("efatt_rounding"),
    ("art73"),
    ("electronic_invoice_subjected"),
)

# account_invoice_line -> account_move_line migration
il_ml_columns = (
    ("discount.rise.price", "invoice_line_id"),
    ("fatturapa.related_document_type", "invoice_line_id"),
    ("fatturapa.related_ddt", "invoice_line_id"),
)

invoice_line_data = (
    "admin_ref",
    "ftpa_line_number",
)


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "account_move", "old_invoice_id"):
        for table, column in i_m_columns:
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE {0} t
                SET t.{1} = m.id
                FROM account_move m
                WHERE m.old_invoice_id = t.{1}"""
                ).format(
                    sql.Identifier(openupgrade.get_legacy_name(table)),
                    sql.Identifier(openupgrade.get_legacy_name(column)),
                ),
            )
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE account_move m
                       SET {}
                       FROM account_invoice i
                       WHERE m.old_invoice_id = i.id
                    """
                ).format(
                    ",\n".join(
                        "m.{0} = i.{0}".format(sql.Identifier(col))
                        for col in invoice_data
                    )
                ),
            )

    elif openupgrade.table_exists(env.cr, "account_invoice"):
        # relay on move_id, usually for not ('draft' or 'cancel')
        for table, column in i_m_columns:
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE {0} t
                SET t.{1} = i.move_id
                FROM account_invoice i
                WHERE t.{1} = i.id and i.move_id is NOT NULL"""
                ).format(
                    sql.Identifier(openupgrade.get_legacy_name(table)),
                    sql.Identifier(openupgrade.get_legacy_name(column)),
                ),
            )
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE account_move m
                       SET {}
                       FROM account_invoice i
                       WHERE i.move_id = m.id
                    """
                ).format(
                    ",\n".join(
                        "m.{0} = i.{0}".format(sql.Identifier(col))
                        for col in invoice_data
                    )
                ),
            )

    if openupgrade.table_exists(
        env.cr, "account_invoice_line"
    ) and openupgrade.column_exists(env.cr, "account_move_line", "old_invoice_line_id"):
        for table, column in il_ml_columns:
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE {0} t
                SET t.{1} = ml.id
                FROM account_move_line ml
                WHERE ml.old_invoice_line_id = t.{1}"""
                ).format(
                    sql.Identifier(openupgrade.get_legacy_name(table)),
                    sql.Identifier(openupgrade.get_legacy_name(column)),
                ),
            )
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE account_move_line ml
                       SET {}
                       FROM account_invoice_line il
                       WHERE ml.old_invoice_line_id = il.id
                    """
                ).format(
                    ",\n".join(
                        "ml.{0} = il.{0}".format(sql.Identifier(col))
                        for col in invoice_line_data
                    )
                ),
            )

    elif openupgrade.table_exists(env.cr, "account_invoice_line"):
        # relay on move_id, usually for not ('draft' or 'cancel')
        for table, column in i_m_columns:
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE {0} t
                SET t.{1} = ml.id
                FROM account_move_line ml
                JOIN account_move m ON (m.id = ml.move_id)
                JOIN account_invoice i ON (i.move_id = m.id)
                JOIN account_invoice_line il ON (il.invoice_id = i.id)
                WHERE t.{1} = il.id AND ml.sequence = il.sequence"""
                ).format(
                    sql.Identifier(openupgrade.get_legacy_name(table)),
                    sql.Identifier(openupgrade.get_legacy_name(column)),
                ),
            )
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE account_move_line ml
                       SET {}
                       FROM account_invoice_line il
                       JOIN account_invoice i ON (i.id = il.invoice_id)
                       JOIN account_move m ON (m.id = i.move_id)
                       WHERE ml.sequence = il.sequence
                    """
                ).format(
                    ",\n".join(
                        "ml.{0} = il.{0}".format(sql.Identifier(col))
                        for col in invoice_line_data
                    )
                ),
            )
