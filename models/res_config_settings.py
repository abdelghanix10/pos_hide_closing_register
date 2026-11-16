from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_hide_closing_register = fields.Boolean(related='pos_config_id.hide_closing_register', readonly=False)
    pos_enable_inventory_adjustment = fields.Boolean(related='pos_config_id.enable_inventory_adjustment', readonly=False)
    pos_inventory_adjustment_product_ids = fields.Many2many(related='pos_config_id.inventory_adjustment_product_ids', readonly=False)
    pos_closing_print_method = fields.Selection(related='pos_config_id.print_method', readonly=False)

    pos_enable_auto_print_sale_details = fields.Boolean(related='pos_config_id.enable_auto_print_sale_details', readonly=False)
    pos_sale_details_custom_title = fields.Char(related='pos_config_id.sale_details_custom_title', readonly=False)
    pos_sale_details_custom_header = fields.Char(related='pos_config_id.sale_details_custom_header', readonly=False)
    pos_sale_details_custom_footer = fields.Char(related='pos_config_id.sale_details_custom_footer', readonly=False)
    pos_sale_details_currency_symbol = fields.Char(related='pos_config_id.sale_details_currency_symbol', readonly=False)

    pos_sd_show_company_info = fields.Boolean(related='pos_config_id.sd_show_company_info', readonly=False)
    pos_sd_show_session_summary = fields.Boolean(related='pos_config_id.sd_show_session_summary', readonly=False)
    pos_sd_show_cash_control = fields.Boolean(related='pos_config_id.sd_show_cash_control', readonly=False)
    pos_sd_show_sales_by_category = fields.Boolean(related='pos_config_id.sd_show_sales_by_category', readonly=False)
    pos_sd_show_discounts_and_refunds = fields.Boolean(related='pos_config_id.sd_show_discounts_and_refunds', readonly=False)
    pos_sd_show_payment_methods = fields.Boolean(related='pos_config_id.sd_show_payment_methods', readonly=False)
    pos_sd_show_inventory_adjustments = fields.Boolean(related='pos_config_id.sd_show_inventory_adjustments', readonly=False)