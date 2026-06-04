
{
    'name': 'Transfer Timesheet to Other Project Task',
    'version': '15.0.1.0.0',
    'category': 'Services/Timesheets',
    'sequence': 10,
    'license': 'OPL-1',
    'summary': 'Transfer Timesheet to Other Project Task',
    'description': """
        The Transfer Timesheet to other Project/Tasks app helps businesses efficiently manage and update timesheet records directly from the Odoo Timesheet module. This module allows authorized users to select multiple timesheet entries and update their related Projects and Tasks in bulk using the Actions menu. A user-friendly popup wizard makes the update process simple and fast without opening each timesheet record individually. The app includes a dedicated permission option under Technical/Extra Rights in User Settings to control access securely. By default, the feature remains disabled to ensure better system control and data security. The module also automatically synchronizes related analytic account information whenever project or task details are updated. It supports smooth handling of large datasets and allows authorized users to manage timesheets across teams efficiently. After every update, the Timesheet List View refreshes instantly to display the latest changes in real time. This app reduces manual effort, improves operational productivity, and ensures accurate project tracking. It is an ideal solution for organizations looking to simplify and streamline timesheet management in Odoo.
    """,
    'author': 'Prefortune Technologies LLP',
    'website': "https://www.prefortune.com/",
    'maintainer': 'Prefortune Technologies LLP',
    "support": "odoo@prefortune.com",
    'currency': 'EUR',
    'price': '0.00',
    'depends': ['base', 'project', 'hr_timesheet', 'analytic'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/update_timesheet_wizard_views.xml',
        'views/timesheet_action_views.xml',
    ],
    'images': ["static/description/banner.png"],
    'installable': True,
    'application': False,
    'auto_install': False,
}
