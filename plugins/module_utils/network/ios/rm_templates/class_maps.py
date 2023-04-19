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
            "name": "match application name",
            "getval": re.compile(
                r"""^\s*match(\s(?P<negate>not))?
                    \sapplication
                    \s(?P<name>cisco-phone|citrix|h323|ip-camera|jabber|rtp|rtsp|sip|surveillance-distribution|telepresence-control|telepresence-data|telepresence-media|vmware-view|webex-meeting|wyze-zero-client|xmpp-client)\s*$
                """,
                re.VERBOSE),
            "result": {
               "{{ class_map_name|d() }}": {
                    "matches": [
                        {
                            "application_name": {
                                "{{ name }}": {}
                            },
                            "negate": "{{ not not negate }}"
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
        }
    ]
    # fmt: on
