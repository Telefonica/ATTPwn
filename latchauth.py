'''
 This library offers an API to use LatchAuth in a python environment.
 Copyright (C) 2013 Eleven Paths

 This library is free software you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

from latchresponse import LatchResponse
import logging
import time


class LatchAuth(object):
    API_VERSION = "1.0"
    API_HOST = "latch.elevenpaths.com"
    API_PORT = 443
    API_HTTPS = True
    API_PROXY = None
    API_PROXY_PORT = None
    API_CHECK_STATUS_URL = "/api/" + API_VERSION + "/status"
    API_PAIR_URL = "/api/" + API_VERSION + "/pair"
    API_PAIR_WITH_ID_URL = "/api/" + API_VERSION + "/pairWithId"
    API_UNPAIR_URL = "/api/" + API_VERSION + "/unpair"
    API_LOCK_URL = "/api/" + API_VERSION + "/lock"
    API_UNLOCK_URL = "/api/" + API_VERSION + "/unlock"
    API_HISTORY_URL = "/api/" + API_VERSION + "/history"
    API_OPERATION_URL = "/api/" + API_VERSION + "/operation"
    API_SUBSCRIPTION_URL = "/api/" + API_VERSION + "/subscription"
    API_APPLICATION_URL = "/api/" + API_VERSION + "/application"
    API_INSTANCE_URL = "/api/" + API_VERSION + "/instance"

    AUTHORIZATION_HEADER_NAME = "Authorization"
    DATE_HEADER_NAME = "X-11Paths-Date"
    AUTHORIZATION_METHOD = "11PATHS"
    AUTHORIZATION_HEADER_FIELD_SEPARATOR = " "

    UTC_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"

    X_11PATHS_HEADER_PREFIX = "X-11paths-"
    X_11PATHS_HEADER_SEPARATOR = ":"

    @staticmethod
    def set_host(host):
        '''
        @param $host The host to be connected with (http://hostname) or (https://hostname)
        '''
        if host.startswith("http://"):
            LatchAuth.API_HOST = host[len("http://"):]
            LatchAuth.API_PORT = 80
            LatchAuth.API_HTTPS = False
        elif host.startswith("https://"):
            LatchAuth.API_HOST = host[len("https://"):]
            LatchAuth.API_PORT = 443
            LatchAuth.API_HTTPS = True

    @staticmethod
    def set_proxy(proxy, port):
        '''
        Enable using a Proxy to connect through
        @param $proxy The proxy server
        @param $port The proxy port number
        '''
        LatchAuth.API_PROXY = proxy
        LatchAuth.API_PROXY_PORT = port

    @staticmethod
    def get_part_from_header(part, header):
        '''
        The custom header consists of three parts, the method, the appId and the signature.
        This method returns the specified part if it exists.
        @param $part The zero indexed part to be returned
        @param $header The HTTP header value from which to extract the part
        @return string the specified part from the header or an empty string if not existent
        '''
        if header:
            parts = header.split(LatchAuth.AUTHORIZATION_HEADER_FIELD_SEPARATOR)
            if len(parts) >= part:
                return parts[part]
        return ""

    @staticmethod
    def get_auth_method_from_header(authorization_header):
        '''
        @param $authorization_header Authorization HTTP Header
        @return string the Authorization method. Typical values are "Basic", "Digest" or "11PATHS"
        '''
        return LatchAuth.get_part_from_header(0, authorization_header)

    @staticmethod
    def get_appId_from_header(authorization_header):
        '''
        @param $authorization_header Authorization HTTP Header
        @return string the requesting application Id. Identifies the application using the API
        '''
        return LatchAuth.get_part_from_header(1, authorization_header)

    @staticmethod
    def get_signature_from_header(authorization_header):
        '''
        @param $authorization_header Authorization HTTP Header
        @return string the signature of the current request. Verifies the identity of the application using the API
        '''
        return LatchAuth.get_part_from_header(2, authorization_header)

    @staticmethod
    def get_current_UTC():
        '''
        @return a string representation of the current time in UTC to be used in a Date HTTP Header
        '''
        return time.strftime(LatchAuth.UTC_STRING_FORMAT, time.gmtime())

    def __init__(self, appId, secretKey):
        '''
        Create an instance of the class with the Application ID and secret obtained from Eleven Paths
        @param $appId
        @param $secretKey
        '''
        self.appId = appId
        self.secretKey = secretKey

    def _http(self, method, url, x_headers=None, params=None):
        '''
        HTTP Request to the specified API endpoint
        @param $string $url
        @param $string $x_headers
        @return LatchResponse
        '''
        try:
            # Try to use the new Python3 HTTP library if available
            import http.client as http
            import urllib.parse as urllib
        except:
            # Must be using Python2 so use the appropriate library
            import httplib as http
            import urllib

        auth_headers = self.authentication_headers(method, url, x_headers, None, params)
        if LatchAuth.API_PROXY != None:
            if LatchAuth.API_HTTPS:
                conn = http.HTTPSConnection(LatchAuth.API_PROXY, LatchAuth.API_PROXY_PORT)
                conn.set_tunnel(LatchAuth.API_HOST, LatchAuth.API_PORT)
            else:
                conn = http.HTTPConnection(LatchAuth.API_PROXY, LatchAuth.API_PROXY_PORT)
                url = "http://" + LatchAuth.API_HOST + url
        else:
            if LatchAuth.API_HTTPS:
                conn = http.HTTPSConnection(LatchAuth.API_HOST, LatchAuth.API_PORT)
            else:
                conn = http.HTTPConnection(LatchAuth.API_HOST, LatchAuth.API_PORT)

        try:
            all_headers = auth_headers
            if method == "POST" or method == "PUT":
                all_headers["Content-type"] = "application/x-www-form-urlencoded"
            if params is not None:
                parameters = urllib.urlencode(params)

                conn.request(method, url, parameters, headers=all_headers)
            else:
                conn.request(method, url, headers=auth_headers)

            response = conn.getresponse()

            response_data = response.read().decode('utf8')
            conn.close()
            ret = LatchResponse(response_data)
        except:
            ret = None

        return ret

    def sign_data(self, data):
        '''
        @param $data the string to sign
        @return string base64 encoding of the HMAC-SHA1 hash of the data parameter using {@code secretKey} as cipher key.
        '''
        from hashlib import sha1
        import hmac
        import binascii

        sha1_hash = hmac.new(self.secretKey.encode(), data.encode(), sha1)
        return binascii.b2a_base64(sha1_hash.digest())[:-1].decode('utf8')

    def authentication_headers(self, http_method, query_string, x_headers=None, utc=None, params=None):
        '''
        Calculate the authentication headers to be sent with a request to the API
        @param $http_method the HTTP Method, currently only GET is supported
        @param $query_string the urlencoded string including the path (from the first forward slash) and the parameters
        @param $x_headers HTTP headers specific to the 11-paths API. null if not needed.
        @param $utc the Universal Coordinated Time for the Date HTTP header
        @return array a map with the Authorization and Date headers needed to sign a Latch API request
        '''
        if not utc:
            utc = LatchAuth.get_current_UTC()

        utc = utc.strip()

        #logging.debug(http_method)
        #logging.debug(query_string)
        #logging.debug(utc)

        string_to_sign = (http_method.upper().strip() + "\n" +
                          utc + "\n" +
                          self.get_serialized_headers(x_headers) + "\n" +
                          query_string.strip())

        if params is not None:
            string_to_sign = string_to_sign + "\n" + self.get_serialized_params(params)

        authorization_header = (LatchAuth.AUTHORIZATION_METHOD + LatchAuth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.appId + LatchAuth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.sign_data(string_to_sign))

        headers = dict()
        headers[LatchAuth.AUTHORIZATION_HEADER_NAME] = authorization_header
        headers[LatchAuth.DATE_HEADER_NAME] = utc
        return headers

    def get_serialized_headers(self, x_headers):
        '''
        Prepares and returns a string ready to be signed from the 11-paths specific HTTP headers received
        @param $x_headers a non neccesarily ordered map (array without duplicates) of the HTTP headers to be ordered.
        @return string The serialized headers, an empty string if no headers are passed, or None if there's a problem such as non 11paths specific headers
        '''
        if x_headers:
            headers = dict((k.lower(), v) for k, v in x_headers.iteritems())
            headers.sort()
            serialized_headers = ""
            for key, value in headers:
                if not key.startsWith(LatchAuth.X_11PATHS_HEADER_PREFIX.lower()):
                    logging.error(
                        "Error serializing headers. Only specific " + LatchAuth.X_11PATHS_HEADER_PREFIX + " headers need to be singed")
                    return None
                serialized_headers += key + LatchAuth.X_11PATHS_HEADER_SEPARATOR + value + " "
            return serialized_headers.strip()
        else:
            return ""

    def get_serialized_params(self, params):
        try:
            # Try to use the new Python3 HTTP library if available
            import http.client as http
            import urllib.parse as urllib
        except:
            # Must be using Python2 so use the appropriate library
            import httplib as http
            import urllib
        if params:
            serialized_params = ""
            for key in sorted(params):
                serialized_params += key + "=" + urllib.quote_plus(params[key]) + "&"
            return serialized_params.strip("&")
        else:
            return ""
