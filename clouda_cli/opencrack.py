import json
import requests


def api_request(url, token_id, data=None,
                method='POST', content_type='application/json'):
    """Manual Openstack API wrapper since some of the clients suck, and can't
    do what we want them to.

    Args:
        url (string) - full path for the request
        token_id (string) - The token ID to use, will re-auth through keystone.
        data (dict) - A dict of data that will get JSON dumped. if None is
                      passed, it's dropped completely.
        method (string) - HTTP Method, GET | POST | PUT | DELETE

    Returns (requests.Response)
    """

    headers = {
        'X-Auth-Token': token_id,
        'content-type': content_type
    }

    if data:
        if content_type == 'application/json':
            data = json.dumps(data)
        resp = requests.request(method, url, headers=headers,
                                data=data)
    else:
        resp = requests.request(method, url, headers=headers)

    return resp


class Auth(object):
    """docstring for AuthModel"""
    def __init__(self, method, body):
        self.method = method
        self.body = body

    def as_dict(self):
        return {
            "auth": {
                "identity": {
                    "methods": [self.method],
                    self.method: self.body
                }
            }
        }
