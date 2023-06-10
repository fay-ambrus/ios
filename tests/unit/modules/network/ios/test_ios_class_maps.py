#
# (c) 2023, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.ios.plugins.modules import ios_class_maps
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


class TestIosClassMapsModule(TestIosModule):
    module = ios_class_maps

    def setUp(self):
        super(TestIosClassMapsModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection"
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection"
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.class_maps.class_maps."
            "Class_mapsFacts.get_class_map_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosClassMapsModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_ios_class_maps_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
                Current configuration : 372 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-any test-class-map1
                 match access-group 1000
                 match access-group name test_acl
                 match application citrix source cli
                class-map match-all test-class-map2
                 match any
                class-map match-any test-class-map3
                  description This is a test description.
                 match application attribute media-type audio-video
                !
                !
                end
            """
        )
        module_args = {
            "config": [
                {
                    "name": "test-class-map3",
                    "match_type": "match-any",
                    "matches": [{"application_group": "telepresence-group"}],
                },
                {
                    "name": "new_class",
                    "class_type": "standard",
                    "match_type": "match-all",
                    "matches": [{"cac_status": "admitted"}],
                },
                {
                    "name": "another_new_class",
                    "matches": [
                        {"class_map": "test-class-map1"},
                        {"cos": [4, 1, 6], "negate": True},
                    ],
                },
                {
                    "name": "yet_another_class_map",
                    "match_type": "match-any",
                    "description": "yet another class description.",
                    "matches": [
                        {"cos_inner": [1, 2, 3, 4, 5, 6, 7]},
                        {"destination_mac_address": "1234:5678:9aBc", "negate": True},
                    ],
                },
            ],
            "state": "merged",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=True)
        commands = [
            "class-map match-any test-class-map3",
            "match application application-group telepresence-group",
            "class-map match-all new_class",
            "match cac status admitted",
            "class-map match-all another_new_class",
            "match class-map test-class-map1",
            "match not cos 1 4 6",
            "class-map match-any yet_another_class_map",
            "description yet another class description.",
            "match cos inner 1 2 3 4 5 6 7",
            "match not destination-address mac 1234.5678.9ABC",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_class_maps_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
                Current configuration : 305 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-all test-class1
                class-map match-all test-class3
                 match dscp default  cs1  af31  cs7  60
                class-map match-all test-class2
                 match discard-class 0
                 match security-group destination tag 100
                 match input-interface GigabitEthernet3
                !
                !
                end
            """
        )

        module_args = {
            "config": [
                {"name": "test-class1", "match_type": "match-all"},
                {"name": "test-class2", "class_type": "standard", "match_type": "match-all"},
                {
                    "name": "test-class3",
                    "matches": [
                        {
                            "dscp": {
                                "dscp_values": ["8", "0", "56", "af31", "60", "cs1"],
                                "ip_versions": "ipv4-and-ipv6",
                            }
                        }
                    ],
                },
            ],
            "state": "merged",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), [])

    def test_ios_class_maps_replaced(self):
        self.execute_show_command.return_value = dedent(
            """
                Current configuration : 348 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-all test-class1
                  description This is a test description.
                class-map match-any test-class2
                 match ip dscp default  7  af11  af23  af41  43  63
                 match ip precedence 5
                 match ip rtp 3000 1000
                !
                !
                end
            """
        )

        module_args = {
            "config": [
                {
                    "name": "test-class2",
                    "class_type": "standard",
                    "match_type": "match-any",
                    "description": "This is another test description.",
                    "matches": [
                        {"metadata": {"called_uri": "this_is_a_test_uri.test"}, "negate": True}
                    ],
                }
            ],
            "state": "replaced",
        }

        set_module_args(module_args)
        result = self.execute_module(changed=True)
        commands = [
            "class-map match-any test-class2",
            "description This is another test description.",
            "no match ip dscp 0 22 34 40 43 63 7",
            "no match ip precedence 5",
            "no match ip rtp 3000 1000",
            "match not metadata called-uri this_is_a_test_uri.test",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_class_maps_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
                Current configuration : 339 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-all test-class1
                class-map match-all test-class3
                  description This is a test description.
                class-map match-any test-class2
                 match metadata device-model this_is_a_device_model
                 match mpls experimental topmost 0  1  2  3  4
                 match packet length min 100 max 1000
                !
                !
                end
            """
        )
        module_args = {
            "config": [
                {"name": "test-class1"},
                {
                    "name": "test-class2",
                    "match_type": "match-any",
                    "matches": [
                        {"metadata": {"device_model": "this_is_a_device_model"}},
                        {"mpls_experimental_topmost": [0, 1, 2, 3, 4]},
                        {"packet_length": {"min": 100, "max": 1000}},
                    ],
                },
                {"name": "test-class3", "description": "This is a test description."},
            ],
            "state": "replaced",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), [])

    def test_ios_class_maps_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
                Current configuration : 365 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-all test-class1
                class-map match-all test-class3
                  description This is a test description.
                 match security-group destination tag 100
                class-map match-any test-class2
                 match protocol http server "example-server.com"
                 match protocol attribute category consumer-internet
                 match qos-group 70
                !
                !
                end
            """
        )
        module_args = {
            "config": [
                {
                    "name": "new-test-class",
                    "match_type": "match-any",
                    "matches": [
                        {"source_mac_address": "abCd:1243:87bf", "negate": True},
                        {"traffic_category": "optimize"},
                    ],
                }
            ],
            "state": "overridden",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=True)
        commands = [
            "no class-map match-all test-class1",
            "no class-map match-all test-class3",
            "no class-map match-any test-class2",
            "class-map match-any new-test-class",
            "match not source-address mac ABCD.1243.87BF",
            "match traffic-category optimize",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_class_maps_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
                Current configuration : 309 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-all test-class1
                class-map match-all test-class3
                  description This is a test description.
                 match ip precedence 7
                class-map match-any test-class2
                 match vlan  100
                 match vlan inner  20
                 match not dscp 21  af32  af43  cs5  43  ef
                !
                !
                end
            """
        )
        module_args = {
            "config": [
                {"name": "test-class1"},
                {
                    "name": "test-class3",
                    "description": "This is a test description.",
                    "matches": [{"ip_precedence": [7]}],
                },
                {
                    "name": "test-class2",
                    "matches": [
                        {"vlan": 100},
                        {"vlan_inner": 20},
                        {
                            "dscp": {"dscp_values": [21, "af32", "af43", "cs5", "43", "ef"]},
                            "negate": True,
                        },
                    ],
                },
            ],
            "state": "overridden",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), [])

    def test_ios_class_maps_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
                Current configuration : 372 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-any test-class-map1
                 match access-group 1000
                 match access-group name test_acl
                 match application citrix source cli
                class-map match-all test-class-map2
                 match any
                class-map match-any test-class-map3
                  description This is a test description.
                 match application attribute media-type audio-video
                !
                !
                end
            """
        )
        module_args = {
            "config": [
                {
                    "name": "test-class-map1",
                    "match_type": "match-any",
                    "matches": [
                        {"access_group": {"number": 1000}},
                        {"access_group": {"name": "test_acl"}},
                        {"application": {"name": "citrix", "source": "cli"}},
                    ],
                },
                {"name": "test-class-map2", "matches": [{"any": True}]},
            ],
            "state": "deleted",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=True)
        commands = [
            "no class-map match-any test-class-map1",
            "no class-map match-all test-class-map2",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_class_maps_deleted_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
                Current configuration : 305 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-all test-class1
                class-map match-all test-class3
                 match dscp default  cs1  af31  cs7  60
                class-map match-all test-class2
                 match discard-class 0
                 match security-group destination tag 100
                 match input-interface GigabitEthernet3
                !
                !
                end
            """
        )

        module_args = {
            "config": [
                {"name": "test-class4", "match_type": "match-all"},
                {"name": "test-class5", "class_type": "standard", "match_type": "match-all"},
            ],
            "state": "deleted",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), [])

    def test_ios_class_maps_rendered(self):
        module_args = {
            "config": [
                {
                    "name": "test-class1",
                    "class_type": "standard",
                    "match_type": "match-any",
                    "description": "This is a test description.",
                    "matches": [
                        {"metadata": {"global_session_id": "test_session_id"}, "negate": True},
                        {"packet_length": {"max": 1500}},
                        {"protocol": {"protocol_name": "dns"}, "negate": True},
                    ],
                }
            ],
            "state": "rendered",
        }
        set_module_args(module_args)
        commands = [
            "class-map match-any test-class1",
            "description This is a test description.",
            "match not metadata global-session-id test_session_id",
            "match packet length max 1500",
            "match not protocol dns",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_ios_class_maps_parsed(self):
        module_args = {
            "running_config": """\
                class-map match-all test-class1
                class-map match-all test-class3
                  description This is a test description.
                class-map match-any test-class2
                 match metadata device-model this_is_a_device_model
                 match mpls experimental topmost 0  1  2  3  4
                 match packet length min 100 max 1000
            """,
            "state": "parsed",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=False)
        parsed_list = [
            {"name": "test-class1", "match_type": "match-all", "class_type": "standard"},
            {
                "name": "test-class3",
                "match_type": "match-all",
                "class_type": "standard",
                "description": "This is a test description.",
            },
            {
                "name": "test-class2",
                "match_type": "match-any",
                "class_type": "standard",
                "matches": [
                    {"metadata": {"device_model": "this_is_a_device_model"}},
                    {"mpls_experimental_topmost": [0, 1, 2, 3, 4]},
                    {"packet_length": {"min": 100, "max": 1000}},
                ],
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_ios_class_maps_overridden_description_1(self):
        self.execute_show_command.return_value = dedent(
            """\
                Current configuration : 365 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-all test-class1
                class-map match-all test-class3
                  description This is a test description.
                 match security-group destination tag 100
                class-map match-any test-class2
                 match protocol http server "example-server.com"
                 match protocol attribute category consumer-internet
                 match qos-group 70
                !
                !
                end
            """
        )
        module_args = {
            "config": [{"name": "test-class3", "description": "This a new description."}],
            "state": "overridden",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=True, sort=True)
        cmds = [
            "class-map match-all test-class3",
            "description This a new description.",
            "no match security-group destination tag 100",
            "no class-map match-any test-class2",
            "no class-map match-all test-class1",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(cmds))

    def test_ios_class_maps_overridden_description_2(self):
        self.execute_show_command.return_value = dedent(
            """\
                Current configuration : 178 bytes
                !
                Configuration of Partition - class-map
                !
                !
                !
                !
                !
                !
                class-map match-all test-class
                description This is a test description.
                match cos  0  2
                match cos inner  5  6
                !
                !
                end
            """
        )
        module_args = {
            "config": [
                {
                    "name": "test-class",
                    "description": "This is another description.",
                    "matches": [{"vlan": 100, "negate": True}],
                }
            ],
            "state": "overridden",
        }
        set_module_args(module_args)
        result = self.execute_module(changed=True)
        commands = [
            "class-map match-all test-class",
            "description This is another description.",
            "no match cos 0 2",
            "no match cos inner 5 6",
            "match not vlan 100",
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))
