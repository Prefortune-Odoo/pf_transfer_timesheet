import odoo
from odoo import api, SUPERUSER_ID

config_file = "/odoo18/odoo18.conf"
odoo.tools.config.parse_config(['-c', config_file])

dbname = "pf_transfer_timesheet_v19"
registry = odoo.modules.registry.Registry.new(dbname)

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    model = env['project.task']
    if 'user_skill_ids' in model._fields:
        print("SUCCESS: user_skill_ids is in project.task")
    else:
        print("FAILURE: user_skill_ids is MISSING from project.task")
        print("Available fields:", list(model._fields.keys()))
