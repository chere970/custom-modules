{
    'name':'Real Estate',
    'summary':'Test module',
    'version':'1.0',
    'depends':["crm"],
    'data':[
        'security/res_group.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menu.xml'
        ],
    'demo':[
        'demo/demo.xml'
        
    ],
    'installable':True,
    'application':True,
}