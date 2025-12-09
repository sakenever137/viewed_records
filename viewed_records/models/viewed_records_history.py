from odoo import api, fields, models, _
from datetime import datetime, timedelta

class ViewedRecordsHistory(models.Model):
    _name = 'viewed.records.history'
    _description = 'Records Viewed History'
    _order = "create_date DESC"

    res_model = fields.Char(string='Model Name', required=True)
    record_id = fields.Integer(string='Record ID', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    record_name = fields.Char(string='Record Name')
    record_url = fields.Char(string='Record URL', readonly=True)
    
    @api.model
    def _cleanup_old_records(self):
        """Deleting a record older than limit_of_viewed_records_by_date days"""
        limit_of_viewed_records_by_date = self.env['ir.config_parameter'].sudo().get_param('viewed_records.limit_of_viewed_records_by_date')
        if not limit_of_viewed_records_by_date:
            return None
        cutoff_date = fields.Datetime.to_string(datetime.now() - timedelta(days=int(limit_of_viewed_records_by_date)))
        old_records = self.search([('create_date', '<', cutoff_date)])
        if old_records:
            old_records.unlink()
