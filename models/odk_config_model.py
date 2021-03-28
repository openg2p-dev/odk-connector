# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ODKConfig(models.Model):
    _name = 'odk.config'
    _description = 'ODK Form Configuration'
    _order = 'id'

    # Columns
    odk_endpoint = fields.Char(
        string='ODK Base URL',
        required=True,
        readonly=True
    )
    odk_project_id = fields.Integer(
        string='ODK Project ID',
        required=True,
        readonly=True
    )
    odk_form_id = fields.Char(
        string='ODK Form ID',
        required=True,
        readonly=True
    )


