from odoo import models, fields, api, _
from odoo.exceptions import UserError

class UpdateTimesheetWizard(models.TransientModel):
    _name = 'pf.update.timesheet.wizard'
    _description = 'Update Timesheet Project and Task Wizard'

    project_id = fields.Many2one('project.project', string='Project', required=True)
    task_id = fields.Many2one('project.task', string='Task', required=True, domain="[('project_id', '=', project_id)]")

    def action_update_timesheet(self):
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}
        
       
        active_ids = [aid for aid in active_ids if isinstance(aid, int)]
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}

        timesheets = self.env['account.analytic.line'].sudo().browse(active_ids)
        
        
        if not self.env.user.has_group('pf_transfer_timesheet.group_update_timesheet_project_task'):
            raise UserError(_("You do not have permission to update timesheet project/task."))

      
        write_vals = {
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
        }
        if self.project_id.account_id:
            write_vals['account_id'] = self.project_id.account_id.id

        timesheets.write(write_vals)
        
        return {'type': 'ir.actions.act_window_close'}
