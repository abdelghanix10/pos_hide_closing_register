from odoo import models, api


class ReportSaleDetails(models.AbstractModel):
    _name = 'report.pos_hide_closing_register.report_saledetails'
    _description = 'Point of Sale Custom Sales Details'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['pos.session'].sudo().browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'pos.session',
            'docs': docs,
        }