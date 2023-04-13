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
            "name": "standard_class_map_names",
            "getval": re.compile(
                r"""^class-map
                    \s(type\s(?P<class_map_type>access-control|appnav|site-manager|stack|traffic))?
                    \s(?P<match_type>match-any|match-all)
                    \s*(?P<class_map_name>\S+)
                $""", re.VERBOSE),
            "result": {
                "class_maps": {
                    "{{ class_map_name|d() }}": {
                        "name": "{{ class_map_name }}",
                        "type": "{{ class_map_type }}",
                        "match_type": "{{ match_type }}"
                    }
                }
            },
            "shared": True
        }, #todo: add separate entry for multicast group flows
    ]
    # fmt: on
