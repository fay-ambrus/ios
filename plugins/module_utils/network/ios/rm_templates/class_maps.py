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
                    \s
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
    ]
    # fmt: on
