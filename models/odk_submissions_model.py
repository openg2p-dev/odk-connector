# -*- coding: utf-8 -*-

from odoo import _
from odoo import api, fields, models
from .odk import ODK


class ODKSubmissions(models.Model):
    _name = 'odk.submissions'
    _description = 'ODK Form Submissions'
    _order = 'submission_date'

    # Columns
    odk_submission_id = fields.Char(
        string='ODK Submission Instance ID',
        required=True,
        index=True,
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
    odoo_corresponding_id = fields.Many2one(
        'openg2p.registration',
        string="OpenG2P Registration",
        help="Registration linked to the submission.",
        readonly=True
    )

    # Entrypoint for submissions class. This will be called by other classes. TODO: Change to take 'config' as argument
    def submissions_entry(self, odk_config):
        odk_response_data = self.get_data_from_odk(odk_config)
        print("get_data_from_odk: ", odk_response_data)

        for value in odk_response_data:
            # Add check if the record already exists in the database
            existing_object = self.search([('odk_submission_id', '=', value.get('__id'))])
            if len(existing_object) >= 1:
                print("Submissions with Id: ", value.get('__id'), " already exists.Skipping.")

            else:
                registration = self.create_registration_from_submission(value)
                print("create_registration_from_submission: ", registration)
                self.odk_create_submissions_data(value,
                                                 {'odk_config_id': odk_config.id,
                                                  'odoo_corresponding_id': registration.id})
                print("odk_create_submissions_data: ", "Completed")

        config = self.odk_update_configuration({'odk_last_sync_date': fields.Datetime.now()}, odk_config.id)
        print("Successfully update config:", config)

    # def get_data_from_odk(self, odk_link, odk_user, odk_password, odk_project, odk_form):
    def get_data_from_odk(self, odk_config):
        odk = ODK('submission', odk_config.odk_email, odk_config.odk_password)
        response = odk.get((odk_config.odk_project_id, odk_config.odk_form_id))
        return response['value']

    def create_registration_from_submission(self, data, extra_data=None):
        extra_data = extra_data and extra_data or {}
        map_dict = self.get_conversion_dict()
        res = {}
        for k, v in map_dict.items():
            if hasattr(self.env['openg2p.registration'], k) and data.get(v, False):
                res.update({k: data[v]})
                print("Interim step, res value: ", res)
        res.update(extra_data)
        registration = self.env['openg2p.registration'].create(res)
        return registration

    # Need to pass odoo_corresponding_id in extra_data
    def odk_create_submissions_data(self, data, extra_data=None):
        extra_data = extra_data and extra_data or {}
        res = {}
        res.update({
            'odk_submission_id': data.get('__id'),
            'submission_date': data.get('__system').get('submissionDate'),
            'submission_response': data,
        })
        res.update(extra_data)
        self.create(res)

    def odk_update_configuration(self, data, odk_config_id):
        return self.env['odk.config'].search([('id', '=', odk_config_id)]).write(data)

    def get_conversion_dict(self):
        return {
            "firstname": "firstname",
            "lastname": "lastname",
            "location_id": "location_id",
            "street": "street",
            "city": "city",
            "state_id": "state_id",
            "country_id": "country_id",
            "gender": "gender",
        }
