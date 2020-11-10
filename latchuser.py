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

from latchauth import LatchAuth


class LatchUser(LatchAuth):

    def __init__(self, user_id, secret_key):
        '''
        Create an instance of the class with the User ID and secret obtained from Eleven Paths
        @param $user_id
        @param $secret_key
        '''
        super(LatchUser, self).__init__(user_id, secret_key)

    def get_subscription(self):
        return self._http("GET", self.API_SUBSCRIPTION_URL)

    def create_application(self, name, two_factor, lock_on_request, contact_phone, contact_email):
        params = {
            'name': name,
            'two_factor': two_factor,
            'lock_on_request': lock_on_request,
            'contactPhone': contact_phone,
            'contactEmail': contact_email
        }

        return self._http("PUT", self.API_APPLICATION_URL, None, params)

    def remove_application(self, application_id):
        return self._http("DELETE", self.API_APPLICATION_URL + "/" + application_id)

    def get_applications(self):
        return self._http("GET", self.API_APPLICATION_URL)

    def update_application(self, application_id, name, two_factor, lock_on_request, contact_phone, contact_email):
        params = {
            'name': name,
            'two_factor': two_factor,
            'lock_on_request': lock_on_request,
            'contactPhone': contact_phone,
            'email': contact_email
        }
        return self._http("POST", self.API_APPLICATION_URL + "/" + application_id, None, params)