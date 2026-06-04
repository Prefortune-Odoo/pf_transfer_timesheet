from odoo import api, fields, models, _
from odoo.exceptions import UserError

class UpdateTimesheetWizard(models.TransientModel):
    _name = 'update.timesheet.wizard'
    _description = 'Update Timesheet Project and Task Wizard'

    project_id = fields.Many2one('project.project', string='Project', required=True)
    task_id = fields.Many2one(
        'project.task',
        string='Task',
        domain="[('project_id', '=', project_id), ('allow_timesheets', '=', True)]"
    )

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id and self.task_id.project_id != self.project_id:
            self.task_id = False

    def action_update_timesheet(self):
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}
        
        timesheets = self.env['account.analytic.line'].browse(active_ids)
        
        vals = {
            'project_id': self.project_id.id,
            'task_id': self.task_id.id if self.task_id else False,
        }
        
        
        account_id = False
        if self.task_id and hasattr(self.task_id, '_get_task_analytic_account_id'):
            task_account = self.task_id._get_task_analytic_account_id()
            if task_account:
                account_id = task_account.id
        if not account_id and self.project_id.analytic_account_id:
            account_id = self.project_id.analytic_account_id.id
            
        if account_id:
            vals['account_id'] = account_id

        timesheets.write(vals)
        return {'type': 'ir.actions.act_window_close'}
