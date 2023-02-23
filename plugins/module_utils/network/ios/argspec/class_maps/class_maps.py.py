# -*- coding: utf-8 -*-
# todo: copyright information

# todo: check out cli_rm_builder

__metaclass__ = type

"""
The arg spec for the ios_classmap module
"""

class ClassMapArgs(object):
    """The arg spec for the ios_classmap module"""
    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {
                    "required": True,
                    "type": "str"
                },
                "match_type": {
                    "choices": ["all", "any"],
                    "default": "all",
                    "type": "str",
                },
                "matches": {
                    "elements": "dict",
                    "options": {
                        "access_group": {"type": "str"}
                    },
                    "type": "list"
                }
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }