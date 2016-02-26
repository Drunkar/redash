import json
import logging
import requests

from redash.destinations import *


class Slack(BaseDestination):

    @classmethod
    def configuration_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'url': {
                    'type': 'string',
                    'title': 'Slack webhook URL'
                }
            }
        }

    def notify(self, alert_id, query_id, user_id, new_state, app, host, options):
        msg = "Check <{host}/alerts/{alert_id}|alert> / check <{host}/queries/{query_id}|query>".format(
            host=host, alert_id=alert_id, query_id=query_id)
        payload = {'text': msg}
        try:
            resp = requests.post(options.get('url'), data=json.dumps(payload))
            logging.warning(resp.text)
            if resp.status_code != 200:
                logging.error("Slack send ERROR. status_code => {status}".format(status=resp.status_code))
        except Exception:
            logging.exception("Slack send ERROR.")


register(Slack)
