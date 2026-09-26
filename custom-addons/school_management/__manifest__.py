{
    'name': 'School Management',
    'version': '1.0',
    'summary': 'Basic school management system',
 
   'description': """
        School Management
        =================
        Manage students and school information.
    """,
    'category': 'Education',
    'author': 'Cherinet Kebede',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
    ],
    'installable': True,
    'application': True,
}
