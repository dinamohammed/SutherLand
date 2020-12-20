# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProvinCityMode(models.Model):
    _name = 'provin.city.mode'
    _description = "Billability"

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
