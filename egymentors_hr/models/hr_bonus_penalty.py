# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.exceptions import Warning

_STATES = [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')]
# Ahmed Salama Code Start ---->


class HrBonusPenalty(models.Model):
	_name = 'hr.bonus.penalty'
	_description = "Hr Bonus/Penalty"
	_inherit = ['mail.thread', 'image.mixin']
	
	name = fields.Char("Bonus", translate=True)
	extra_type = fields.Selection([('bonus', 'Bonus'),
	                               ('penalty', 'Penalty')], "Type",
	                              readonly=True, states={'draft': [('readonly', False)]})
	bonus_type = fields.Selection([('allowance', 'Allowance'), ('rewards', 'Rewards')],
	                              "Bonus Type", readonly=True, default='rewards', states={'draft': [('readonly', False)]})
	date = fields.Date("Date", default=fields.Date.today(),
	                   readonly=True, states={'draft': [('readonly', False)]})
	fixed_amount = fields.Boolean("Fixed Amount",
	                              readonly=True, states={'draft': [('readonly', False)]})
	date_to = fields.Date("To Date",
	                      readonly=True, states={'draft': [('readonly', False)]})
	period_month = fields.Char("Period Month",
	                           default=lambda x: fields.Date.today().strftime("%B"),
	                           readonly=True, states={'draft': [('readonly', False)]})
	work_location_id = fields.Many2one('hr.location', "Work Location",
	                                   readonly=True, states={'draft': [('readonly', False)]})
	state = fields.Selection(_STATES, default='draft', string="Stage", track_visibility='onchange')
	line_ids = fields.One2many('hr.bonus.penalty.line', 'bonus_penalty_id', "Lines",
	                           readonly=True, states={'draft': [('readonly', False)]})
	
	def _change_state(self, state):
		self.write({'state': state})
		for line in self.line_ids:
			line.write({'state': state})
	
	def action_confirm(self):
		for action in self:
			action._change_state('confirm')
	
	def action_cancel(self):
		for action in self:
			action._change_state('cancel')
	
	def action_reset(self):
		for action in self:
			action._change_state('draft')
	
	def action_print_report(self):
		if self[0].extra_type == 'bonus':
			return self.env.ref('egymentors_hr.hr_bonus_report').report_action(self)
		elif self[0].extra_type == 'penalty':
			return self.env.ref('egymentors_hr.hr_penalty_report').report_action(self)
		else:
			raise Warning(_("Something Went Wrong!!!"))
	
	def unlink(self):
		for rec in self:
			if rec.state == 'confirm':
				raise Warning(_("You can't delete confirmed records!!!"))
		return super(HrBonusPenalty, self).unlink()
	
	@api.onchange('line_ids')
	@api.depends('line_ids.days_num','line_ids.amount')
	def _get_total_bonus_penalty(self):
		# Bonus Allowance
		bonus_production = self.env.ref('egymentors_hr.bonus_production')
		bonus_leadership = self.env.ref('egymentors_hr.bonus_leadership')
		bonus_board_of_direction = self.env.ref('egymentors_hr.bonus_board_of_direction')
		bonus_workshop = self.env.ref('egymentors_hr.bonus_workshop')
		# Bonus Reward
		bonus_comp_off_site = self.env.ref('egymentors_hr.bonus_comp_off_site')
		bonus_comp_off_home = self.env.ref('egymentors_hr.bonus_comp_off_home')
		bonus_overtime_site = self.env.ref('egymentors_hr.bonus_overtime_site')
		bonus_overtime_home = self.env.ref('egymentors_hr.bonus_overtime_home')
		bonus_vpp = self.env.ref('egymentors_hr.bonus_vpp')
		bonus_ramadan = self.env.ref('egymentors_hr.bonus_ramadan')
		bonus_other = self.env.ref('egymentors_hr.bonus_other')
		bonus_night_shift = self.env.ref('egymentors_hr.bonus_night_shift')
		bonus_leave_balance = self.env.ref('egymentors_hr.bonus_leave_balance')
		bonus_amount_vpp = self.env.ref('egymentors_hr.bonus_amount_vpp')
		# Penalty
		penalty_other = self.env.ref('egymentors_hr.penalty_other')
		penalty_ramadan = self.env.ref('egymentors_hr.penalty_ramadan')
		penalty_absence = self.env.ref('egymentors_hr.penalty_absence')
		penalty_advanced = self.env.ref('egymentors_hr.penalty_advanced')
		
		for rec in self:
			rec.total_bonuses = sum(l.amount for l in rec.line_ids)
			# Penalty
			rec.total_penalty_other = sum(l.days_num for l in
			                              rec.line_ids.filtered(lambda x: x.type_id == penalty_other))
			rec.total_penalty_ramadan = sum(l.days_num for l in
			                                rec.line_ids.filtered(lambda x: x.type_id == penalty_ramadan))
			rec.total_penalty_absence = sum(l.days_num for l in
			                                rec.line_ids.filtered(lambda x: x.type_id == penalty_absence))
			rec.total_penalty_advanced = sum(l.days_num for l in
			                                 rec.line_ids.filtered(lambda x: x.type_id == penalty_advanced))
			rec.total_penalties = sum(l.days_num for l in
			                          rec.line_ids.filtered(lambda x: x.extra_type == 'penalty'))
			# Bonus
			# Allowance
			rec.total_bonus_production = sum(l.amount for l in
			                                 rec.line_ids.filtered(lambda x: x.type_id == bonus_production))
			rec.total_bonus_leadership = sum(l.amount for l in
			                                 rec.line_ids.filtered(lambda x: x.type_id == bonus_leadership))
			rec.total_bonus_workshop = sum(l.amount for l in
			                               rec.line_ids.filtered(lambda x: x.type_id == bonus_workshop))
			rec.total_bonus_direction = sum(l.amount for l in
			                                rec.line_ids.filtered(lambda x: x.type_id == bonus_board_of_direction))
			rec.total_bonuses_allowance = sum(l.amount for l in
			                                  rec.line_ids.filtered(lambda x: x.type_id.bonus_type == 'allowance'))
			# Rewards
			rec.total_bonus_comp_off_site = sum(l.amount for l in
			                                    rec.line_ids.filtered(lambda x: x.type_id == bonus_comp_off_site))
			rec.total_bonus_comp_off_home = sum(l.amount for l in
			                                    rec.line_ids.filtered(lambda x: x.type_id == bonus_comp_off_home))
			rec.total_bonus_overtime_site = sum(l.amount for l in
			                                    rec.line_ids.filtered(lambda x: x.type_id == bonus_overtime_site))
			rec.total_bonus_overtime_home = sum(l.amount for l in
			                                    rec.line_ids.filtered(lambda x: x.type_id == bonus_overtime_home))
			rec.total_bonus_vpp = sum(l.amount for l in
			                          rec.line_ids.filtered(lambda x: x.type_id == bonus_vpp))
			rec.total_bonus_ramadan = sum(l.amount for l in
			                              rec.line_ids.filtered(lambda x: x.type_id == bonus_ramadan))
			rec.total_bonus_other = sum(l.amount for l in
			                            rec.line_ids.filtered(lambda x: x.type_id == bonus_other))
			rec.total_bonus_night_shift = sum(l.amount for l in
			                            rec.line_ids.filtered(lambda x: x.type_id == bonus_night_shift))
			rec.total_bonus_leave_balance = sum(l.amount for l in
			                            rec.line_ids.filtered(lambda x: x.type_id == bonus_leave_balance))
			rec.total_bonus_amount_vpp = sum(l.amount for l in
												rec.line_ids.filtered(lambda x: x.type_id == bonus_amount_vpp))
			rec.total_bonuses_rewards = sum(l.amount for l in
			                                rec.line_ids.filtered(lambda x: x.type_id.bonus_type == 'rewards'))
	
	@api.onchange('work_location_id', 'extra_type', 'bonus_type')
	def generate_employee_ids(self):
		emp_obj = self.env['hr.employee']
		type_obj = self.env['hr.bonus.penalty.type']
		for rec in self:
			if rec.extra_type == 'bonus' and rec.work_location_id:
				domain = [('extra_type', '=', 'bonus')]
				if rec.bonus_type:
					domain.append(('bonus_type', '=', rec.bonus_type))
				type_id = type_obj.search(domain, limit=1)
				emps_list = rec.line_ids.mapped('employee_id.id')
				emp_ids = emp_obj.search([('work_location_id', '=', rec.work_location_id.id)])
				for emp_id in emp_ids:
					if emp_id.id not in emps_list:
						rec.line_ids.create({
							'bonus_penalty_id': rec.id,
							'employee_id': emp_id.id,
							'type_id': type_id and type_id.id or False,
						})
	
	total_bonuses = fields.Float("Total Bonuses", compute=_get_total_bonus_penalty)
	# Bonus Allowance
	total_bonuses_allowance = fields.Float("Total Bonuses(Allowance)", compute=_get_total_bonus_penalty)
	total_bonuses_rewards = fields.Float("Total Bonuses(Rewards)", compute=_get_total_bonus_penalty)
	total_bonus_production = fields.Float("Production", compute=_get_total_bonus_penalty)
	total_bonus_leadership = fields.Float("Leadership", compute=_get_total_bonus_penalty)
	total_bonus_workshop = fields.Float("Workshop", compute=_get_total_bonus_penalty)
	total_bonus_direction = fields.Float("Board of Direction", compute=_get_total_bonus_penalty)
	# Bonus Rewards
	total_bonus_comp_off_site = fields.Float("Comp Off Site", compute=_get_total_bonus_penalty)
	total_bonus_comp_off_home = fields.Float("Comp Off Home", compute=_get_total_bonus_penalty)
	total_bonus_overtime_site = fields.Float("OverTime Site", compute=_get_total_bonus_penalty)
	total_bonus_overtime_home = fields.Float("OverTime Home", compute=_get_total_bonus_penalty)
	total_bonus_vpp = fields.Float("VPP", compute=_get_total_bonus_penalty)
	total_bonus_ramadan = fields.Float("Ramadan", compute=_get_total_bonus_penalty)
	total_bonus_other = fields.Float("Other", compute=_get_total_bonus_penalty)
	total_bonus_night_shift = fields.Float("Night Shift", compute=_get_total_bonus_penalty)
	total_bonus_leave_balance = fields.Float("Leave Balance", compute=_get_total_bonus_penalty)
	total_bonus_amount_vpp = fields.Float("Amount VPP", compute=_get_total_bonus_penalty)
	# Penalties
	total_penalties = fields.Float("Total Penalties", compute=_get_total_bonus_penalty)
	total_penalty_absence = fields.Float("Absence", compute=_get_total_bonus_penalty)
	total_penalty_other = fields.Float("Other", compute=_get_total_bonus_penalty)
	total_penalty_ramadan = fields.Float("Ramadan", compute=_get_total_bonus_penalty)
	total_penalty_advanced = fields.Float("Advanced Payment", compute=_get_total_bonus_penalty)
	
	
class HrBonusPenaltyLine(models.Model):
	_name = 'hr.bonus.penalty.line'
	_description = "Hr Bonus/Penalty Line"
	_rec_name = 'employee_id'
	
	bonus_penalty_id = fields.Many2one('hr.bonus.penalty', "Bonus/Penalty")
	payslip_id = fields.Many2one('hr.payslip', "Payslip")
	date = fields.Date(related='bonus_penalty_id.date')
	date_to = fields.Date(related='bonus_penalty_id.date_to')
	state = fields.Selection(_STATES, default='draft', string="Stage", track_visibility='onchange')
	extra_type = fields.Selection(related='bonus_penalty_id.extra_type')
	
	@api.onchange('bonus_penalty_id', 'extra_type')
	@api.depends('bonus_penalty_id.work_location_id')
	def _get_emp_domain(self):
		for line in self:
			domain = []
			if line.extra_type == 'bonus' and line.bonus_penalty_id.work_location_id:
				domain = [('work_location_id', '=', line.bonus_penalty_id.work_location_id.id)]
			return {'domain': {'employee_id': domain}}
	
	employee_id = fields.Many2one('hr.employee', "Employee", required=True, domain=_get_emp_domain)
	type_id = fields.Many2one('hr.bonus.penalty.type', "Type", required=True)
	pre_amount = fields.Float("Amount")
	discount_list = fields.Float("Discount list")
	stop_incentive = fields.Float("Stop incentive")
	amount = fields.Float("Net Amount")
	
	days_num = fields.Float("Number of Days", default=1)
	notes = fields.Text("Notes")
	
	@api.model
	def create(self, vals):
		if vals.get('pre_amount') or vals.get('discount_list') \
				or vals.get('stop_incentive') and vals.get('bonus_type') == 'allowance':
			self._compute_other_vals(vals)
		return super(HrBonusPenaltyLine, self).create(vals)
	
	def write(self, vals_list):
		for line in self:
			if vals_list.get('pre_amount') or vals_list.get('discount_list') \
					or vals_list.get('stop_incentive') and line.bonus_penalty_id.bonus_type == 'allowance':
				line._compute_other_vals(vals_list)
			return super(HrBonusPenaltyLine, self).write(vals_list)
	
	def _compute_other_vals(self, vals_list):
		pre_amount = vals_list.get('pre_amount') or self.pre_amount
		discount_list = vals_list.get('discount_list') or self.discount_list
		stop_incentive = vals_list.get('stop_incentive') or self.stop_incentive
		vals_list['amount'] = pre_amount - discount_list - stop_incentive
		return vals_list


class HrBonusPenaltyType(models.Model):
	_name = 'hr.bonus.penalty.type'
	_description = "Hr Bonus Type"
	
	name = fields.Char("Bonus Type", translate=True)
	extra_type = fields.Selection([('bonus', 'Bonus'),
	                               ('penalty', 'Penalty')], "Type")
	bonus_type = fields.Selection([('allowance', 'Allowance'), ('rewards', 'Rewards')],
	                              "Bonus Type")
	fixed_amount = fields.Boolean("Fixed Amount",
	                              help="If selected it will add start and end month ")
# Ahmed Salama Code End.
