# -*- coding: utf-8 -*-

from odoo import models, fields


class HrContactType(models.Model):
    _name = 'hr.contract.type'
    _inherit = ['mail.thread']
    _order = "name"

    name = fields.Char(string="Contract Type", required=True)
    code = fields.Char(string="Contract Code", required=True)

