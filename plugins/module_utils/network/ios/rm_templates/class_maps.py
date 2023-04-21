# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Class_maps parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)

class Class_mapsTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Class_mapsTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "standard class map names",
            "getval": re.compile(
                r"""^class-map
                    \s(type\s(?P<class_map_type>access-control|appnav|site-manager|stack|traffic)\s)?
                    (?P<match_type>match-any|match-all)
                    \s(?P<class_map_name>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "name": "{{ class_map_name }}",
                    "type": "{{ class_map_type }}",
                    "match_type": "{{ match_type }}"
                }
            },
            "shared": True
        }, #todo: add separate entry for multicast group flows
        {
            "name": "description",
            "getval": re.compile(
                r"""^\s*description
                    \s(?P<description>.+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "class_map_decription": "{{ description }}"
                }
            },
        },
        {
            "name": "match access groups",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \saccess-group
                    \s((?P<number>\S+)|(name\s(?P<name>\S+)))
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "access_groups": {
                                "name": "{{ name }}",
                                "number": "{{ number }}",
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
        },
        {
            "name": "match any",
            "getval": re.compile(
                r"""^\s*match
                    \sany
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "any": True,
                        }
                    ]
                }
            }
        },
        {
            "name": "match application name regexp",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sapplication
                    \s(?P<regexp>\S+)
                    (\ssource\s(?P<source>cli|cube|msp|nbar|rfmd|rsvp|cac))?
                    (\svendor\s(?P<vendor>)\S+)?
                    (\sversion\s(?P<version>\S+))?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "application_name": {
                                "name_regexp": "{{ regexp }}",
                                "source": "{{ source }}",
                                "vendor": "{{ vendor }}",
                                "version": "{{ version }}",
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match application attribute",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sapplication
                    \sattribute
                    \s(?P<attribute>category|device-class|media-type|sub-category|tcl)
                    \s(?P<value>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "application_attribute": {
                                "{{ attribute.replace('-', '_') }}": "{{ value }}"
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match application group",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sapplication
                    \sapplication-group
                    \s(?P<application_group>telepresence-group|vmware-group|webex-group)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "application_group": "{{ application_group }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match class-map",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sclass-map
                    \s(?P<class_map>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "class_map": "{{ class_map }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match cac status",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \scac
                    \sstatus
                    \s(?P<cac_status>admitted|un-admitted)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "cac_status": "{{ cac_status }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match cos",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \scos
                    \s* (?P<cos_val_0>\d)
                    (\s*(?P<cos_val_1>\d))?
                    (\s*(?P<cos_val_2>\d))?
                    (\s*(?P<cos_val_3>\d))?
                    (\s*(?P<cos_val_4>\d))?
                    (\s*(?P<cos_val_5>\d))?
                    (\s*(?P<cos_val_6>\d))?
                    (\s*(?P<cos_val_7>\d))?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "cos": {
                                "{{ 'cos_' + cos_val_0 if cos_val_0 is defined else None }}": "{{ not not cos_val_0 }}",
                                "{{ 'cos_' + cos_val_1 if cos_val_1 is defined else None }}": "{{ not not cos_val_1 }}",
                                "{{ 'cos_' + cos_val_2 if cos_val_2 is defined else None }}": "{{ not not cos_val_2 }}",
                                "{{ 'cos_' + cos_val_3 if cos_val_3 is defined else None }}": "{{ not not cos_val_3 }}",
                                "{{ 'cos_' + cos_val_4 if cos_val_4 is defined else None }}": "{{ not not cos_val_4 }}",
                                "{{ 'cos_' + cos_val_5 if cos_val_5 is defined else None }}": "{{ not not cos_val_5 }}",
                                "{{ 'cos_' + cos_val_6 if cos_val_6 is defined else None }}": "{{ not not cos_val_6 }}",
                                "{{ 'cos_' + cos_val_7 if cos_val_7 is defined else None }}": "{{ not not cos_val_7 }}",
                            },  
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match cos inner",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \scos
                    \sinner
                    \s*(?P<cos_inner_val_0>\d)
                    (\s*(?P<cos_inner_val_1>\d))?
                    (\s*(?P<cos_inner_val_2>\d))?
                    (\s*(?P<cos_inner_val_3>\d))?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "cos_inner": {
                                "{{ 'cos_inner_' + cos_inner_val_0 if cos_inner_val_0 is defined else None }}": "{{ not not cos_inner_val_0 }}",
                                "{{ 'cos_inner_' + cos_inner_val_1 if cos_inner_val_1 is defined else None }}": "{{ not not cos_inner_val_1 }}",
                                "{{ 'cos_inner_' + cos_inner_val_2 if cos_inner_val_2 is defined else None }}": "{{ not not cos_inner_val_2 }}",
                                "{{ 'cos_inner_' + cos_inner_val_3 if cos_inner_val_3 is defined else None }}": "{{ not not cos_inner_val_3 }}",
                            },  
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match destination mac",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sdestination-address
                    \smac
                    \s(?P<dest_mac>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "destination_mac_address": "{{ dest_mac.lower() }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
        "name": "match discard class",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sdiscard-class
                    \s(?P<discard_class>\d)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "discard_class": "{{ discard_class }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
        "name": "match object-group security",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sgroup-object
                    \ssecurity
                    \s(?P<direction>destination|source)
                    \s(?P<name>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "object_group_security": {
                                "direction": "{{ direction }}",
                                "name": "{{ name }}"
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
        "name": "match input-interface",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sinput-interface
                    \s(?P<interface_name>\S+)(?P<interface_number>\d+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "input_interface": {
                                "interface_name": "{{ interface_name.lower() }}",
                                "interface_number": "{{ interface_number }}"
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
        "name": "match ip dscp",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sip
                    \sdscp
                    \s*(?P<dscp_value_1>(\d{1,2})|(af[1-4][1-3])|(cs[1-7])|default|ef)
                    \s*(?P<dscp_value_2>(\d{1,2})|(af[1-4][1-3])|(cs[1-7])|default|ef)?
                    \s*(?P<dscp_value_3>(\d{1,2})|(af[1-4][1-3])|(cs[1-7])|default|ef)?
                    \s*(?P<dscp_value_4>(\d{1,2})|(af[1-4][1-3])|(cs[1-7])|default|ef)?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "ip_dscp": {
                                "dscp_value_1": "{{ dscp_value_1 }}",
                                "dscp_value_2": "{{ dscp_value_2 }}",
                                "dscp_value_3": "{{ dscp_value_3 }}",
                                "dscp_value_4": "{{ dscp_value_4 }}"
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        # todo ip precedence
        {
            "name": "match ip rtp",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sip
                    \srtp
                    \s(?P<starting_port_number>\d{4,5})
                    \s(?P<port_range>\d{1,5})
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "ip_rtp": {
                                "starting_port_number": "{{ starting_port_number }}",
                                "port_range": "{{ port_range }}",
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match metadata",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \smetadata
                    \s(?P<metadata_type>(cac\sstatus)|(called-uri)|(calling-uri)|(device-model)|(global-session-id)|(multi-party-session-id))
                    \s(?P<metadata_value>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "metadata": {
                                "{{ metadata_type.replace('-', '_').replace(' ', '_') }}": "{{ metadata_value }}",
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match mpls experimental",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \smetadata
                    \s(?P<metadata_type>(cac\sstatus)|(called-uri)|(calling-uri)|(device-model)|(global-session-id)|(multi-party-session-id))
                    \s(?P<metadata_value>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "metadata": {
                                "{{ metadata_type.replace('-', '_').replace(' ', '_') }}": "{{ metadata_value }}",
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        # todo mpls_experimental_topmost
        {
            "name": "match packet length",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \spacket
                    \slength
                    ((\smin\s(?P<min>\d{1,4}))|(\smax\s(?P<max>\d{1,4}))){1,2}
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "packet_length": {
                                "min": "{{ min }}",
                                "max": "{{ max }}",
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match protocol attribute",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sprotocol
                    \sattribute
                    \s(?P<attribute_name>\S+)
                    \s(?P<attribute_value>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "protocol_attribute": {
                                "attribute_name": "{{ attribute_name }}",
                                "attribute_value":  "{{ attribute_value }}"
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match protocol",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sprotocol
                    \s(?P<protocol_name>\S+)
                    (\s(?P<subprotocol_parameter_name>\S+)
                    \s"(?P<subprotocol_parameter_value>.+)")?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "protocol": {
                                "protocol_name": "{{ protocol_name }}",
                                "subprotocol_parameter":  {
                                    "subprotocol_parameter_name": "{{ subprotocol_parameter_name }}",
                                    "subprotocol_parameter_value": "{{ subprotocol_parameter_value }}"
                                }
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match qos group",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sqos-group
                    \s(?P<qos_group_num>\d{1,2})
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "qos_group": "{{ qos_group_num }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match security group",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \ssecurity-group
                    \s(?P<direction>(destination\stag)|(source\stag))
                    \s(?P<num>\d{1,5})
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "security_group": {
                                "{{ direction.replace(' ', '_') }}": "{{ num }}"
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
                {
            "name": "match source mac",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \ssource-address
                    \smac
                    \s(?P<source_mac>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "source_mac_address": "{{ source_mac.lower() }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match destination mac",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sdestination-address
                    \smac
                    \s(?P<dest_mac>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "destination_mac_address": "{{ dest_mac.lower() }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match vlan",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \svlan
                    \s*(?P<id>\d{1,4})
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "vlan_id": "{{ id }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match traffic category",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \straffic-category
                    \s(?P<traffic_category>allow|optimize)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "traffic_category": "{{ traffic_category }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
        {
            "name": "match vlan inner",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \svlan
                    \sinner
                    \s*(?P<id>\d{1,4})
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "vlan_id_inner": "{{ id }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            }
        },
    ]
    # fmt: on
