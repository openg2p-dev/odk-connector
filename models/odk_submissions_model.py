# -*- coding: utf-8 -*-

from odoo import _
from odoo import api, fields, models
from .odk import ODK


class ODKSubmissions(models.Model):
    _name = 'odk.submissions'
    _description = 'ODK Form Submissions'
    _order = 'submission_date'
    # _inherit = ['openg2p.registration']

    # Columns
    odk_submission_id = fields.Char(
        string='ODK Submission Instance ID',
        required=True,
        # readonly=True
    )
    submission_date = fields.Datetime(
        string='Submission Date Time in ODK',
        required=True,
        # readonly=True
    )
    odk_config_id = fields.Many2one(
        'odk.config',
        string='Configuration',
        required=True,
        # readonly=True
    )
    submission_response = fields.Char(
        string='Form Response',
        required=True,
        # readonly=True
    )
    odoo_corrosponding_id = fields.Many2one(
        'openg2p.registration',
        string="OpenG2P Registration",
        help="Registration linked to the submission."
    )

    # Entrypoint for submissions class. This will be called by other classes.
    def submissions_entry(self, odk_link, odk_user, odk_password, odk_project, odk_form):
        odk = ODK('submission', odk_user, odk_password)
        print("Printing from Submissions: ", odk.get((odk_project, odk_form)))





