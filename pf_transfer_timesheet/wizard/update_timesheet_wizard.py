# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class UpdateTimesheetWizard(models.TransientModel):
    _name = 'update.timesheet.wizard'
    _description = 'Update Timesheet Wizard'

    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        domain="[('allow_timesheets', '=', True)]"
    )
    task_id = fields.Many2one(
        'project.task',
        string='Task',
        domain="[('project_id', '=', project_id), ('allow_timesheets', '=', True)]"
    )

    def action_update_timesheet(self):
        self.ensure_one()
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return

        # Sanitize active_ids to ensure integer IDs (protects against Odoo sample data strings like 'virtual_1')
        valid_ids = [int(i) for i in active_ids if isinstance(i, (int, float)) or (isinstance(i, str) and i.isdigit())]

        if not valid_ids:
            return

        lines = self.env['account.analytic.line'].browse(valid_ids)
        update_vals = {'project_id': self.project_id.id}
        if self.task_id:
            update_vals['task_id'] = self.task_id.id
        else:
            update_vals['task_id'] = False

        lines.write(update_vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
