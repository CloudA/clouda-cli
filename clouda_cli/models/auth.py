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
