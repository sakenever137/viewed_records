from odoo import api, fields, models, _
from odoo.addons.web.controllers import utils

class ViewedRecordsMixin(models.AbstractModel):
    _name = 'viewed.records.mixin'
    _description = 'Viewed Records Mixin'

    is_viewed = fields.Boolean(string='Is Opened', compute='_compute_is_viewed')
    
    @api.depends()
    def _compute_is_viewed(self):
        ViewedRecordsHistory = self.env['viewed.records.history']
        action_id = self.env.context.get('params', {}).get('action')
        for rec in self:
            viewed_record = ViewedRecordsHistory.search([
                ('res_model', '=', self._name),
                ('record_id', '=', rec.id),
                ('user_id', '=', self.env.user.id),
            ], limit=1)
            rec.is_viewed = bool(viewed_record)
    
    def check_viewed(self, res_model):
        ViewedRecordsHistory = self.env['viewed.records.history']
        viewed_record = ViewedRecordsHistory.search([
            ('res_model', '=', res_model),
            ('record_id', '=', self.id),
            ('user_id', '=', self.env.uid),
        ], limit=1)

        return bool(viewed_record)

    def mark_as_viewed(self, res_name):
        self.ensure_one()
        ViewedRecordsHistory = self.env['viewed.records.history']
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        check_viewed = self.check_viewed(res_name)
        if not check_viewed:
            ViewedRecordsHistory.sudo().create({
                'record_id': self.id,
                'res_model': res_name,
                'user_id': self.env.uid,
                'record_name': self.display_name,
                'record_url': f"{base_url}/web#id={self.id}&model={res_name}&view_type=form",
            })

    def _mark_as_dont_viewed(self, res_model, rec_id, users):
        for user in users:
            ViewedRecordsHistory = self.env['viewed.records.history']
            viewed_record = ViewedRecordsHistory.search([
                ('res_model', '=', res_model),
                ('record_id', '=', rec_id),
                ('user_id', '=', user.id),
            ], limit=1)
            
            if viewed_record:
                viewed_record.sudo().unlink()
                self.is_viewed = False
    