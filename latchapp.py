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
import time

from latchauth import LatchAuth


class LatchApp(LatchAuth):

    def __init__(self, app_id, secret_key):
        '''
        Create an instance of the class with the Application ID and secret obtained from Eleven Paths
        @param $app_id
        @param $secret_key
        '''
        super(LatchApp, self).__init__(app_id, secret_key)

    def pairWithId(self, account_id):
        return self._http("GET", self.API_PAIR_WITH_ID_URL + "/" + account_id)

    def pair(self, token):
        return self._http("GET", self.API_PAIR_URL + "/" + token)

    def status(self, account_id, silent=False, nootp=False):
        url = self.API_CHECK_STATUS_URL + "/" + account_id
        if nootp:
            url += '/nootp'
        if silent:
            url += '/silent'
        return self._http("GET", url)

    def operationStatus(self, account_id, operation_id, silent=False, nootp=False):
        url = self.API_CHECK_STATUS_URL + "/" + account_id + "/op/" + operation_id
        if nootp:
            url += '/nootp'
        if silent:
            url += '/silent'
        return self._http("GET", url)

    def unpair(self, account_id):
        return self._http("GET", self.API_UNPAIR_URL + "/" + account_id)

    def lock(self, account_id, operation_id=None):
        if operation_id == None:
            return self._http("POST", self.API_LOCK_URL + "/" + account_id)
        else:
            return self._http("POST", self.API_LOCK_URL + "/" + account_id + "/op/" + operation_id)

    def unlock(self, account_id, operation_id=None):
        if operation_id == None:
            return self._http("POST", self.API_UNLOCK_URL + "/" + account_id)
        else:
            return self._http("POST", self.API_UNLOCK_URL + "/" + account_id + "/op/" + operation_id)

    def history(self, account_id, from_t=0, to_t=None):
        if to_t is None:
            to_t = int(round(time.time() * 1000))
        return self._http("GET", self.API_HISTORY_URL + "/" + account_id + "/" + str(from_t) + "/" + str(to_t))

    def createOperation(self, parent_id, name, two_factor, lock_on_request):
        params = {'parentId': parent_id, 'name': name, 'two_factor': two_factor, 'lock_on_request': lock_on_request}
        return self._http("PUT", self.API_OPERATION_URL, None, params)

    def updateOperation(self, operation_id, name, two_factor, lock_on_request):
        params = {'name': name, 'two_factor': two_factor, 'lock_on_request': lock_on_request}
        return self._http("POST", self.API_OPERATION_URL + "/" + operation_id, None, params)

    def deleteOperation(self, operation_id):
        return self._http("DELETE", self.API_OPERATION_URL + "/" + operation_id)

    def getOperations(self, operation_id=None):
        if operation_id == None:
            return self._http("GET", self.API_OPERATION_URL)
        else:
            return self._http("GET", self.API_OPERATION_URL + "/" + operation_id)

    def getInstances(self, account_id, operation_id=None):
        if operation_id == None:
            return self._http("GET", self.API_INSTANCE_URL + "/" + account_id)
        else:
            return self._http("GET", self.API_INSTANCE_URL + "/" + account_id + "/op/" + operation_id)

    def instanceStatus(self, instance_id, account_id, operation_id=None, silent=False, nootp=False):
        if operation_id == None:
            url = self.API_CHECK_STATUS_URL + "/" + account_id + "/i/" + instance_id
        else:
            url = self.API_CHECK_STATUS_URL + "/" + account_id + "/op/" + operation_id + "/i/" + instance_id
        if nootp:
            url += '/nootp'
        if silent:
            url += '/silent'
        return self._http("GET", url)

    def createInstance(self, name, account_id, operation_id=None):
        # Only one at a time
        params = {'instances': name}
        if operation_id == None:
            return self._http("PUT", self.API_INSTANCE_URL + '/' + account_id, None, params)
        else:
            return self._http("PUT", self.API_INSTANCE_URL + '/' + account_id + '/op/' + operation_id, None, params)

    def updateInstance(self, instance_id, account_id, operation_id, name, two_factor, lock_on_request):
        params = {'name': name, 'two_factor': two_factor, 'lock_on_request': lock_on_request}

        if operation_id == None:
            return self._http("POST", self.API_INSTANCE_URL + "/" + account_id + '/i/' + instance_id, None, params)
        else:
            return self._http("POST", self.API_OPERATION_URL + "/" + account_id + '/op/' + operation_id + '/i/' + instance_id, None, params)

    def deleteInstance(self, instance_id, account_id, operation_id=None):
        if operation_id == None:
            return self._http("DELETE", self.API_INSTANCE_URL + "/" + account_id + '/i/' + instance_id)
        else:
            return self._http("DELETE", self.API_INSTANCE_URL + "/" + account_id + "/op/" + operation_id + "/i/" + instance_id)
