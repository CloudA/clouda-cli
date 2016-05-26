import json
import requests


def lookup_endpoint(catalog_type, url, tenant_id):
    """

    Args:
        catalog_type (string) - The type of api request we want to make
                     (compute, keystone, etc) by service name.
        url (string) - the path portion of the url that wants to be called.
    Returns (string)
    """
    ksc = build_keystone_client(token_id)
    token = get_keystone_token(ksc, token_id, tenant_id)

    # find the service in the token's catalog
    for service in token.serviceCatalog:
        if service["type"] == catalog_type:
            endpoint = service["endpoints"][0]["internalURL"]

    # Use requests to post to the API url, since the nova client blows
    server_url = "%s%s" % (endpoint, url)
    return server_url


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
