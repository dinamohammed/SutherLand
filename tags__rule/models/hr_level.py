# -*- coding: utf-8 -*-

from odoo import models, fields


class HrLevel(models.Model):
    _name = 'hr.level'
    _description = "HR Level"
    
    name = fields.Char("Level")








