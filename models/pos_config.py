from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    hide_closing_register = fields.Boolean(
        string="Hide Closing Register Popup",
        default=True,
        help="Skip the standard closing control popup and close the session automatically.",
    )
    enable_inventory_adjustment = fields.Boolean(
        string="Enable Closing Inventory Check",
        default=True,
        help="Prompt the cashier to enter product inventory counts before closing the session.",
    )
    inventory_adjustment_product_ids = fields.Many2many(
        'product.product',
        string="Inventory Adjustment Products",
        help="Leave empty to allow selecting any POS product, or specify products to count at closing.",
    )
    print_method = fields.Selection(
        [
            ('chrome_preview', 'Chrome Print Preview'),
            ('qz_tray', 'QZ Tray'),
        ],
        string="Print Method",
        default='chrome_preview',
        help="Chrome Print Preview opens the browser print dialog; QZ Tray prints directly to the default thermal printer.",
    )

    # Custom Sales Details Report Configuration
    enable_auto_print_sale_details = fields.Boolean(
        string="Auto-Print Sales Details on Close",
        default=True,
    )
    sale_details_custom_title = fields.Char(
        string="Report Title",
        default="SESSION REPORT",
    )
    sale_details_custom_header = fields.Char(
        string="Custom Header Note",
        help="Optional subtitle or note printed below the report title.",
    )
    sale_details_custom_footer = fields.Char(
        string="Custom Footer Message",
        default="Thank you for using Odoo POS",
    )
    sale_details_currency_symbol = fields.Char(
        string="Currency Label",
        default="DH",
    )

    # Section toggles for Custom Sales Details
    sd_show_company_info = fields.Boolean(string="Show Company Info", default=True)
    sd_show_session_summary = fields.Boolean(string="Show Session & Order Count", default=True)
    sd_show_cash_control = fields.Boolean(string="Show Cash Register Balances", default=True)
    sd_show_sales_by_category = fields.Boolean(string="Show Sales Breakdown by Category", default=True)
    sd_show_discounts_and_refunds = fields.Boolean(string="Show Discounts, Taxes & Refunds", default=True)
    sd_show_payment_methods = fields.Boolean(string="Show Payment Methods Breakdown", default=True)
    sd_show_inventory_adjustments = fields.Boolean(string="Show Closing Inventory Counts", default=True)