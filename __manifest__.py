# -*- coding: utf-8 -*-
{
    "name": "Custom Clients",
    "version": "1.0",
    "summary": "Módulo personalizado para gestionar clientes",
    "description": "Este módulo permite gestionar clientes de manera personalizada.",
    "author": "Nathaly García",
    "category": "Custom",
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'views/custom_client_views.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
