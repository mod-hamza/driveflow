from odoo import models, fields, api

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _check_unique_name = models.Constraint("UNIQUE(name)", "Property tag name must be unique.")
