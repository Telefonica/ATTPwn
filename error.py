
'''
 This library offers an API to use Latch in a python environment.
 Copyright (C) 2013 Eleven Paths

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

import json


class Error(object):

    def __init__(self, json_data):
        '''
        Constructor
        '''

        self.code = json_data['code']
        self.message = json_data['message']

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def to_json(self):
        return {"code" : self.code, "message" : self.message}

    def __repr__(self):
        return json.dumps(self.to_json())

    def __str__(self):
        return self.__repr__()