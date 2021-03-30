# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ODKConfig(models.Model):
    _name = 'odk.config'
    _description = 'ODK Form Configuration'
    _order = 'id'

    # Columns
    form_name = fields.Char(
        string="Form Name",
        required=True,
    )
    odk_endpoint = fields.Char(
        string='ODK Base URL',
        required=True,
        # readonly=True
    )
    odk_project_id = fields.Integer(
        string='ODK Project ID',
        required=True,
        # readonly=True
    )
    odk_form_id = fields.Char(
        string='ODK Form ID',
        required=True,
        # readonly=True
    )
    odk_email = fields.Char(
        string='ODK User EMail',
        required=True,
        # readonly=True
    )
    odk_password = fields.Char(
        string='ODK User Password',
        required=True,
        # readonly=True
    )
    is_active = fields.Boolean(
        string="Active",
        default=False
    )

    @api.multi
    def odk_button_update_submissions(self):
        print("Button Clicked = ", self.id)


