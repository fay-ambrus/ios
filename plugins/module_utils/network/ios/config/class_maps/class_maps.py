#
# -*- coding: utf-8 -*-
# todo: copyright information

"""
The ios_classmap class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.classmap import (
    ClassMapTemplate,
)

# todo: delete this
MY_LOG_FILE_NAME = '/home/kerak/my_logs.txt'

def my_log(outp):
    with open(MY_LOG_FILE_NAME, 'a') as log_file:
        log_file.write(str(outp))
        log_file.write('\n')

def my_log_erase():
    with open(MY_LOG_FILE_NAME, 'w') as log_file:
        log_file.write('')

class ClassMap(ResourceModule):

    def __init__(self, module):
        super(ClassMap, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="classmap",
            tmplt=ClassMapTemplate(),
        )

    def execute_module(self):
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        haved, wantd = dict(), dict()

        if self.have:
            haved = self.list_to_dict(self.have)
        if self.want:
            wantd = self.list_to_dict(self.want)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        if self.state == "deleted":
            if wantd:
                wantd = {k: v for k, v in iteritems(haved) if k not in wantd}

        self._compare(wantd, haved)


    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the class-map network resource.
        """

        for wname, wentry in iteritems(want):
            hentry = have.pop(wname, {})
            match_type = wentry["match_type"] if wentry.get("match_type") else hentry.get("match_type")
            begin = len(self.commands)  # to determine the index for classmap command

            # todo: this won't be correct if the model is expanded, and can be written more compactly
            # handle matches
            wmatches = wentry.pop("matches", {})
            swmatches = set()
            for k, v in iteritems(wmatches):
                swmatches.add(v["access_group"])

            hmatches = hentry.pop("matches", {})
            shmatches = set()
            for k, v in iteritems(hmatches):
                shmatches.add(v["access_group"])

            sadd = swmatches - shmatches
            sremove = shmatches - swmatches

            for num in sadd:
                self.addcmd({"access_group": num}, "matches", False)

            for num in sremove:
                self.addcmd({"access_group": num}, "matches", True)

            if len(self.commands) != begin and wname != "class-default":
                self.commands.insert(begin, "class-map match-{0} {1}".format(match_type, wname))
                self.commands.append("exit")

        # deleting unwanted class-maps
        for name in have.keys():
            if name != "class-default":
                self.commands.append("no class-map {0}".format(name))

        my_log(self.commands)

    def list_to_dict(self, param):
        """converts list attributes to dict"""

        temp, cnt = dict(), 0
        if param:
            for each in param:
                temp_matches = {}
                cnt = 0
                if each.get("matches"):
                    for access_group in each.get("matches"):
                        if access_group:
                            cnt += 1
                            temp_matches.update({"_"+str(cnt): access_group})

                if each.get("match_type"):
                    temp.update(
                         {
                            each.get("name"): {
                                "match_type": each.get("match_type"),
                                "matches": temp_matches
                            }
                        }
                    )

                else:
                    temp.update(
                        {
                            each.get("name"): {
                                "match_type": "match_all",
                                "matches": temp_matches
                            }
                        }
                    )

            return temp