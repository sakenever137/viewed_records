# -*- coding: utf-8 -*-
{
    "name": "Viewed Records History",
    "summary": """
        Viewed Records History""",
    "description": """
        Viewed Records History.
    """,
    "author": "Saken Serdaly",
    "category": "Technical",
    "version": "18.0.0.0",
    "depends": ['base','hr'],
    'images': [
        'static/description/banner.gif',
    ],
    "data": [
        'security/ir.model.access.csv',

        'data/cron_viewed_records_history.xml',

        'views/viewed_records_history.xml',
        'views/res_config_settings_views.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "assets": {
        "web.assets_backend": [
            "viewed_records/static/src/js/mark_as_viewed_widget.js",
        ]
    },
}
