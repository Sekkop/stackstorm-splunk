import splunklib.client as client
import splunklib.results as results

from st2common.runners.base_action import Action
from lib.base import SplunkBaseAction

__all__ = [
    'UpdateApp'
]


class UpdateApp(SplunkBaseAction):

    def run(self, instance, filepath):
        """stackstorm run method"""
        # Find config details
        if instance:
            splunk_config = self.config['splunk_instances'].get(instance)
        else:
            splunk_config = self.config['splunk_instances'].get('default')

        try:
            if splunk_config.get('splunkToken'):
                self.service = client.connect(
                    host=splunk_config.get('host'),
                    port=splunk_config.get('port'),
                    splunkToken=splunk_config.get('splunkToken'),
                    scheme=splunk_config.get('scheme'),
                    verify=splunk_config.get('verify'))
            else:
                self.service = client.connect(
                    host=splunk_config.get('host'),
                    port=splunk_config.get('port'),
                    username=splunk_config.get('username'),
                    password=splunk_config.get('password'),
                    scheme=splunk_config.get('scheme'),
                    verify=splunk_config.get('verify'))
        except BaseException as err:
            raise Exception(
                "Failed to connect to Splunk Instance {} with error {}".format(splunk_config, err)
            )

        params = {'name': filepath, "filename": True, "update": True}
        result = self.service.apps.post(**params)
        return result
