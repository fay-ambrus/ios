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
            "name": "class maps",
            "getval": re.compile(
                r"""^class-map
                    \s(?P<match_type>match-any|match-all)
                    \s(?P<class_map_name>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                        "class_map_type": "{{ class_map_type }}",
                        "name": "{{ class_map_name }}",
                        "match_type": "{{ match_type }}"
                    }
            },
            "setval": "class-map {{ match_type if match_type is defined else '' }} {{ name }}",
            "compval": "name",
            "shared": True
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""^\s*description
                    \s(?P<description>.+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "description": "{{ description }}"
                }
            },
            "compval": "description",
            "setval": "description {{ description }}"
        },
        {
            "name": "match access group",
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
                            "access_group": {
                                "name": "{{ name }}",
                                "number": "{{ number }}",
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
            "compval": "access_group",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} access-group "
            "{{ access_group.number if access_group.number is defined else 'name ' + access_group.name }}",
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
            },
            "compval": "any",
            "setval": "{{ 'match any' if any else '' }}"
        },
        {
            "name": "match application",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sapplication
                    \s(?P<name>\S+)
                    (\ssource\s(?P<source>cli|cube|msp|nbar|rfmd|rsvp|cac))?
                    (\svendor\s(?P<vendor>)\S+)?
                    (\sversion\s(?P<version>\S+))?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "application": {
                                "name": "{{ name }}",
                                "source": "{{ source }}",
                                "vendor": "{{ vendor }}",
                                "version": "{{ version }}",
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                },
            },
            "compval": "application",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} application "
            "{{ application.name }} "
            "{{ 'source ' + application.source if application.source is defined }}"
            "{{ 'vendor ' + application.vendor if application.vendor is defined }}"
            "{{ 'version ' + application.version if application.version is defined }}"
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
            },
            "compval":  "application_attribute",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} application attribute "
            "{{ 'category ' + application_attribute.category if application_attribute.category is defined }}"            
            "{{ 'device-class ' + application_attribute.device_class if application_attribute.device_class is defined }}"
            "{{ 'media-type ' + application_attribute.media_type if application_attribute.media_type is defined }}"
            "{{ 'sub-category ' + application_attribute.sub_category if application_attribute.sub_category is defined }}"
            "{{ 'tcl ' + application_attribute.tcl if application_attribute.tcl is defined }}"            
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
            },
            "compval": "application_group",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} application application-group {{ application_group }}"
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
            },
            "compval": "class_map",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} class-map {{ class_map }}"
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
            },
            "compval": "cac_status",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} cac status {{ cac_status }}"
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
                            "cos": [
                                "{{ cos_val_0 if cos_val_0 is defined else None }}",
                                "{{ cos_val_1 if cos_val_1 is defined else None }}",
                                "{{ cos_val_2 if cos_val_2 is defined else None }}",
                                "{{ cos_val_3 if cos_val_3 is defined else None }}",
                                "{{ cos_val_4 if cos_val_4 is defined else None }}",
                                "{{ cos_val_5 if cos_val_5 is defined else None }}",
                                "{{ cos_val_6 if cos_val_6 is defined else None }}",
                                "{{ cos_val_7 if cos_val_7 is defined else None }}"
                            ],  
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
            "compval": "cos",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} cos"
            "{% for cos_value in cos %} {{ cos_value }}{% endfor %}"
        },
        {
            "name": "match cos inner",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \scos
                    \sinner
                    \s* (?P<cos_inner_val_0>\d)
                    (\s*(?P<cos_inner_val_1>\d))?
                    (\s*(?P<cos_inner_val_2>\d))?
                    (\s*(?P<cos_inner_val_3>\d))?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "cos_inner": [
                                "{{ cos_inner_val_0 if cos_inner_val_0 is defined else None }}",
                                "{{ cos_inner_val_1 if cos_inner_val_1 is defined else None }}",
                                "{{ cos_inner_val_2 if cos_inner_val_2 is defined else None }}",
                                "{{ cos_inner_val_3 if cos_inner_val_3 is defined else None }}",
                            ],  
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
            "compval": "cos_inner",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} cos inner"
            "{% for cos_inner_value in cos_inner %} {{ cos_inner_value }}{% endfor %}"
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
                            "destination_mac_address": "{{ dest_mac.upper() }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
            "compval": "destination_mac_address",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} destination-address mac "
            "{{ destination_mac_address }}"
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
            },
            "compval": "discard_class",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} discard-class "
            "{{ discard_class }}"
        },
        {
        "name": "match object-group security",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sgroup-object
                    \ssecurity
                    \s(?P<endpoint>destination|source)
                    \s(?P<name>\S+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "object_group_security": {
                                "endpoint": "{{ endpoint }}",
                                "name": "{{ name }}"
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
            "compval": "object_group_security",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} group-object security "
            "{{ object_group_security.endpoint }} {{ object_group_security.name }}"
        },
        {
        "name": "match input-interface",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sinput-interface
                    \s(?P<interface_type>\S+)(?P<interface_number>\d+)
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "input_interface": {
                                "interface_type": "{{ interface_type.lower() }}",
                                "interface_number": "{{ interface_number }}"
                            },
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
            "compval": "input_interface",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} input-interface "
            "{{ input_interface.interface_type }} {{ input_interface.interface_number }}"
        },
        {
            "name": "match dscp",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sdscp
                    \s* (?P<dscp_val_0>\S+)
                    (\s*(?P<dscp_val_1>\S+))?
                    (\s*(?P<dscp_val_2>\S+))?
                    (\s*(?P<dscp_val_3>\S+))?
                    (\s*(?P<dscp_val_4>\S+))?
                    (\s*(?P<dscp_val_5>\S+))?
                    (\s*(?P<dscp_val_6>\S+))?
                    (\s*(?P<dscp_val_7>\S+))?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "dscp":{
                                "dscp_values": [
                                    "{{ dscp_val_0 if dscp_val_0 is defined else None }}",
                                    "{{ dscp_val_1 if dscp_val_1 is defined else None }}",
                                    "{{ dscp_val_2 if dscp_val_2 is defined else None }}",
                                    "{{ dscp_val_3 if dscp_val_3 is defined else None }}",
                                    "{{ dscp_val_4 if dscp_val_4 is defined else None }}",
                                    "{{ dscp_val_5 if dscp_val_5 is defined else None }}",
                                    "{{ dscp_val_6 if dscp_val_6 is defined else None }}",
                                    "{{ dscp_val_7 if dscp_val_7 is defined else None }}"
                                ]
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
                    \sip\sdscp
                    \s* (?P<dscp_val_0>\S+)
                    (\s*(?P<dscp_val_1>\S+))?
                    (\s*(?P<dscp_val_2>\S+))?
                    (\s*(?P<dscp_val_3>\S+))?
                    (\s*(?P<dscp_val_4>\S+))?
                    (\s*(?P<dscp_val_5>\S+))?
                    (\s*(?P<dscp_val_6>\S+))?
                    (\s*(?P<dscp_val_7>\S+))?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "dscp":{
                                "dscp_values": [
                                    "{{ dscp_val_0 if dscp_val_0 is defined else None }}",
                                    "{{ dscp_val_1 if dscp_val_1 is defined else None }}",
                                    "{{ dscp_val_2 if dscp_val_2 is defined else None }}",
                                    "{{ dscp_val_3 if dscp_val_3 is defined else None }}",
                                    "{{ dscp_val_4 if dscp_val_4 is defined else None }}",
                                    "{{ dscp_val_5 if dscp_val_5 is defined else None }}",
                                    "{{ dscp_val_6 if dscp_val_6 is defined else None }}",
                                    "{{ dscp_val_7 if dscp_val_7 is defined else None }}"
                                ],
                                "ip_versions": "IPv4"
                            },  
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
            "compval": "dscp",
            "setval": "match {{ 'not' if negate is defined and negate else '' }}"
            "{{ ' ip' if dscp.ip_versions == 'IPv4' }} dscp"
            "{% for dscp_value in dscp.dscp_values %} {{ dscp_value }}{% endfor %}"       
        },
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
            },
            "compval": "ip_rtp",
            "setval": "match {{ 'not' if negate is defined and negate else '' }}"
            "ip rtp {{ ip_rtp.starting_port_number }} {{ ip_rtp.port_range }}"     
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
            },
            "compval": "metadata",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} metadata "
            "{{ 'cac status ' + metadata.cac_status if metadata.cac_status is defined }}"
            "{{ 'called-uri ' + metadata.called_uri if metadata.called_uri is defined }}"
            "{{ 'calling-uri ' + metadata.calling_uri if metadata.calling_uri is defined }}"
            "{{ 'device-model ' + metadata.device_model if metadata.device_model is defined }}"
            "{{ 'global-session-id ' + metadata.global_session_id if metadata.global_session_id is defined }}"
            "{{ 'multi-party-session-id ' + metadata.multi_party_session_id if metadata.multi_party_session_id is defined }}"
        },
        {
            "name": "match mpls experimental",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \smpls\sexperimental\stopmost
                    \s* (?P<mpls_val_0>\d)
                    (\s*(?P<mpls_val_1>\d))?
                    (\s*(?P<mpls_val_2>\d))?
                    (\s*(?P<mpls_val_3>\d))?
                    (\s*(?P<mpls_val_4>\d))?
                    (\s*(?P<mpls_val_5>\d))?
                    (\s*(?P<mpls_val_6>\d))?
                    (\s*(?P<mpls_val_7>\d))?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "mpls_experimental_topmost": [
                                "{{ mpls_val_0 if mpls_val_0 is defined else None }}",
                                "{{ mpls_val_1 if mpls_val_1 is defined else None }}",
                                "{{ mpls_val_2 if mpls_val_2 is defined else None }}",
                                "{{ mpls_val_3 if mpls_val_3 is defined else None }}",
                                "{{ mpls_val_4 if mpls_val_4 is defined else None }}",
                                "{{ mpls_val_5 if mpls_val_5 is defined else None }}",
                                "{{ mpls_val_6 if mpls_val_6 is defined else None }}",
                                "{{ mpls_val_7 if mpls_val_7 is defined else None }}"
                            ],
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
            "compval": "mpls_experimental_topmost",
            "setval": "match{{ ' not' if negate is defined and negate else '' }} mpls experimental topmost"
            "{% for mpls_val in mpls_experimental_topmost %} {{ mpls_val }}{% endfor %}"  
        },
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
            },
            "compval": "packet_length",
            "setval": "match{{ ' not' if negate is defined and negate else '' }} packet length"
            "{{ ' min ' + packet_length.min|string if packet_length.min is defined }}"  
            "{{ ' max ' + packet_length.max|string if packet_length.max is defined }}"
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
            },
            "compval": "protocol_attribute",
            "setval": "match{{ ' not' if negate is defined and negate else '' }} protocol attribute "
            "{{ protocol_attribute.attribute_name }} {{ protocol_attribute.attribute_value }}"
        },
        {
            "name": "match protocol",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \s(protocol)
                    \s(?P<protocol_name>\S+)
                    (\s(?P<subprotocol_parameter_name>\S+)?
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
            },
            "compval": "protocol",
            "setval": "match{{ ' not' if negate is defined and negate else '' }} protocol "
            "{{ protocol.protocol_name }}"
            " {{ protocol.subprotocol_parameter.subprotocol_parameter_name if protocol.subprotocol_parameter.subprotocol_parameter_name is defined}}"
            " {{ protocol.subprotocol_parameter.subprotocol_parameter_value if protocol.subprotocol_parameter.subprotocol_parameter_value is defined}}"
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
            },
            "compval": "qos_group",
            "setval": "match{{ ' not' if negate is defined and negate else '' }} qos-group "
            "{{ qos_group }}"
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
            },
            "compval": "security_group",
            "setval": "match{{ ' not' if negate is defined and negate else '' }} security-group"
            "{{ ' destination tag ' + security_group.destination_tag|string if security_group.destination_tag is defined }}"
            "{{ ' source tag ' + security_group.source_tag|string if security_group.source_tag is defined }}"
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
                            "source_mac_address": "{{ source_mac.upper() }}",
                            "negate": "{{ not not negate }}"
                        }
                    ]
                }
            },
            "compval": "source_mac_address",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} source-address mac "
            "{{ source_mac_address }}"
        },
        {
            "name": "match start eq or neq",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sstart
                    \s(?P<layer>l2|l3)-start
                    \soffset
                    \s(?P<offset>\d{1,3})
                    \ssize
                    \s(?P<size>\d{1,2})
                    \s(?P<eq_type>eq|neq)
                    \s(?P<value>\S+)
                    (\smask
                    \s(?P<mask>\S+))?
                \s*$""",
                re.VERBOSE),
            "result": {
                "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "start": {
                                "layer": "{{ layer }}",
                                "offset": "{{ offset }}",
                                "size": "{{ size }}",
                                "{{ eq_type }}": {
                                    "value": "{{ value }}",
                                    "mask": "{{ mask }}"
                                }
                            }
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
            },
            "compval": "vlan_id",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} "
            "vlan {{ vlan_id }}",
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
            },
            "compval": "vlan_id_inner",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} "
            "vlan inner {{ vlan_id_inner }}",
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
            },
            "compval": "traffic_category",
            "setval": "match {{ 'not' if negate is defined and negate else '' }} "
            "traffic-category {{ traffic_category }}",
        },
    ]
    # fmt: on
