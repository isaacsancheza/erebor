import re
import json
import requests


class Erebor:
    def __init__(self, filename, site_id='MLM'):
        self._site_id = site_id
        self._api_root = 'https://api.mercadolibre.com'
        self._filename = filename
        self._response = None
        self._access_token = None

        self._refresh_token()

    def _request(self, *args, include_token=True, refresh_token=False, **kwargs):

        method = 'GET'
        headers = dict()
        resource = self._construct_url(*args)

        string = resource.replace(self._api_root, '')
        rgx_items = r'^/items/(?P<item_id>\d+)(/[0-9A-Za-z_/]+)?$'

        match = re.match(rgx_items, string)
        if match:
            resource = resource.replace(match.group('item_id'), f'{self._site_id + match.group("item_id")}')

        if 'headers' in kwargs:
            headers = kwargs.pop('headers')
        if include_token:
            headers['Authorization'] = f'Bearer {self._access_token}'

        keys = ['post', 'put', 'delete']
        for key in keys:
            if key in kwargs:
                method = kwargs.pop(key).upper()
                break

        response = requests.request(method, resource, headers=headers, **kwargs)
        self._response = response

        data = response.json()
        error = data.get('error', None)
        status_code = response.status_code

        if error == 'invalid_grant' and include_token and not refresh_token:
            self._refresh_token()
            self._request(method, *args, refresh_token=True, **kwargs)

        return status_code, data

    def _construct_url(self, resource, *args):
        return '/'.join((self._api_root, resource,) + tuple(str(arg) for arg in args))

    def _refresh_token(self):
        with open(self._filename, 'r') as f:
            credentials = json.loads(f.read())
            self._access_token = credentials['access_token']

    def my(self, *args, **kwargs):
        return self._request('my', *args, **kwargs)

    def users(self, *args, **kwargs):
        return self._request('users', *args, **kwargs)

    def items(self, *args, **kwargs):
        return self._request('items', *args, **kwargs)

    def sites(self, *args, **kwargs):
        return self._request('sites', *args, **kwargs)

    def orders(self, *args, **kwargs):
        return self._request('orders', *args, **kwargs)

    def answers(self, *args, **kwargs):
        return self._request('answers', *args, **kwargs)

    def myfeeds(self, *args, **kwargs):
        return self._request('myfeed', *args, **kwargs)

    def feedback(self, *args, **kwargs):
        return self._request('feedback', *args, **kwargs)

    def questions(self, *args, **kwargs):
        return self._request('questions', *args, **kwargs)

    def shipments(self, *args, **kwargs):
        return self._request('shipments', *args, **kwargs)

    def categories(self, *args, **kwargs):
        return self._request('categories', *args, **kwargs)

    def site_domains(self, *args, **kwargs):
        return self._request('site_domains', *args, **kwargs)
