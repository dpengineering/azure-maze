import requests
import base64
import json
from threading import Thread


class MixPanel(object):
    """
    Class to easily interact with MixPanel analytics to send events and values
    """
    MIXPANEL_URL = "http://api.mixpanel.com/track/?data="
    properties = {}

    def __init__(self, project_name, token):
        """
        Construct a new MixPanel Object
        :param project_name: name of the project
        :param token: MixPanel token of the project
        """
        self.properties.clear()
        self.add_property("token", token)
        self.add_property("distinct_id", project_name)
        self.event_name = None

    def set_event_name(self, event_name):
        """
        Set the event name
        :param event_name: name of the event
        :return: None
        """
        self.event_name = event_name

    def add_property(self, key, value):
        """
        Add a property
        :param key: Key of the property
        :param value: Value associated with the key property
        :return: None
        """
        self.properties[key] = value

    def http_post_request(self, url):
        """
        Send an HTML POST request to the given url
        :param url: url to send a POST request to
        :return: Results of the POST request, see requests.post()
        """
        requests.post(url)
    
    def send_event(self):
        """
        Send the event to Mixpanel
        :return: results of the HTML POST request, see http_post_request()
        """
        event = {}
        event['event'] = self.event_name
        event['properties'] = self.properties

        data = json.dumps(event)
        url = self.MIXPANEL_URL + base64.b64encode(data.encode("utf-8")).decode("utf-8")
        request = Thread(target=self.http_post_request, args=(url,))
        request.start()

