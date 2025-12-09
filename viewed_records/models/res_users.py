from odoo import api, fields, models, _


class ResUsersViewedHistory(models.Model):
    _inherit = 'res.users'
    _description = 'History of Responsibles'

    viewed_history_ids = fields.One2many(
        'viewed.records.history', inverse_name='user_id', string='Viewed History', readonly=True)
    