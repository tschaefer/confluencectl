# Copyright (c) 2016, Tobias Schaefer
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of upmctl nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Core client functionality, common across all API requests (including performing
HTTP requests).
"""

from requests import Session, Request
from requests.exceptions import ConnectionError
from exception import ClientError


class Client(object):

    def __init__(self, base_url, base_auth):
        self.base_url = base_url
        self.base_auth = base_auth
        self.request = Request('None', base_url)
        if self.base_auth is not None:
            user, password = self.base_auth.split(':')
            self.request.auth = (user, password)
        self.response = None

    def _method(self, method, data=None, files=None):
        self.request.method = method
        if files:
            self.request.files = files
        if data:
            self.request.data = data
        preparation = self.request.prepare()
        session = Session()
        try:
            self.response = session.send(preparation)
        except ConnectionError as e:
            error = "Failed to establish a connection '%s'" % (self.base_url)
            raise ClientError(error)
        if self.response.status_code < 200 \
            or self.response.status_code > 299:
                error = "[%s] %s" % (self.response.status_code,
                                     self.response.reason)
                raise ClientError(error)

    def get(self):
        self._method('GET')

    def post(self, data=None, files=None):
        self._method('POST', data=data, files=files)

    def put(self, data=None, files=None):
        self._method('PUT', data=data, files=files)

    def delete(self, data=None, files=None):
        self._method('DELETE', data=data, files=files)
