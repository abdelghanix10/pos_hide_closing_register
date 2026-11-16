from datetime import datetime
from zoneinfo import ZoneInfo
import json
import traceback

from odoo import models, fields, api


class PosSession(models.Model):
    _inherit = 'pos.session'

    closing_inventory_log_json = fields.Text(
        string="Closing Inventory Log (JSON)",
        help="Stores the inventory adjustments recorded when closing this session.",
    )

    @api.model
    def get_daily_sale_report_html(self, session_id):
        try:
            session = self.env['pos.session'].sudo().browse(session_id)
            if not session.exists():
                return "<html><body><h1>Session not found</h1></body></html>"
            report = self.env.ref('pos_hide_closing_register.sale_details_report').sudo()
            html = report._render_qweb_html(report.report_name, [session_id])[0].decode('utf-8')
            return html
        except Exception as e:
            return (
                f"<html><body><h1>Error</h1><p>{str(e)}</p>"
                f"<pre>{traceback.format_exc()}</pre></body></html>"
            )

    @api.model
    def apply_inventory_adjustments(self, session_id, adjustments):
        session = self.sudo().browse(session_id)
        if not session.exists():
            return False

        StockQuant = self.env['stock.quant'].sudo()
        location = session.config_id.picking_type_id.default_location_src_id
        if not location:
            return False

        log_entries = []

        for adj in adjustments:
            product_id = adj.get('product_id')
            quantity = adj.get('quantity')

            if product_id and quantity is not None:
                product = self.env['product.product'].sudo().browse(product_id)
                quant = StockQuant.search([
                    ('product_id', '=', product_id),
                    ('location_id', '=', location.id),
                ], limit=1)

                prev_qty = quant.quantity if quant else 0.0

                if not quant:
                    quant = StockQuant.create({
                        'product_id': product_id,
                        'location_id': location.id,
                    })

                quant.inventory_quantity = float(quantity)
                quant.action_apply_inventory()

                log_entries.append({
                    'product_name': product.display_name,
                    'previous_qty': prev_qty,
                    'counted_qty': float(quantity),
                    'difference': float(quantity) - prev_qty,
                })

        session.closing_inventory_log_json = json.dumps(log_entries)
        return True

    def _get_custom_sale_details_data(self):
        """Computes structured, timezone-aware Custom Sales Details data for the QWeb report."""
        self.ensure_one()
        user_tz = self.env.tz or ZoneInfo(self.env.user.tz or 'UTC')
        if isinstance(user_tz, str):
            user_tz = ZoneInfo(user_tz)
        utc_tz = ZoneInfo('UTC')

        def _fmt_dt(dt_val):
            if not dt_val:
                return '-'
            return dt_val.replace(tzinfo=utc_tz).astimezone(user_tz).strftime('%Y-%m-%d %H:%M:%S')

        valid_orders = self.order_ids.filtered(lambda o: o.state not in ('draft', 'cancel'))
        refund_orders = valid_orders.filtered(lambda o: o.amount_total < 0)

        total_sales = sum(valid_orders.mapped('amount_total'))
        total_tax = sum(valid_orders.mapped('amount_tax'))
        net_sales = total_sales - total_tax
        total_refunds = sum(refund_orders.mapped('amount_total'))

        total_discount = 0.0
        categories_map = {}
        total_items_qty = 0.0

        for order in valid_orders:
            for line in order.lines:
                product = line.product_id
                if not product:
                    continue

                if line.discount:
                    total_discount += (line.price_unit * line.qty * line.discount / 100.0)

                # Determine primary POS category (avoid double counting across multiple categories)
                cat_name = 'Uncategorized'
                tmpl = product.product_tmpl_id
                if 'pos_categ_ids' in tmpl._fields and tmpl.pos_categ_ids:
                    cat_name = tmpl.pos_categ_ids[0].name
                elif 'pos_categ_id' in tmpl._fields and tmpl.pos_categ_id:
                    cat_name = tmpl.pos_categ_id.name

                if cat_name not in categories_map:
                    categories_map[cat_name] = {
                        'name': cat_name,
                        'qty': 0.0,
                        'amount': 0.0,
                        'products': {},
                    }

                categories_map[cat_name]['qty'] += line.qty
                categories_map[cat_name]['amount'] += line.price_subtotal_incl
                total_items_qty += line.qty

                p_key = product.id
                if p_key not in categories_map[cat_name]['products']:
                    categories_map[cat_name]['products'][p_key] = {
                        'name': product.display_name,
                        'qty': 0.0,
                        'amount': 0.0,
                    }
                categories_map[cat_name]['products'][p_key]['qty'] += line.qty
                categories_map[cat_name]['products'][p_key]['amount'] += line.price_subtotal_incl

        categories_list = []
        for cat in sorted(categories_map.values(), key=lambda c: c['name']):
            cat_products = sorted(cat['products'].values(), key=lambda p: p['name'])
            categories_list.append({
                'name': cat['name'],
                'qty': cat['qty'],
                'amount': cat['amount'],
                'products': cat_products,
            })

        # Payments aggregation
        payments_map = {}
        for payment in valid_orders.mapped('payment_ids'):
            m_name = payment.payment_method_id.name or 'Other'
            payments_map[m_name] = payments_map.get(m_name, 0.0) + payment.amount

        payments_list = [
            {'name': name, 'amount': amount}
            for name, amount in sorted(payments_map.items(), key=lambda x: x[0])
        ]

        # Cash register balances
        opening_cash = getattr(self, 'cash_register_balance_start', 0.0) or 0.0
        expected_cash = getattr(self, 'cash_register_balance_end', 0.0) or 0.0
        counted_cash = getattr(self, 'cash_register_balance_end_real', 0.0) or expected_cash
        cash_diff = getattr(self, 'cash_register_difference', 0.0) or (counted_cash - expected_cash)

        # Inventory adjustments log
        inventory_log = []
        if self.closing_inventory_log_json:
            try:
                inventory_log = json.loads(self.closing_inventory_log_json)
            except Exception:
                inventory_log = []

        now_local = datetime.now(tz=user_tz).strftime('%Y-%m-%d %H:%M:%S')

        return {
            'opened_at': _fmt_dt(self.start_at),
            'closed_at': _fmt_dt(self.stop_at),
            'generated_at': now_local,
            'cashier': self.user_id.name or '',
            'order_count': len(valid_orders),
            'refund_count': len(refund_orders),
            'total_items_qty': total_items_qty,
            'total_sales': total_sales,
            'net_sales': net_sales,
            'total_tax': total_tax,
            'total_discount': total_discount,
            'total_refunds': total_refunds,
            'opening_cash': opening_cash,
            'expected_cash': expected_cash,
            'counted_cash': counted_cash,
            'cash_diff': cash_diff,
            'categories': categories_list,
            'payments': payments_list,
            'inventory_log': inventory_log,
            'currency': self.config_id.sale_details_currency_symbol or 'DH',
        }