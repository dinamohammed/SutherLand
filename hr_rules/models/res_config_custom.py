# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime


class HrEmployeeConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    taxbase_erase_date = fields.Date("Tax Base Clearance on ")

    @api.model
    def get_values(self):
        res = super(HrEmployeeConfigSetting, self).get_values()
        res['taxbase_erase_date'] = self.env['ir.config_parameter'].\
                                       get_param('taxbase_erase_date', default=datetime.today())
        return res

    def set_values(self):
        self.taxbase_erase_date and self.env['ir.config_parameter'].\
            set_param('taxbase_erase_date', self.taxbase_erase_date)
        super(HrEmployeeConfigSetting, self).set_values()

