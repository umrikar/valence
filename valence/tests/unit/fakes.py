#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json


def mock_request_get(json_data, status_code):

    class MockResponse(object):
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return json.dumps(self.json_data)

    return MockResponse(json_data, status_code)


def fake_chassis_list():
    return [
        {
            "Id": "1",
            "ChassisType": "Pod",
            "Name": "Pod 1"
        },
        {
            "Id": "2",
            "ChassisType": "Rack",
            "Name": "Rack 1"
        },
        {
            "Id": "3",
            "ChassisType": "Rack",
            "Name": "Rack 2"
        }
    ]
