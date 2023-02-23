# pylint: skip-file
# -*- coding: utf-8 -*-
# todo: copyright information
"""
The ios_classmap fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.classmap.classmap import (
    ClassMapArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.classmap import (
    ClassMapTemplate,
)

class ClassMapFacts(object):
    """The ios_classmap fact class"""


    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = ClassMapArgs.argument_spec

    def get_classmap_data(self, connection):
        # Get the class-maps from the ios router
        return connection.get("show class-map")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for classmaps
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        if not data:
            data = self.get_classmap_data(connection)

        rmmod = NetworkTemplate(lines=data.splitlines(), tmplt=ClassMapTemplate())
        current = rmmod.parse()

        temp = []

        for k, v in iteritems(current):
            temp.append(v)

        temp = sorted(temp, key=lambda i: str(i["name"]))


        facts = list()
        if temp:
            params = utils.validate_config(
                self.argument_spec,
                {"config": temp},
            )
            for cfg in params["config"]:
                facts.append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update({"classmap": facts})

        return ansible_facts
