#!/usr/bin/python
# -*- coding: utf-8 -*-
# todo: copyright information

"""
The module file for ios_acls
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

# todo: update docmentation and look into autogenerating the templates
DOCUMENTATION = """
author:
  - Ambrus Fáy (@fay-ambrus)
decription: This module configures and manages Class-Maps on IOS platforms.
module: ios_classmap
notes:
  - todo: make notes
options:
  config:
    description: A dictionary of Class-Map options.
    elements: dict
    suboptions:
      classmaps:
        description:
          - It is pretty much th same thing as one level up... -> A list of Class-Maps.
        elements: dict
        suboptions:
          matces:
            description: A list of the match criteria.
            elements: dict
            subopptions:
              access_group:
                description: Match the specified Access-Group.
                type: int
            type: list
          match_type:
            choices:
              - any
              - all
            description:
              - Decides, if the packet has to match all or any of the criteria defined to
                be classified to this Class-Map.
            default: all
            type: str
          name:
            description:
              - The name of the Class-Map.
            required: true
            type: str
        tpye: list
    type: list  
  running_config:
    description:
      - This is not yet implemented!
    type: str
  state:
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - gathered
      - rendered
      - parsed
    default: merged
    description:
      - todo: description here
    type: str
short_description: Resource module to configure ACLs.
"""

EXAMPLES = """todo"""

RETURN = """todo"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.classmap.classmap import (
    ClassMapArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.classmap.classmap import ClassMap


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=ClassMapArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True
    )

    result = ClassMap(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
