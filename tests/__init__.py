class HTTPResponseException(Exception):
    def __init__(self, response, path):
        self.response = response
        self.path = path
        self.message = self.get_message()
        super().__init__(self.message)

    def get_message(self):
        code = self.response.status_code
        path = self.path

        mapping = {
            401: f'Authorization needed for {path}',
            403: f'Access to {path} is forbidden',
            404: f'Not found {path}',
            '3xx': f'Redirect on {path}',
            '4xx': f'Wrong request to {path}',
            '5xx': f'Server can\'t handle request to {path}'
        }

        known_error = mapping.get(code)

        if known_error:
            return known_error
        if code < 400:
            return mapping['3xx']
        if code < 500:
            return mapping['4xx']
        if code >= 500:
            return mapping['5xx']

        return f'Unknown http error code {code}'