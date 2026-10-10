# -*- coding: utf-8 -*-
{
    "name": "Tolo Todo",
    "version": "19.0.1.0.0",
    "category": "Productivity/Tolo Todo",
    "summary": "Junior live test starter: personal tasks (incomplete on purpose)",
    "description": """
Tolo Solutions — Junior live / take-home starter for Odoo 19.
Fill TODOs, fix the broken view inherit, install and demo.
    """,
    "author": "Tolo Solutions (hiring starter)",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/tolo_todo_security.xml",
        "security/ir.model.access.csv",
        "views/tolo_todo_task_views.xml",
    ],
    "installable": True,
    "application": True,
}
