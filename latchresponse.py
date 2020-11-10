'''
 This library offers an API to use Latch in a python environment.
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

from error import Error
import json


class LatchResponse(object):
    '''
    This class models a response from any of the endpoints in the Latch API.
    It consists of a "data" and an "error" elements. Although normally only one of them will be
    present, they are not mutually exclusive, since errors can be non fatal, and therefore a response
    could have valid information in the data field and at the same time inform of an error.
    '''

    def __init__(self, json_string):
        '''
        @param $json a json string received from one of the methods of the Latch API
        '''
        json_object = json.loads(json_string)
        if "data" in json_object:
            self.data = json_object["data"]
        else:
            self.data = ""

        if "error" in json_object:
            self.error = Error(json_object["error"])
        else:
            self.error = ""

    def get_data(self):
        '''
        @return JsonObject the data part of the API response
        '''
        return self.data

    def set_data(self, data):
        '''
        @param $data the data to include in the API response
        '''
        self.data = json.loads(data)

    def get_error(self):
        '''
        @return Error the error part of the API response, consisting of an error code and an error message
        '''
        return self.error

    def set_error(self, error):
        '''
        @param $error an error to include in the API response
        '''
        self.error = Error(error)

    def to_json(self):
        '''
        @return a Json object with the data and error parts set if they exist
        '''
        json_response = {}

        if hasattr(self, "data"):
            json_response["data"] = self.data

        if hasattr(self, "error"):
            json_response["error"] = self.error

        return json_response