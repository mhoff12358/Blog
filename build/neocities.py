import requests

__version__ = '1.1.0'

class NeoCities:
    """NeoCities API client library.
    """

    def __init__(self, user=None, password=None, key=None, url="https://neocities.org"):
        """Initialize self.
        
        user is the same as your site name, you can leave user and password
        empty if you are only going to use the info method. As an alternative to
        using an user and password combination you can specify a key that you
        have previously generated using the /api/key endpoint.
        
        Keyword arguments:
        user -- user account (default None)
        password -- user password (default None)
        key -- API key generated using the /api/key endpoint (default None)
        url -- base URL to use for API calls (default "https://neocities.org")
        """
        parsed_url = requests.utils.urlparse(url)
        self.url = '{}://{}'.format(parsed_url.scheme, parsed_url.netloc)
        if key is None and user is not None and password is not None:
            self.auth = requests.auth.HTTPBasicAuth(user, password)
        else:
            self.auth = None
        port_part = ':{}'.format(parsed_url.port) if parsed_url.port else ''
        self.request_headers = {
            'Host': parsed_url.hostname + port_part,
            'User-Agent': 'neoapi/{}'.format(
                '.'.join(__version__.split('.')[:2])),
        }
        if key is not None:
            self.request_headers['Authorization'] = 'Bearer {}'.format(key)
        self.session = requests.Session()

    def _decode(self, response):
        """Decode a response.
        
        Convert a json response into a Python dict.
        """
        if response.status_code == 200:
            return response.json()
        try:
            data = response.json()
        except:
            data = response.text
        raise NeoCities.RequestError({'status_code': response.status_code,
            'data': data})

    def _get(self, method, args=None):
        """Execute a get request.
        
        Keyword arguments:
        method -- API method
        args -- dict, query string parameters and their valies (default None)
        """
        path = '/api/{}'.format(method)
        headers = self.request_headers.copy()
        headers['path'] = path
        response = self.session.get(self.url + path, auth=self.auth,
            headers=headers, params=args)
        return self._decode(response)

    def _post(self, method, args=None, files=None):
        """Execute a post request.
        
        Keyword arguments:
        method -- API method
        args -- dict, data to send as the POST data (default None)
        files -- dict, files to upload (default None)
        """
        path = '/api/{}'.format(method)
        headers = self.request_headers.copy()
        headers['path'] = path
        response = self.session.post(self.url + path, auth=self.auth,
            headers=headers, data=args, files=files)
        return self._decode(response)

    def key(self):
        """Retrieve an API key you can use instead your username and password.
        """
        return self._get('key')

    def info(self, sitename=None):
        """Retrieve information about a web site.
        
        This API call can be used without logging in but in that case you are
        required to specify a site name.
        If no site name is specified it will retrieve the information of the
        site belonging to the username specified in the __init__ method.
        
        Keyword arguments:
        sitename -- the site name to retrieve information from (default None)
        """
        if sitename is not None:
            return self._get('info', args={'sitename': sitename})
        return self._get('info')

    def list(self, path=None):
        """Return a list of files of your site.
        
        If path is not specified it will return a list of all files.
        
        Keyword arguments:
        path -- the path to list files from (default None)
        """
        if path is not None:
            return self._get('list', args={'path': path})
        return self._get('list')

    def upload(self, *files):
        """Upload files to your site.
        
        The files parameters must be a tuple with two items, the first one is
        the file name you want the file to have on NeoCities and the second one
        is the path of the file on your disk.
        
        Arguments:
        files -- a list of tuples in the required format
        """
        args = {}
        for f in files:
            args[f[0]] = open(f[1], 'rb')
        return self._post('upload', files=args)

    def delete(self, *filenames):
        """Delete files from your site.
        
        Arguments:
        filenames -- a list of file names to delete
        """
        return self._post('delete', args={'filenames[]': filenames})

    class RequestError(Exception):
        """Exception for signalling responses different than 200"""

