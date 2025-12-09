# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ViewedRecordsHistoryResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    limit_of_viewed_records_by_date = fields.Integer(string='Limit of Viewed Records by Date (days)', default=30)

    def set_values(self):
        res = super(ViewedRecordsHistoryResConfig, self).set_values()
        params = self.env["ir.config_parameter"]
        def __set_param(param_str):
            nonlocal params, self
            params.set_param("viewed_records." + param_str, getattr(self, param_str))
        __set_param("limit_of_viewed_records_by_date")
        return res

    @api.model
    def get_values(self):
        res = super(ViewedRecordsHistoryResConfig, self).get_values()
        params = self.env["ir.config_parameter"]
        def __get_param(param_str):
            nonlocal params, res
            res.update({param_str:params.get_param("viewed_records." + param_str)})
        __get_param("limit_of_viewed_records_by_date")
     
        return res
