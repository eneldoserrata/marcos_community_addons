from openerp import models, fields, api, _

class MultiHRPayslipWiz(models.TransientModel):
    _name = 'multi.hr.payslip.wiz'

    @api.multi
    def confirm_multi_hr_payslip(self):
    	hr_payslip_ids = self.env['hr.payslip'].browse(self._context.get('active_ids'))
    	for hr in hr_payslip_ids:
    		if hr.state == 'draft':
    			hr.hr_verify_sheet()
