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
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config",
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.class_maps.class_maps."
            "Class_mapsFacts.get_class_map_data",
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
                    "matches": [
                        {
                            "application_group": "telepresence-group"
                        }
                    ]
                },
                {
                    "name": "new_class",
                    "class_type": "standard",
                    "match_type": "match-all",
                    "matches": [
                        {
                            "cac_status": "admitted"
                        }
                    ]
                },
                {
                    "name": "another_new_class",
                    "matches": [
                        {
                            "class_map": "test-class-map1",
                        },
                        {
                            "cos": [4, 1, 6],
                            "negate": True
                        }
                    ]
                },
                {
                    "name": "yet_another_class_map",
                    "match_type": "match-any",
                    "description": "yet another class description.",
                    "matches": [
                        {
                            "cos_inner": [1, 2, 3, 4, 5, 6, 7]
                        },
                        {
                            "destination_mac_address": "1234:5678:9aBc",
                            "negate": True
                        }
                    ]
                }
            ],
            "state": "merged"
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
            "match not destination-address mac 1234.5678.9ABC"
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
                {
                    "name": "test-class1",
                    "match_type": "match-all",
                },
                {
                    "name": "test-class2",
                    "class_type": "standard",
                    "match_type": "match-all",
                },
                {
                    "name": "test-class3",
                    "matches": [
                        {
                            "dscp": {
                                "dscp_values": [ "8", "0", "56", "af31", "60", "cs1"],
                                "ip_versions": "ipv4-and-ipv6"
                            },
                        }
                    ]
                },
            ],
            "state": "merged"
        }
        set_module_args(module_args)
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), [])
        # self.execute_module(changed=False, commands=[], sort=True)

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
                        {
                            "metadata":  {
                                "called_uri": "this_is_a_test_uri.test"
                            },
                            "negate": True
                        }
                    ]
                },
            ],
            "state": "replaced"
        }

        set_module_args(module_args)
        result = self.execute_module(changed=True)
        commands = [
            "class-map match-any test-class2",
            "description This is another test description.",
            "no match ip dscp 0 22 34 40 43 63 7",
            "no match ip precedence 5",
            "no match ip rtp 3000 1000",
            "match not metadata called-uri this_is_a_test_uri.test"
        ]
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_acls_replaced_idempotent(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list test_acl
    #         Extended IP access list 110
    #             10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
    #             20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
    #             30 deny icmp object-group test_network_og any dscp ef ttl eq 10
    #         IPv6 access list R1_TRAFFIC
    #             deny tcp any eq www any eq telnet ack dscp af11 sequence 10
    #         Extended IP access list test_pre
    #             10 permit ip any any precedence internet
    #         """,
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 {
    #                     "afi": "ipv4",
    #                     "acls": [
    #                         {
    #                             "name": "110",
    #                             "acl_type": "extended",
    #                             "aces": [
    #                                 {
    #                                     "sequence": 10,
    #                                     "grant": "permit",
    #                                     "protocol": "tcp",
    #                                     "source": {
    #                                         "address": "198.51.100.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "destination": {"any": True, "port_protocol": {"eq": "22"}},
    #                                     "log": {"user_cookie": "testLog"},
    #                                 },
    #                                 {
    #                                     "sequence": 20,
    #                                     "grant": "deny",
    #                                     "protocol": "icmp",
    #                                     "source": {
    #                                         "address": "192.0.2.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "destination": {
    #                                         "address": "192.0.3.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "dscp": "ef",
    #                                     "ttl": {"eq": 10},
    #                                     "protocol_options": {"icmp": {"echo": True}},
    #                                 },
    #                                 {
    #                                     "sequence": 30,
    #                                     "grant": "deny",
    #                                     "protocol": "icmp",
    #                                     "source": {"object_group": "test_network_og"},
    #                                     "destination": {"any": True},
    #                                     "dscp": "ef",
    #                                     "ttl": {"eq": 10},
    #                                 },
    #                             ],
    #                         },
    #                         {"name": "test_acl", "acl_type": "standard"},
    #                         {
    #                             "name": "test_pre",
    #                             "acl_type": "extended",
    #                             "aces": [
    #                                 {
    #                                     "sequence": 10,
    #                                     "grant": "permit",
    #                                     "protocol": "ip",
    #                                     "source": {"any": True},
    #                                     "destination": {"any": True},
    #                                     "precedence": "internet",
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "acls": [
    #                         {
    #                             "name": "R1_TRAFFIC",
    #                             "aces": [
    #                                 {
    #                                     "sequence": 10,
    #                                     "grant": "deny",
    #                                     "protocol": "tcp",
    #                                     "source": {"any": True, "port_protocol": {"eq": "www"}},
    #                                     "destination": {
    #                                         "any": True,
    #                                         "port_protocol": {"eq": "telnet"},
    #                                     },
    #                                     "dscp": "af11",
    #                                     "protocol_options": {"tcp": {"ack": True}},
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #             ],
    #             state="replaced",
    #         ),
    #     )
    #     result = self.execute_module(changed=False)
    #     self.assertEqual(sorted(result["commands"]), [])

    # def test_ios_acls_overridden(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list test_acl
    #         Extended IP access list 110
    #             10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
    #             20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
    #             30 deny icmp object-group test_network_og any dscp ef ttl eq 10
    #         IPv6 access list R1_TRAFFIC
    #             deny tcp any eq www any eq telnet ack dscp af11 sequence 10
    #         """,
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     afi="ipv4",
    #                     acls=[
    #                         dict(
    #                             name="150",
    #                             aces=[
    #                                 dict(
    #                                     grant="deny",
    #                                     protocol_options=dict(tcp=dict(syn="true")),
    #                                     source=dict(
    #                                         address="198.51.100.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                         port_protocol=dict(eq="telnet"),
    #                                     ),
    #                                     destination=dict(
    #                                         address="198.51.110.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                         port_protocol=dict(eq="telnet"),
    #                                     ),
    #                                     dscp="ef",
    #                                     ttl=dict(eq=10),
    #                                 ),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #             state="overridden",
    #         ),
    #     )
    #     result = self.execute_module(changed=True)
    #     commands = [
    #         "no ipv6 access-list R1_TRAFFIC",
    #         "no ip access-list standard test_acl",
    #         "no ip access-list extended 110",
    #         "ip access-list extended 150",
    #         "deny tcp 198.51.100.0 0.0.0.255 eq telnet 198.51.110.0 0.0.0.255 eq telnet syn dscp ef ttl eq 10",
    #     ]
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_acls_overridden_idempotent(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list test_acl
    #         Extended IP access list 110
    #             10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
    #             20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
    #             30 deny icmp object-group test_network_og any dscp ef ttl eq 10
    #         Reflexive IP access list MIRROR
    #             permit tcp host 0.0.0.0 eq 22 host 192.168.0.1 eq 50200 (2 matches) (time left 123)
    #             permit tcp host 0.0.0.0 eq 22 host 192.168.0.1 eq 50201 (2 matches) (time left 345)
    #             permit tcp host 0.0.0.0 eq 22 host 192.168.0.1 eq 50202 (2 matches) (time left 678)
    #         IPv6 access list R1_TRAFFIC
    #             deny tcp any eq www any eq telnet ack dscp af11 sequence 10
    #         """,
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 {
    #                     "afi": "ipv4",
    #                     "acls": [
    #                         {
    #                             "name": "110",
    #                             "acl_type": "extended",
    #                             "aces": [
    #                                 {
    #                                     "sequence": 10,
    #                                     "grant": "permit",
    #                                     "protocol": "tcp",
    #                                     "source": {
    #                                         "address": "198.51.100.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "destination": {"any": True, "port_protocol": {"eq": "22"}},
    #                                     "log": {"user_cookie": "testLog"},
    #                                 },
    #                                 {
    #                                     "sequence": 20,
    #                                     "grant": "deny",
    #                                     "protocol": "icmp",
    #                                     "source": {
    #                                         "address": "192.0.2.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "destination": {
    #                                         "address": "192.0.3.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "dscp": "ef",
    #                                     "ttl": {"eq": 10},
    #                                     "protocol_options": {"icmp": {"echo": True}},
    #                                 },
    #                                 {
    #                                     "sequence": 30,
    #                                     "grant": "deny",
    #                                     "protocol": "icmp",
    #                                     "source": {"object_group": "test_network_og"},
    #                                     "destination": {"any": True},
    #                                     "dscp": "ef",
    #                                     "ttl": {"eq": 10},
    #                                 },
    #                             ],
    #                         },
    #                         {"name": "test_acl", "acl_type": "standard"},
    #                     ],
    #                 },
    #                 {
    #                     "afi": "ipv6",
    #                     "acls": [
    #                         {
    #                             "name": "R1_TRAFFIC",
    #                             "aces": [
    #                                 {
    #                                     "sequence": 10,
    #                                     "grant": "deny",
    #                                     "protocol": "tcp",
    #                                     "source": {"any": True, "port_protocol": {"eq": "www"}},
    #                                     "destination": {
    #                                         "any": True,
    #                                         "port_protocol": {"eq": "telnet"},
    #                                     },
    #                                     "dscp": "af11",
    #                                     "protocol_options": {"tcp": {"ack": True}},
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #             ],
    #             state="overridden",
    #         ),
    #     )
    #     result = self.execute_module(changed=False)
    #     command = []
    #     self.assertEqual(sorted(result["commands"]), sorted(command))

    # def test_ios_acls_deleted_afi_based(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list test_acl
    #         Extended IP access list 110
    #             10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
    #             20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
    #             30 deny icmp object-group test_network_og any dscp ef ttl eq 10
    #         IPv6 access list R1_TRAFFIC
    #             deny tcp any eq www any eq telnet ack dscp af11 sequence 10
    #         """,
    #     )
    #     set_module_args(dict(config=[dict(afi="ipv4")], state="deleted"))
    #     result = self.execute_module(changed=True)
    #     commands = ["no ip access-list extended 110", "no ip access-list standard test_acl"]
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_acls_deleted_acl_based(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list test_acl
    #         Extended IP access list 110
    #             10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
    #             20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
    #             30 deny icmp object-group test_network_og any dscp ef ttl eq 10
    #         IPv6 access list R1_TRAFFIC
    #             deny tcp any eq www any eq telnet ack dscp af11 sequence 10
    #         """,
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     afi="ipv4",
    #                     acls=[
    #                         dict(
    #                             name="110",
    #                             aces=[
    #                                 dict(
    #                                     grant="deny",
    #                                     protocol_options=dict(icmp=dict(echo="true")),
    #                                     sequence="10",
    #                                     source=dict(address="192.0.2.0", wildcard_bits="0.0.0.255"),
    #                                     destination=dict(
    #                                         address="192.0.3.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     dscp="ef",
    #                                     ttl=dict(eq=10),
    #                                 ),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #                 dict(
    #                     afi="ipv6",
    #                     acls=[
    #                         dict(
    #                             name="R1_TRAFFIC",
    #                             aces=[
    #                                 dict(
    #                                     grant="deny",
    #                                     protocol_options=dict(tcp=dict(ack="true")),
    #                                     sequence="10",
    #                                     source=dict(any="true", port_protocol=dict(eq="www")),
    #                                     destination=dict(
    #                                         any="true",
    #                                         port_protocol=dict(eq="telnet"),
    #                                     ),
    #                                     dscp="af11",
    #                                 ),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #             state="deleted",
    #         ),
    #     )
    #     result = self.execute_module(changed=True)
    #     commands = ["no ip access-list extended 110", "no ipv6 access-list R1_TRAFFIC"]
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_acls_rendered(self):
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     afi="ipv4",
    #                     acls=[
    #                         dict(
    #                             name="110",
    #                             acl_type="extended",
    #                             aces=[
    #                                 dict(
    #                                     grant="deny",
    #                                     sequence="10",
    #                                     remarks=["check for remark", "remark for acl 110"],
    #                                     protocol_options=dict(tcp=dict(syn="true")),
    #                                     source=dict(address="192.0.2.0", wildcard_bits="0.0.0.255"),
    #                                     destination=dict(
    #                                         address="192.0.3.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                         port_protocol=dict(eq="www"),
    #                                     ),
    #                                     dscp="ef",
    #                                     ttl=dict(eq=10),
    #                                 ),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #             state="rendered",
    #         ),
    #     )
    #     commands = [
    #         "ip access-list extended 110",
    #         "10 deny tcp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 eq www syn dscp ef ttl eq 10",
    #         "remark check for remark",
    #         "remark remark for acl 110",
    #     ]
    #     result = self.execute_module(changed=False)
    #     self.assertEqual(sorted(result["rendered"]), sorted(commands))

    # def test_ios_acls_parsed(self):
    #     set_module_args(
    #         dict(
    #             running_config="""IPv6 access list R1_TRAFFIC\n deny tcp any eq www any range 10 20 ack dscp af11 sequence 10
    #             20 permit icmp host 192.0.2.1 host 192.0.2.2 echo\n 30 permit icmp host 192.0.2.3 host 192.0.2.4 echo-reply""",
    #             state="parsed",
    #         ),
    #     )
    #     result = self.execute_module(changed=False)
    #     parsed_list = [
    #         {
    #             "afi": "ipv6",
    #             "acls": [
    #                 {
    #                     "name": "R1_TRAFFIC",
    #                     "aces": [
    #                         {
    #                             "sequence": 10,
    #                             "grant": "deny",
    #                             "protocol": "tcp",
    #                             "source": {"any": True, "port_protocol": {"eq": "www"}},
    #                             "destination": {
    #                                 "any": True,
    #                                 "port_protocol": {"range": {"start": 10, "end": 20}},
    #                             },
    #                             "dscp": "af11",
    #                             "protocol_options": {"tcp": {"ack": True}},
    #                         },
    #                         {
    #                             "sequence": 20,
    #                             "grant": "permit",
    #                             "protocol": "icmp",
    #                             "source": {"host": "192.0.2.1"},
    #                             "destination": {"host": "192.0.2.2"},
    #                             "protocol_options": {"icmp": {"echo": True}},
    #                         },
    #                         {
    #                             "sequence": 30,
    #                             "grant": "permit",
    #                             "protocol": "icmp",
    #                             "source": {"host": "192.0.2.3"},
    #                             "destination": {"host": "192.0.2.4"},
    #                             "protocol_options": {"icmp": {"echo_reply": True}},
    #                         },
    #                     ],
    #                 },
    #             ],
    #         },
    #     ]
    #     self.assertEqual(parsed_list, result["parsed"])

    # def test_ios_acls_parsed_matches(self):
    #     set_module_args(
    #         dict(
    #             running_config="""Standard IP access list R1_TRAFFIC\n10 permit 10.11.12.13 (2 matches)\n
    #             40 permit 128.0.0.0, wildcard bits 63.255.255.255 (2 matches)\n60 permit 134.107.136.0, wildcard bits 0.0.0.255 (1 match)""",
    #             state="parsed",
    #         ),
    #     )
    #     result = self.execute_module(changed=False)
    #     parsed_list = [
    #         {
    #             "afi": "ipv4",
    #             "acls": [
    #                 {
    #                     "name": "R1_TRAFFIC",
    #                     "acl_type": "standard",
    #                     "aces": [
    #                         {"sequence": 10, "grant": "permit", "source": {"host": "10.11.12.13"}},
    #                         {
    #                             "sequence": 40,
    #                             "grant": "permit",
    #                             "source": {
    #                                 "address": "128.0.0.0",
    #                                 "wildcard_bits": "63.255.255.255",
    #                             },
    #                         },
    #                         {
    #                             "grant": "permit",
    #                             "sequence": 60,
    #                             "source": {
    #                                 "address": "134.107.136.0",
    #                                 "wildcard_bits": "0.0.0.255",
    #                             },
    #                         },
    #                     ],
    #                 },
    #             ],
    #         },
    #     ]
    #     self.assertEqual(parsed_list, result["parsed"])

    # def test_ios_acls_overridden_remark(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list test_acl
    #         Extended IP access list 110
    #             10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log (tag = testLog)
    #             20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10
    #             30 deny icmp object-group test_network_og any dscp ef ttl eq 10
    #         access-list 110 remark test ab.
    #         access-list 110 remark test again ab.
    #         """,
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 {
    #                     "afi": "ipv4",
    #                     "acls": [
    #                         {
    #                             "name": "110",
    #                             "acl_type": "extended",
    #                             "aces": [{"remarks": ["test ab.", "test again ab."]}],
    #                         },
    #                         {"name": "test_acl", "acl_type": "standard"},
    #                     ],
    #                 },
    #             ],
    #             state="overridden",
    #         ),
    #     )
    #     result = self.execute_module(changed=True, sort=True)
    #     cmds = [
    #         "ip access-list extended 110",
    #         "no 10 permit tcp 198.51.100.0 0.0.0.255 any eq 22 log testLog",
    #         "no 20 deny icmp 192.0.2.0 0.0.0.255 192.0.3.0 0.0.0.255 echo dscp ef ttl eq 10",
    #         "no 30 deny icmp object-group test_network_og any dscp ef ttl eq 10",
    #     ]
    #     self.assertEqual(sorted(result["commands"]), cmds)

    # def test_ios_acls_overridden_option(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list test_acl
    #         ip access-list standard test_acl
    #             remark remark check 1
    #             remark some random remark 2
    #         """,
    #     )

    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     afi="ipv4",
    #                     acls=[
    #                         dict(
    #                             name="113",
    #                             acl_type="extended",
    #                             aces=[
    #                                 dict(
    #                                     grant="deny",
    #                                     protocol_options=dict(tcp=dict(ack="true")),
    #                                     source=dict(
    #                                         address="198.51.100.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     destination=dict(
    #                                         address="198.51.101.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                         port_protocol=dict(eq="telnet"),
    #                                     ),
    #                                     tos=dict(min_monetary_cost=True),
    #                                 ),
    #                                 dict(
    #                                     grant="permit",
    #                                     protocol_options=dict(protocol_number=433),
    #                                     source=dict(
    #                                         address="198.51.101.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     destination=dict(
    #                                         address="198.51.102.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                         port_protocol=dict(eq="telnet"),
    #                                     ),
    #                                     log=dict(user_cookie="check"),
    #                                     tos=dict(max_throughput=True),
    #                                 ),
    #                                 dict(
    #                                     grant="permit",
    #                                     source=dict(
    #                                         address="198.51.102.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     destination=dict(
    #                                         address="198.51.103.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     precedence=10,
    #                                     tos=dict(normal=True),
    #                                 ),
    #                                 dict(
    #                                     grant="permit",
    #                                     source=dict(
    #                                         address="198.51.105.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     destination=dict(
    #                                         address="198.51.106.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     time_range=20,
    #                                     tos=dict(max_throughput=True),
    #                                 ),
    #                             ],
    #                         ),
    #                         dict(
    #                             name="test_acl",
    #                             acl_type="standard",
    #                             aces=[dict(remarks=["Another remark here"])],
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #             state="overridden",
    #         ),
    #     )
    #     result = self.execute_module(changed=True)
    #     commands = [
    #         "ip access-list extended 113",
    #         "deny tcp 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 eq telnet ack tos min-monetary-cost",
    #         "permit 198.51.102.0 0.0.0.255 198.51.103.0 0.0.0.255 precedence 10 tos normal",
    #         "permit 433 198.51.101.0 0.0.0.255 198.51.102.0 0.0.0.255 eq telnet log check tos max-throughput",
    #         "permit 198.51.105.0 0.0.0.255 198.51.106.0 0.0.0.255 time-range 20 tos max-throughput",
    #         "ip access-list standard test_acl",
    #         "remark Another remark here",
    #         "no remark remark check 1",
    #         "no remark some random remark 2",
    #     ]
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_acls_overridden_clear(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         """,
    #     )

    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     afi="ipv4",
    #                     acls=[
    #                         dict(
    #                             name="113",
    #                             acl_type="extended",
    #                             aces=[
    #                                 dict(
    #                                     grant="deny",
    #                                     source=dict(
    #                                         address="198.51.100.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     destination=dict(
    #                                         address="198.51.101.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     tos=dict(max_reliability=True),
    #                                     enable_fragments=True,
    #                                 ),
    #                                 dict(
    #                                     remarks=["extended ACL remark"],
    #                                     grant="permit",
    #                                     source=dict(
    #                                         address="198.51.101.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     destination=dict(
    #                                         address="198.51.102.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     log=dict(user_cookie="check"),
    #                                     tos=dict(service_value="119"),
    #                                 ),
    #                             ],
    #                         ),
    #                         dict(
    #                             name="23",
    #                             acl_type="standard",
    #                             aces=[dict(remarks=["check remark here"])],
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #             state="overridden",
    #         ),
    #     )
    #     result = self.execute_module(changed=True)
    #     commands = [
    #         "ip access-list extended 113",
    #         "deny 198.51.100.0 0.0.0.255 198.51.101.0 0.0.0.255 fragments tos max-reliability",
    #         "permit 198.51.101.0 0.0.0.255 198.51.102.0 0.0.0.255 log check tos 119",
    #         "remark extended ACL remark",
    #         "ip access-list standard 23",
    #         "remark check remark here",
    #     ]
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))

    # def test_ios_delete_acl(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list 2
    #             30 permit 172.16.1.11
    #             20 permit 172.16.1.10 log
    #             10 permit 172.16.1.2
    #         """,
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     afi="ipv4",
    #                     acls=[
    #                         dict(
    #                             name="2",
    #                             aces=[
    #                                 dict(
    #                                     grant="permit",
    #                                     source=dict(host="192.0.2.1"),
    #                                     sequence=10,
    #                                 ),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #             state="deleted",
    #         ),
    #     )

    #     result = self.execute_module(changed=True)
    #     commands = ["no ip access-list standard 2"]
    #     self.assertEqual(result["commands"], commands)

    # def test_ios_failed_extra_param_standard_acl(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list test_acl
    #         ip access-list standard test_acl
    #             remark remark check 1
    #             remark some random remark 2
    #         """,
    #     )

    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     afi="ipv4",
    #                     acls=[
    #                         dict(
    #                             name="test_acl",
    #                             acl_type="standard",
    #                             aces=[
    #                                 dict(
    #                                     grant="deny",
    #                                     sequence=10,
    #                                     source=dict(
    #                                         address="198.51.100.0",
    #                                         wildcard_bits="0.0.0.255",
    #                                     ),
    #                                     destination=dict(any="True"),
    #                                 ),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #             state="overridden",
    #         ),
    #     )
    #     result = self.execute_module(failed=True)
    #     self.assertEqual(result, {"failed": True})

    # def test_ios_failed_update_with_merged(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         Standard IP access list test_acl
    #             30 permit 172.16.1.11
    #             20 permit 172.16.1.10 log
    #             10 permit 172.16.1.2
    #         """,
    #     )
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     afi="ipv4",
    #                     acls=[
    #                         dict(
    #                             name="test_acl",
    #                             aces=[
    #                                 dict(
    #                                     grant="permit",
    #                                     source=dict(host="192.0.2.1"),
    #                                     sequence=10,
    #                                 ),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #             state="merged",
    #         ),
    #     )

    #     result = self.execute_module(failed=True)
    #     self.assertEqual(
    #         result,
    #         {
    #             "msg": "Cannot update existing sequence 10 of ACLs test_acl with state merged. Please use state replaced or overridden.",
    #             "failed": True,
    #         },
    #     )

    # def test_ios_acls_parsed_multioption(self):
    #     set_module_args(
    #         dict(
    #             running_config=dedent(
    #                 """\
    #                 Standard IP access list 2
    #                     30 permit 172.16.1.11
    #                     20 permit 172.16.1.10
    #                     10 permit 172.16.1.2
    #                 Extended IP access list 101
    #                     15 permit tcp any host 172.16.2.9
    #                     18 permit tcp any host 172.16.2.11
    #                     20 permit udp host 172.16.1.21 any
    #                     30 permit udp host 172.16.1.22 any
    #                     40 deny icmp any 10.1.1.0 0.0.0.255 echo
    #                     50 permit ip any 10.1.1.0 0.0.0.255
    #                     60 permit tcp any host 10.1.1.1 eq telnet
    #                     70 permit tcp 10.1.1.0 0.0.0.255 172.16.1.0 0.0.0.255 eq telnet time-range EVERYOTHERDAY (active)
    #                 Extended IP access list outboundfilters
    #                     10 permit icmp 10.1.1.0 0.0.0.255 172.16.1.0 0.0.0.255
    #                 Extended IP access list test
    #                     10 permit ip host 10.2.2.2 host 10.3.3.3
    #                     20 permit tcp host 10.1.1.1 host 10.5.5.5 eq www
    #                     30 permit icmp any any
    #                     40 permit udp host 10.6.6.6 10.10.10.0 0.0.0.255 eq domain
    #                 Extended MAC access list system-cpp-bpdu-range
    #                     permit any 0180.c200.0000 0000.0000.0003
    #                 Extended MAC access list system-cpp-cdp
    #                     permit any host 0100.0ccc.cccc
    #                 """,
    #             ),
    #             state="parsed",
    #         ),
    #     )
    #     result = self.execute_module(changed=False)
    #     parsed_list = [
    #         {
    #             "afi": "ipv4",
    #             "acls": [
    #                 {
    #                     "name": "101",
    #                     "acl_type": "extended",
    #                     "aces": [
    #                         {
    #                             "sequence": 15,
    #                             "grant": "permit",
    #                             "protocol": "tcp",
    #                             "source": {"any": True},
    #                             "destination": {"host": "172.16.2.9"},
    #                         },
    #                         {
    #                             "sequence": 18,
    #                             "grant": "permit",
    #                             "protocol": "tcp",
    #                             "source": {"any": True},
    #                             "destination": {"host": "172.16.2.11"},
    #                         },
    #                         {
    #                             "sequence": 20,
    #                             "grant": "permit",
    #                             "protocol": "udp",
    #                             "source": {"host": "172.16.1.21"},
    #                             "destination": {"any": True},
    #                         },
    #                         {
    #                             "sequence": 30,
    #                             "grant": "permit",
    #                             "protocol": "udp",
    #                             "source": {"host": "172.16.1.22"},
    #                             "destination": {"any": True},
    #                         },
    #                         {
    #                             "sequence": 40,
    #                             "grant": "deny",
    #                             "protocol": "icmp",
    #                             "source": {"any": True},
    #                             "destination": {
    #                                 "address": "10.1.1.0",
    #                                 "wildcard_bits": "0.0.0.255",
    #                             },
    #                             "protocol_options": {"icmp": {"echo": True}},
    #                         },
    #                         {
    #                             "sequence": 50,
    #                             "grant": "permit",
    #                             "protocol": "ip",
    #                             "source": {"any": True},
    #                             "destination": {
    #                                 "address": "10.1.1.0",
    #                                 "wildcard_bits": "0.0.0.255",
    #                             },
    #                         },
    #                         {
    #                             "sequence": 60,
    #                             "grant": "permit",
    #                             "protocol": "tcp",
    #                             "source": {"any": True},
    #                             "destination": {
    #                                 "host": "10.1.1.1",
    #                                 "port_protocol": {"eq": "telnet"},
    #                             },
    #                         },
    #                         {
    #                             "sequence": 70,
    #                             "grant": "permit",
    #                             "protocol": "tcp",
    #                             "source": {"address": "10.1.1.0", "wildcard_bits": "0.0.0.255"},
    #                             "destination": {
    #                                 "address": "172.16.1.0",
    #                                 "port_protocol": {"eq": "telnet"},
    #                                 "wildcard_bits": "0.0.0.255",
    #                             },
    #                             "time_range": "EVERYOTHERDAY",
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "name": "2",
    #                     "acl_type": "standard",
    #                     "aces": [
    #                         {"sequence": 30, "grant": "permit", "source": {"host": "172.16.1.11"}},
    #                         {"sequence": 20, "grant": "permit", "source": {"host": "172.16.1.10"}},
    #                         {"sequence": 10, "grant": "permit", "source": {"host": "172.16.1.2"}},
    #                     ],
    #                 },
    #                 {
    #                     "name": "outboundfilters",
    #                     "acl_type": "extended",
    #                     "aces": [
    #                         {
    #                             "sequence": 10,
    #                             "grant": "permit",
    #                             "protocol": "icmp",
    #                             "source": {"address": "10.1.1.0", "wildcard_bits": "0.0.0.255"},
    #                             "destination": {
    #                                 "address": "172.16.1.0",
    #                                 "wildcard_bits": "0.0.0.255",
    #                             },
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "name": "test",
    #                     "acl_type": "extended",
    #                     "aces": [
    #                         {
    #                             "sequence": 10,
    #                             "grant": "permit",
    #                             "protocol": "ip",
    #                             "source": {"host": "10.2.2.2"},
    #                             "destination": {"host": "10.3.3.3"},
    #                         },
    #                         {
    #                             "sequence": 20,
    #                             "grant": "permit",
    #                             "protocol": "tcp",
    #                             "source": {"host": "10.1.1.1"},
    #                             "destination": {"host": "10.5.5.5", "port_protocol": {"eq": "www"}},
    #                         },
    #                         {
    #                             "sequence": 30,
    #                             "grant": "permit",
    #                             "protocol": "icmp",
    #                             "source": {"any": True},
    #                             "destination": {"any": True},
    #                         },
    #                         {
    #                             "sequence": 40,
    #                             "grant": "permit",
    #                             "protocol": "udp",
    #                             "source": {"host": "10.6.6.6"},
    #                             "destination": {
    #                                 "address": "10.10.10.0",
    #                                 "port_protocol": {"eq": "domain"},
    #                                 "wildcard_bits": "0.0.0.255",
    #                             },
    #                         },
    #                     ],
    #                 },
    #             ],
    #         },
    #     ]
    #     self.assertEqual(parsed_list, result["parsed"])

    # def test_ios_acls_rendered_muiltioption(self):
    #     set_module_args(
    #         dict(
    #             config=[
    #                 {
    #                     "afi": "ipv4",
    #                     "acls": [
    #                         {
    #                             "name": "101",
    #                             "acl_type": "extended",
    #                             "aces": [
    #                                 {
    #                                     "sequence": 15,
    #                                     "grant": "permit",
    #                                     "protocol": "tcp",
    #                                     "source": {"any": True},
    #                                     "destination": {"host": "172.16.2.9"},
    #                                 },
    #                                 {
    #                                     "sequence": 18,
    #                                     "grant": "permit",
    #                                     "protocol": "tcp",
    #                                     "source": {"any": True},
    #                                     "destination": {"host": "172.16.2.11"},
    #                                 },
    #                                 {
    #                                     "sequence": 20,
    #                                     "grant": "permit",
    #                                     "protocol": "udp",
    #                                     "source": {"host": "172.16.1.21"},
    #                                     "destination": {"any": True},
    #                                 },
    #                                 {
    #                                     "sequence": 30,
    #                                     "grant": "permit",
    #                                     "protocol": "udp",
    #                                     "source": {"host": "172.16.1.22"},
    #                                     "destination": {"any": True},
    #                                 },
    #                                 {
    #                                     "sequence": 40,
    #                                     "grant": "deny",
    #                                     "protocol": "icmp",
    #                                     "source": {"any": True},
    #                                     "destination": {
    #                                         "address": "10.1.1.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "protocol_options": {"icmp": {"echo": True}},
    #                                 },
    #                                 {
    #                                     "sequence": 50,
    #                                     "grant": "permit",
    #                                     "protocol": "ip",
    #                                     "source": {"any": True},
    #                                     "destination": {
    #                                         "address": "10.1.1.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                 },
    #                                 {
    #                                     "sequence": 60,
    #                                     "grant": "permit",
    #                                     "protocol": "tcp",
    #                                     "source": {"any": True},
    #                                     "destination": {
    #                                         "host": "10.1.1.1",
    #                                         "port_protocol": {"eq": "telnet"},
    #                                     },
    #                                 },
    #                                 {
    #                                     "sequence": 70,
    #                                     "grant": "permit",
    #                                     "protocol": "tcp",
    #                                     "source": {
    #                                         "address": "10.1.1.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "destination": {
    #                                         "address": "172.16.1.0",
    #                                         "port_protocol": {"eq": "telnet"},
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "time_range": "EVERYOTHERDAY",
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "name": "2",
    #                             "acl_type": "standard",
    #                             "aces": [
    #                                 {
    #                                     "sequence": 30,
    #                                     "grant": "permit",
    #                                     "source": {"host": "172.16.1.11"},
    #                                 },
    #                                 {
    #                                     "sequence": 20,
    #                                     "grant": "permit",
    #                                     "source": {"host": "172.16.1.10"},
    #                                 },
    #                                 {
    #                                     "sequence": 10,
    #                                     "grant": "permit",
    #                                     "source": {"host": "172.16.1.2"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "name": "outboundfilters",
    #                             "acl_type": "extended",
    #                             "aces": [
    #                                 {
    #                                     "sequence": 10,
    #                                     "grant": "permit",
    #                                     "protocol": "icmp",
    #                                     "source": {
    #                                         "address": "10.1.1.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                     "destination": {
    #                                         "address": "172.16.1.0",
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "name": "test",
    #                             "acl_type": "extended",
    #                             "aces": [
    #                                 {
    #                                     "sequence": 10,
    #                                     "grant": "permit",
    #                                     "protocol": "ip",
    #                                     "source": {"host": "10.2.2.2"},
    #                                     "destination": {"host": "10.3.3.3"},
    #                                 },
    #                                 {
    #                                     "sequence": 20,
    #                                     "grant": "permit",
    #                                     "protocol": "tcp",
    #                                     "source": {"host": "10.1.1.1"},
    #                                     "destination": {
    #                                         "host": "10.5.5.5",
    #                                         "port_protocol": {"eq": "www"},
    #                                     },
    #                                 },
    #                                 {
    #                                     "sequence": 30,
    #                                     "grant": "permit",
    #                                     "protocol": "icmp",
    #                                     "source": {"any": True},
    #                                     "destination": {"any": True},
    #                                 },
    #                                 {
    #                                     "sequence": 40,
    #                                     "grant": "permit",
    #                                     "protocol": "udp",
    #                                     "source": {"host": "10.6.6.6"},
    #                                     "destination": {
    #                                         "address": "10.10.10.0",
    #                                         "port_protocol": {"eq": "domain"},
    #                                         "wildcard_bits": "0.0.0.255",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #             ],
    #             state="rendered",
    #         ),
    #     )
    #     commands = [
    #         "ip access-list extended 101",
    #         "15 permit tcp any host 172.16.2.9",
    #         "18 permit tcp any host 172.16.2.11",
    #         "20 permit udp host 172.16.1.21 any",
    #         "30 permit udp host 172.16.1.22 any",
    #         "40 deny icmp any 10.1.1.0 0.0.0.255 echo",
    #         "50 permit ip any 10.1.1.0 0.0.0.255",
    #         "60 permit tcp any host 10.1.1.1 eq telnet",
    #         "70 permit tcp 10.1.1.0 0.0.0.255 172.16.1.0 0.0.0.255 eq telnet time-range EVERYOTHERDAY",
    #         "ip access-list standard 2",
    #         "30 permit host 172.16.1.11",
    #         "20 permit host 172.16.1.10",
    #         "10 permit host 172.16.1.2",
    #         "ip access-list extended outboundfilters",
    #         "10 permit icmp 10.1.1.0 0.0.0.255 172.16.1.0 0.0.0.255",
    #         "ip access-list extended test",
    #         "10 permit ip host 10.2.2.2 host 10.3.3.3",
    #         "20 permit tcp host 10.1.1.1 host 10.5.5.5 eq www",
    #         "30 permit icmp any any",
    #         "40 permit udp host 10.6.6.6 10.10.10.0 0.0.0.255 eq domain",
    #     ]
    #     result = self.execute_module(changed=False)
    #     self.assertEqual(sorted(result["rendered"]), sorted(commands))
