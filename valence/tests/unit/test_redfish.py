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

import mock
from unittest import TestCase

from valence import config as cfg
from valence.redfish import redfish
from valence.tests.unit import fakes


class TestRedfish(TestCase):

    def test_get_rfs_url_no_service_ext(self):
        expected = cfg.podm_url + "/redfish/v1/Systems/1"
        result = redfish.get_rfs_url("Systems/1")
        self.assertEqual(expected, result)

    def test_get_rfs_url_with_service_ext(self):
        expected = cfg.podm_url + "/redfish/v1/Systems/1"
        result = redfish.get_rfs_url("/redfish/v1/Systems/1")
        self.assertEqual(expected, result)

    @mock.patch('requests.request')
    def test_send_request(self, mock_request):
        mock_request.return_value = "fake_node"
        result = redfish.send_request("Nodes/1")
        self.assertEqual("fake_node", result)

    @mock.patch('valence.redfish.redfish.send_request')
    def test_filter_chassis_rack(self, mock_request):
        fake_chassis_list = fakes.fake_chassis_list()
        first_request = fakes.mock_request_get(fake_chassis_list[0], "200")
        second_request = fakes.mock_request_get(fake_chassis_list[1], "200")
        third_request = fakes.mock_request_get(fake_chassis_list[2], "200")
        mock_request.side_effect = [first_request,
                                    second_request,
                                    third_request]
        chassis = {"Members":
                   [{"@odata.id": "1"},
                    {"@odata.id": "2"},
                    {"@odata.id": "3"}]}
        expected = {'Members': [
            {u'@odata.id': u'2'},
            {u'@odata.id': u'3'}
        ], 'Members@odata.count': 2}
        result = redfish.filter_chassis(chassis, "Rack")
        self.assertEqual(expected, result)

    def test_generic_filter(self):
        filter_condition = {"Id": "1"}
        json_content_pass = {"Name": "Pass",
                             "Id": "1"}
        result = redfish.generic_filter(json_content_pass,
                                        filter_condition)
        self.assertTrue(result)
        json_content_fail = {"Name": "Fail",
                             "Id": "2"}
        result = redfish.generic_filter(json_content_fail,
                                        filter_condition)
        self.assertFalse(result)
        json_content_fail_2 = {"Name": "Fail2"}
        result = redfish.generic_filter(json_content_fail_2,
                                        filter_condition)
        self.assertFalse(result)

    @mock.patch('valence.redfish.redfish.send_request')
    def test_urls2list_no_members(self, mock_request):
        resp = {"Name": "NoMembers", "Id": 1}
        mock_request.return_value = fakes.mock_request_get(resp, "200")
        result = redfish.urls2list('/redfish/v1/test')
        self.assertEqual([], result)

    @mock.patch('valence.redfish.redfish.send_request')
    def test_urls2list_members(self, mock_request):
        resp = {"Name": "Members", "Id": 1,
                "Members":
                [{"@odata.id": "/redfish/v1/Member/1"},
                 {"@odata.id": "/redfish/v1/Member/2"}]}
        mock_request.return_value = fakes.mock_request_get(resp, "200")
        expected = ["/redfish/v1/Member/1", "/redfish/v1/Member/2"]
        result = redfish.urls2list('/redfish/v1/test')
        self.assertEqual(expected, result)