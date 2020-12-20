# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import Warning
# Ahmed Salama Code Start ---->


class HrEmployeeInherit(models.Model):
	_inherit = 'hr.employee'
	
	location_type = fields.Selection([('static', 'Static'),
	                                  ('dynamic', 'Dynamic'),
	                                  ('management', 'Management')], string="Location Type")
	
	insurance_type = fields.Selection([('foreigner', 'Foreigner'),
	                                   ('insured', 'Insured'), ('out_insurance', 'Outside Insurance'),
	                                   ('pension', 'Pension'), ('blacked', 'Blacked')], string="Insurance",
	                                  required=True, default='insured')
	employee_status = fields.Text("Employee Status")
	
	tax_base = fields.Float(string='Tax Base', default=0)
	work_location_id = fields.Many2one('hr.location', 'Program')
	
	def Daily_Check_Value(self):
		
		Current_Date = datetime.now()
		if Current_Date.day == '30' or Current_Date.day == '31':
			emp_rec = self.env['hr.employee'].search([])
			for emp in emp_rec:
				emp['tax_base'] = 0
	
	# ############### ############### ############### ############### ################
	# Create A Scheduled Action :
	# Name : Update Tax Base Value
	# Model : Employee
	# Execute Every : 1 Week
	# Number of calls : -1
	# Action to Do : Execute Python Code
	# Code to write : Update Tax Base Value
	
	# ############### ############### ############### ############### #################
	# Add Fields to Employee Screen
	levels = fields.Selection([('level1', 'Level 1'),
	                           ('level2', 'Level 2'),
	                           ('level3', 'Level 3'),
	                           ('level4', 'Level 4'),
	                           ('level5', 'Level 5'),
	                           ('level6', 'Level 6'),
	                           ('level_dep_manager', 'Department Manager Level'),
	                           ('level_sec_manager', 'Section Manager Level'),
	                           ('level_sho2on_manager', 'Shoaon Manager Level')], string='Level')
	level_id = fields.Many2one('hr.level', "Level")
	
	certificate_level = fields.Selection([('diploma', 'Diploma'),
	                                      ('bachelor', 'Bachelor'),
	                                      ('license', 'License'),
	                                      ('master', 'Master'),
	                                      ('other', 'Other')], string='Certificate')
	
	grade_level = fields.Selection([('excellent', 'Excellent'),
	                                ('very_good', 'Very Good'),
	                                ('good', 'Good'),
	                                ('med', 'Med'),
	                                ('other', 'Other')], string='Grade Level')
	grade_year = fields.Char(string='Graduation Year')
	
	social_insurance_no = fields.Char(string='Social Insurance No.')
	insurance_date = fields.Date(string='Social Insurance Date')
	start_date = fields.Date(string='Social Insurance Start Date')
	end_date = fields.Date(string='Social Insurance End Date')
	medical_insurance_no = fields.Char(string='Medical Insurance No.')
	medical_location = fields.Char(string='Medical Location')
    
	employee_status_id = fields.Many2one('employee.status', 'Employee Status')
	
	# employee_no = fields.Char(string='Employee Registration Number', search='_get_search_list')
	#
	# def _get_search_list(self, operator, value):
	# 	# print("------------------- On Search List -----------------")
	# 	# print("VALS:: ",operator,value )
	# 	if operator == 'like':
	# 		operator = 'ilike'
	# 	employee_ids = self.env['hr.employee'].search([('registration_number', operator, value)]).mapped('id')
	# 	# print("Employee Ids:: ", employee_ids)
	# 	payslip_ids = self.env['hr.payslip'].search([('employee_id', 'in', employee_ids)]).mapped('id')
	# 	# ids = values
	# 	# print("Contract Ids:: ", payslip_ids)
	# 	return [('id', 'in', payslip_ids)]

# Ahmed Salama Code End.
