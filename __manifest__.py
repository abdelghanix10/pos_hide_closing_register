{
    'name': 'POS Hide Closing Register & Custom Sales Details',
    'version': '20.0.2.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Automate POS closing with inventory count and customizable Sales Details report',
    'description': """
POS Hide Closing Register & Custom Sales Details (Odoo 20)
==========================================================
- Replaces the standard Closing Control popup with an automated closing workflow.
- Optional Inventory Adjustment popup before closing to record stock counts.
- Fully customizable Sales Details thermal report (Company info, Session summary, Cash control, Category & Product breakdown, Discounts/Refunds/Taxes, Payments, and Closing Inventory counts).
- Supports Chrome Print Preview and QZ Tray direct thermal printing.
    """,
    'depends': ['point_of_sale', 'stock'],
    'data': [
        'report_saledetails.xml',
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_hide_closing_register/static/src/js/inventory_adjustment_popup.js',
            'pos_hide_closing_register/static/src/xml/inventory_adjustment_popup.xml',
            'pos_hide_closing_register/static/src/js/pos_hide_closing_register.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}