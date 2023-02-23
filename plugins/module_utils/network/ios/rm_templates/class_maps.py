# -*- coding: utf-8 -*-
# todo: copyright information

"""
The classmap parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""
import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


# todo: this id bad and has to be rewritten later
def _tmplt_classmap_entries(matches):
    command = ""
    if matches:
        access_group = matches.get("access_group")
        if access_group:
            command += "match "
            command += "access-group"
            command += " "
            command += access_group

    return command


class ClassMapTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(ClassMapTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "classmap_name",
            "getval": re.compile(
                r"""^\s*Class*
                \s*Map*
                \s*match-*
                \s*(?P<match_type>all|any)*
                \s*(?P<classmap_name>\S+)*
                \s*.*
                $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "name",
            "result": {
                "{{ classmap_name|d() }}": {
                    "name": "{{ classmap_name }}",
                    "match_type": "{{ match_type }}",
                }
            },
            "shared": True,
        },
        {
            "name": "matches",
            "getval": re.compile(
                r"""^\s*Match*
                    \s*access-group*
                    \s*(?P<index_number>\d+)*
                    \s*
                $""",
                re.VERBOSE
            ),
            "setval": _tmplt_classmap_entries,
            "compval": "matches",
            "result": {
                "{{ classmap_name|d() }}": {
                    "name": "{{ classmap_name }}",
                    "matches": [
                        {
                            "access_group": "{{ index_number }}"
                        }
                    ]
                }
            }
        }
    ]
