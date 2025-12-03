{
    'name': 'Gestión de Clientes de Internet',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Clientes, planes, facturación mensual y cortes automáticos.',
    'author': 'Nathaly García',
    'website': 'https://www.allygo.dev',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/contract_sequence.xml',
        'data/survey_sequence.xml',
        'data/plan_data.xml',
        'data/cron_jobs.xml',
        'views/plan_views.xml',
        'views/client_views.xml',
        'views/invoice_views.xml',
        'views/contract_views.xml',
        'views/survey_views.xml',
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'assets': {
    'web.assets_backend': [
        'custom_clients/static/src/css/plan_form.css',
        'custom_clients/static/src/css/kanban_plans.css',
        'custom_clients/static/src/css/client_form.css',
        'custom_clients/static/src/css/contract.css',
        'custom_clients/static/src/css/survey_kanban.css',
        'custom_clients/static/src/js/survey_kanban.js',
        'custom_clients/static/src/js/survey_kanban_renderer.js',
    ],
    },

}
