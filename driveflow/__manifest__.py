{
    'name':'Drive Flow',
    'depends':['base', 'mail'],
    'application':True,
    'data' : [
        "views/driveflow_agreement_views.xml",
        "views/driveflow_car_views.xml",
        "views/driveflow_car_type_views.xml",
        "views/driveflow_extra_charge_views.xml",
        "views/res_partner_views.xml",
        "views/driveflow_menus.xml",
        "security/ir.model.access.csv"
    ]
}
