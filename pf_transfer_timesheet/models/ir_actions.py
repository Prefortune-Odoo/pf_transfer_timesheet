from collections import defaultdict
from odoo import api, fields, models, tools, _
from odoo.exceptions import MissingError
from odoo.tools import frozendict

class IrActions(models.Model):
    _inherit = 'ir.actions.actions'

    icon = fields.Char(string="Icon", help="FontAwesome or Odoo icon class, e.g., 'fa fa-exchange'")

    def _get_readable_fields(self):
        return super()._get_readable_fields() | {'icon'}

    @tools.ormcache('model_name', 'self.env.lang')
    def _get_bindings(self, model_name):
        cr = self.env.cr
        result = defaultdict(list)
        self.env.flush_all()
        cr.execute("""
            SELECT a.id, a.type, a.binding_type
              FROM ir_actions a
              JOIN ir_model m ON a.binding_model_id = m.id
             WHERE m.model = %s
          ORDER BY a.id
        """, [model_name])
        for action_id, action_model, binding_type in cr.fetchall():
            try:
                action = self.env[action_model].sudo().browse(action_id)
                fields = ['name', 'binding_view_types']
                for field in ('groups_id', 'res_model', 'sequence', 'icon'):
                    if field in action._fields:
                        fields.append(field)
                action = action.read(fields)[0]
                if action.get('groups_id'):
                    groups = self.env['res.groups'].browse(action['groups_id'])
                    action['groups_id'] = ','.join(ext_id for ext_id in groups._ensure_xml_id().values())
                result[binding_type].append(frozendict(action))
            except MissingError:
                continue

        if result.get('action'):
            result['action'] = tuple(sorted(result['action'], key=lambda vals: vals.get('sequence', 0)))
        return frozendict(result)
