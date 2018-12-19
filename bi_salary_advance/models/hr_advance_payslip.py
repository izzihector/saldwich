# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    sa_id = fields.Many2one('salary.advance', string="Salary Advance")


class SalaryRuleInput(models.Model):
    _inherit = 'hr.payslip'

    def get_inputs(self, contract_ids, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(SalaryRuleInput, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        emp_id = contract_obj.browse(contract_ids[0].id).employee_id
        adv_salary = self.env['salary.advance'].search([('employee_id', '=', emp_id.id)])
        for adv_obj in adv_salary:
            current_date = date_from.month
            date = adv_obj.date
            existing_date = date.month
            if current_date == existing_date:
                state = adv_obj.state
                amount = adv_obj.advance
                for result in res:
                    if state == 'approve' and amount != 0 and result.get('code') == 'SAR':
                        result['amount'] = amount
                        result['sa_id'] = adv_obj.id
        return res

    @api.multi
    def action_payslip_done(self):
        for line in self.input_line_ids:
            if line.sa_id:
                line.sa_id.paid = True
        return super(SalaryRuleInput, self).action_payslip_done()
