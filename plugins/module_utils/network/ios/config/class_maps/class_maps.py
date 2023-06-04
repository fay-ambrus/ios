#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios_class_maps config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.class_maps import (
    Class_mapsTemplate,
)
from syslog import syslog


class Class_maps(ResourceModule):
    """
    The ios_class_maps config class
    """

    def __init__(self, module):
        super(Class_maps, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="class_maps",
            tmplt=Class_mapsTemplate(),
        )
        self.parsers = [
            "class maps",
            "description",
            "match access group",
            "match any",
            "match application",
            "match application attribute",
            "match application group",
            "match class-map",
            "match cac status",
            "match cos",
            "match cos inner",
            "match destination mac",
            "match discard class",
            "match object-group security",
            "match input-interface",
            "match ip dscp",
            "match ip rtp",
            "match metadata",
            "match mpls experimental",
            "match packet length",
            "match protocol attribute",
            "match protocol",
            "match qos group",
            "match security group",
            "match source mac",
            "match vlan",
            "match vlan inner",
            "match traffic category"
        ]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        wantd = {entry['name']: entry for entry in self.want}
        haved = {entry['name']: entry for entry in self.have}

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Class_maps network resource.
        """

        begin = len(self.commands)

        # first of all, compare the class-map headers
        self.compare(parsers=self.parsers, want=want, have=have)

        want_matches = []
        have_matches = []

        if want and want.get("matches"):
            want_matches = want.get("matches")

        if have and have.get("matches"):
            have_matches = have.get("matches")

        for wm in want_matches:
            # specific validation has to be done here
            if wm.get("cos"):
                wm["cos"] = list(set(wm.get("cos")))
                wm["cos"].sort()

            if wm.get("cos_inner"):
                wm["cos_inner"] = list(set(wm.get("cos_inner")))
                wm["cos_inner"].sort()

            if wm.get("destination_mac_address"):
                wm["destination_mac_address"] = wm.get("destination_mac_address").upper().replace(':', '.')

            if wm.get("dscp"):
                dscp_values = wm.get("dscp").get("dscp_values")
                for i in range(len(dscp_values)):
                    if Class_mapsTemplate.DSCP_VALUES.get(dscp_values[i], None) is not None:
                        dscp_values[i] = Class_mapsTemplate.DSCP_VALUES.get(dscp_values[i])
                wm["dscp"]["dscp_values"] = list(set(filter(lambda v: v is not None, dscp_values)))
                wm["dscp"]["dscp_values"].sort()

            if wm.get("mpls_experimental_topmost"):
                wm["mpls_experimental_topmost"] = list(set(wm.get("mpls_experimental_topmost")))
                wm["mpls_experimental_topmost"].sort()

            if wm.get("source_mac_address"):
                wm["source_mac_address"] = wm.get("source_mac_address").upper().replace(':', '.')

            hm = {}
            if have_matches.count(wm) > 0:
                hm = have_matches[have_matches.index(wm)]
            self.compare(parsers=self.parsers, want=wm, have=hm)

        # remove "no description" command, if the class-map has been deleted in advance
        if begin + 1 < len(self.commands):
            if self.commands[begin].startswith("no class-map") and self.commands[begin + 1].startswith("no description"):
                del self.commands[begin + 1]

        # generate the command to enter the approriate class-map's configuration
        if begin < len(self.commands):
            if not self.commands[begin].startswith("class-map") and not self.commands[begin].startswith("no class-map"):
                class_map_cmd = "class-map {0} {1}".format(want["match_type"], want["name"])
                self.commands.insert(begin, class_map_cmd)
