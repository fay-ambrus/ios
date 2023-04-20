# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from syslog import syslog


__metaclass__ = type

"""
The ios class_maps fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.class_maps import (
    Class_mapsTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.class_maps.class_maps import (
    Class_mapsArgs,
)

class Class_mapsFacts(object):
    """ The ios class_maps facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = Class_mapsArgs.argument_spec

    def get_class_map_data(self, connection):
        # Get information about each type of class-map
        # alternate command might be 'show running-config partition class-map'
        # todo: consider if this is the correct way to use it
        return connection.get("show running-config partition class-map")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Class_maps network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_class_map_data(connection)

        # parse native config using the Class_maps template
        class_maps_parser = Class_mapsTemplate(lines=data.splitlines(), module=self._module)
        objs = list(class_maps_parser.parse().values())

        ansible_facts['ansible_network_resources'].pop('class_maps', None)

        params = utils.remove_empties(
            class_maps_parser.validate_config(self.argument_spec, {"config": objs}, redact=True)
        )

        if 'config' in params:
            facts['class_maps'] = params['config']

        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
