#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_class_maps
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_class_maps
short_description: Class-Maps resource module
description:
    - This module configures and manages Class-Maps on IOS platforms.
version_added: 0.01
author: Ambrus Fay (@fay-ambrus)
notes:
    - Tested against Cisco IOSXE version 17.3 on CML.
    - This module works with connection C(network_cli).
      See L(IOS Platform Options,../network/user_guide/platform_ios.html).
options:
  config:
    description: A list of class-maps represented as dictionaries.
    type: list
    elements: dict
    mutually_exclusive: [[]] # todo
    suboptions:
        name:
            description:
                - Name of the class for the class map.
                - The name must be surrounded with quotation marks, if it contains spaces.
            required: true
            type: str
        match_type:
            description:
                - Determines how packets are evaluated when multiple match criteria exist.
                - If match-all is provided, a packet must match all statements to be accepted.
                - If match-any is provided, a packet must match any of the match statements to be accepted.
            default: match-all
            type: str
            choices:
                - match-all
                - match-any
                - match-none
        class_map_decription:
            description: Comment or a description that is added to the class map.
            type: str
        class_map_type:
            description: The type of the class-map
            type: str
            default: standard
            choices:
                - access-control
                - appnav
                - control
                - inspect
                - multicast-flows
                - site-manager
                - stack
                - standard
                - traffic
        matches:
            description: A list of classification criteria.
            type: list
            elements: dict
            suboptions:
                access_groups:
                    description:
                        - Access-groups to match.
                        - Identified by a name or number.
                    type: dict
                    mutually_exclusive: [[name, number]]
                    suboptions:
                        name:
                            description:
                                - Specifies a named ACL.
                                - The name can be up to 40 alphanumeric characters.
                            type: str
                        number:
                            description:
                                - Specifies a numbered ACL.
                                - The range is from 1 to 2699.
                            type: int
                any:
                    description: Configures the match criteria to be successful for all packets.
                    type: bool
                application_attribute:
                    description: Specifies the relevant application metadata attribute to match.
                    type: dict
                    suboptions:
                        category:
                            description:
                                - Specifies the category type that the control plane classification engine must match.
                            type: str
                            choices:
                                - business-and-productivity-tools
                                - physical-security
                                - voice-and-video
                        device_class:
                            description:
                                - Specifies the device class to match.
                            type: str
                            choices:
                                - desktop-conferencing
                                - desktop-virtualization
                                - physical-phone
                                - room-conferencing
                                - software-phone
                                - surveillance
                        media_type:
                            description:
                                - Specifies the type of media to match.
                            type: str
                            choices:
                                - audio
                                - audio-video
                                - control
                                - data
                                - video
                        sub_category:
                            description:
                                - Specifies the subcategory to match.
                            type: str
                            choices:
                                - control-and-signaling
                                - remote-access-terminal
                                - video-surveillance
                                - voice-video-chat-collaboration
                        tcl:
                            description:
                                - Traffic Class Label to match.
                            type: str
                application_name:
                    description: Use name, source, vendor and version from application metadata as match criterion for classification.
                    type: dict
                    mutually_exclusive: [[source, vendor, version], [name_regexp, name]]
                    suboptions:
                        name_regexp:
                            description: Match all packets with applicaiton name matching the given regular expression.
                            type: str
                        predefined_type:
                            description: todo
                            type: dict
                            suboptions:
                                name:
                                    description: todo
                                    type: str
                                    choices:
                                        - cisco-phone
                                        - citrix
                                        - h323
                                        - ip-camera
                                        - jabber
                                        - rtp
                                        - rtsp
                                        - sip
                                        - surveillance-distribution
                                        - telepresence-control
                                        - telepresence-data
                                        - telepresence-media
                                        - vmware-view
                                        - webex-meeting
                                        - wyze-zero-client
                                        - xmpp-client
                                traffic_type:
                                    description: Traffic Type
                                    type: str
                                    choices:
                                        - control
                                        - background
                                        - bulk
                                        - desktop
                                        - interactive
                                        - realtime
                                        - session
                                        - streaming
                                        - tunnel
                                transport_type:
                                    description: Transport Type
                                    type: str
                                    choices:
                                        - rtcp
                                        - rtp
                                multiplex_type:
                                    description: Multiplex Type
                                    type: str
                                    choices:
                                        - set
                                        - unset
                                signaling_type:
                                    description: Signaling Type
                                    type: str
                                    choices:
                                        - bfcp
                                        - h323
                                        - mgcp
                                        - sip
                                        - skinny
                        citrix:
                            description: Citrix Application
                            type: dict
                            suboptions:
                                transport_type:
                                    description: Transport Type
                                    type: str
                                    choices:
                                        - ica
                                        - rdp
                        h323:
                            description:
                            type: bool
                        ip-camera:
                            description:
                            type: dict
                            suboptions:
                                traffic_type:
                                    description: Traffic Type
                                    type: str
                                    choices:
                                        - realtime
                                transport_type:
                                    description: Transport Type
                                    type: str
                                    choices:
                                        - rtp
                                multiplex_type:
                                    description: Multiplex Type
                                    type: str
                                    choices:
                                        - set
                                        - unset
                                signaling_type:
                                    description: Signaling Type
                                    type: str
                                    choices:
                                        - rtsp
                        jabber:
                            description:
                            type: bool
                        rtp:
                            description:
                            type: bool
                        rtsp:
                            description:
                            type: bool
                        sip:
                            description:
                            type: bool
                        surveillance-distribution:
                            description:
                            type: dict
                            suboptions:
                                traffic_type:
                                    description: Traffic Type
                                    type: str
                                    choices:
                                        - realtime
                                        - streaming
                                transport_type:
                                    description: Transport Type
                                    type: str
                                    choices:
                                        - rtp
                                multiplex_type:
                                    description: Multiplex Type
                                    type: str
                                    choices:
                                        - set
                                        - unset
                                signaling_type:
                                    description: Signaling Type
                                    type: str
                                    choices:
                                        - rtsp
                        telepresence-control:
                            description:
                            type: dict
                            suboptions:
                                signaling_type:
                                    description: Signaling Type
                                    type: str
                                    choices:
                                        - bfcp
                                        - ccp
                                        - clue
                                        - h323
                                        - mscp
                                        - sip
                                        - xccp
                        telepresence-data:
                            description:
                            type: bool
                        telepresence-media:
                            description:
                            type: dict
                            suboptions:
                                traffic_type:
                                    description: Traffic Type
                                    type: str
                                    choices:
                                        - control
                                transport_type:
                                    description: Transport Type
                                    type: str
                                    choices:
                                        - rtcp
                                        - rtp
                                multiplex_type:
                                    description: Multiplex Type
                                    type: str
                                    choices:
                                        - set
                                        - unset
                        vmware-view:
                            description:
                            type: dict
                            suboptions:
                                traffic_type:
                                    description: Traffic Type
                                    type: str
                                    choices:
                                        - desktop
                                        - desktop-feedback
                                        - session
                                        - streaming
                                        - tunnel
                                        - usb-redirection
                                transport_type:
                                    description: Transport Type
                                    type: str
                                    choices:
                                        - pcoip
                                        - rdp
                        webex-meeting:
                            description:
                            type: dict
                            suboptions:
                                traffic_type:
                                    description: Traffic Type
                                    type: str
                                    choices:
                                        - control
                                        - sharing
                                        - streaming
                                transport_type:
                                    description: Transport Type
                                    type: str
                                    choices:
                                        - http
                        wyze-zero-client:
                            description:
                            type: dict
                            suboptions:
                                traffic_type:
                                    description: Traffic Type
                                    type: str
                                    choices:
                                        - streaming
                        xmpp-client:
                                    description:
                                    type: bool
                        source:
                            description: Specifies the source of the application.
                            type: str
                            choices:
                                - cli
                                - cube
                                - msp
                                - nbar
                                - rfmd
                                - rsvp
                                - cac
                        vendor:
                            description:
                                - Specifies the name of the vendor.
                                - Refer to the manual to get a list of supported vendors for the respective application name.
                            type: str
                        version:
                            description: Specifies the version number.
                            type: str
                application_group:
                    description:
                        - Application Group to match
                    type: str
                    choices:
                        - telepresence-group
                        - vmware-group
                        - webex-group
                cac_status:
                    description: Call Admission Control status
                    type: str
                    choices:
                        - admitted
                        - un-admitted
                class_map:
                    description:
                        - Use a traffic class as a match criterion.
                        - Creating circular class-maps is not allowed!
                    type: str
                cos:
                    description:
                        - Match a packet on the basis of a Layer 2 class of service (CoS)/Inter-Switch Link (ISL) marking
                        - Up to 8 class-of-service values may be entered
                    type: dict
                    suboptions:
                        cos_0:
                            description: Determines if COS value 0 should be matched in this match.
                            type: bool
                        cos_1:
                            description: Determines if COS value 1 should be matched in this match.
                            type: bool
                        cos_2:
                            description: Determines if COS value 2 should be matched in this match.
                            type: bool
                        cos_3:
                            description: Determines if COS value 3 should be matched in this match.
                            type: bool
                        cos_4:
                            description: Determines if COS value 4 should be matched in this match.
                            type: bool
                        cos_5:
                            description: Determines if COS value 5 should be matched in this match.
                            type: bool
                        cos_6:
                            description: Determines if COS value 6 should be matched in this match.
                            type: bool
                        cos_7:
                            description: Determines if COS value 7 should be matched in this match.
                            type: bool
                cos_inner:
                    description:
                        - Match the inner cos of QinQ packets on a Layer 2 class of service (CoS) marking
                        - Up to 4 class-of-service values may be entered.
                    type: dict
                    suboptions:
                        cos_inner_0:
                            description: Determines if COS inner value 0 should be matched in this match.
                            type: bool
                        cos_inner_1:
                            description: Determines if COS inner value 1 should be matched in this match.
                            type: bool
                        cos_inner_2:
                            description: Determines if COS inner value 2 should be matched in this match.
                            type: bool
                        cos_inner_3:
                            description: Determines if COS inner value 3 should be matched in this match.
                            type: bool
                        cos_inner_4:
                            description: Determines if COS inner value 4 should be matched in this match.
                            type: bool
                        cos_inner_5:
                            description: Determines if COS inner value 5 should be matched in this match.
                            type: bool
                        cos_inner_6:
                            description: Determines if COS inner value 6 should be matched in this match.
                            type: bool
                        cos_inner_7:
                            description: Determines if COS inner value 7 should be matched in this match.
                            type: bool
                destination_mac_address:
                    description:
                        - Use the destination MAC address as a match criterion
                        - address format -> 00:00:00:00:00:00
                    type: str
                discard_class:
                    description:
                        - Number of the discard class being matched.
                        - Valid values are 0 to 7.
                    type: int
                field:
                    description: todo
                    type: str
                object_group_security:
                    description: Match traffic coming from, or going to a specified obejct-group.
                    type: dict
                    suboptions:
                        direction:
                            description: Match destination/source object-group security
                            type: str
                            required: true
                            choices:
                                - destination
                                - source
                        name:
                            description: Name of Object-group to match
                            type: str
                            required: true
                input_interface:
                    description: Use the specified input interface as a match criterion
                    type: dict
                    suboptions:
                        interface_name:
                            description: Name of the input interface to be used as match criteria.
                            type: str
                            required: true
                            choices:
                                - acr
                                - atm-acr
                                - analysis-module
                                - appnav-compress
                                - appnav-uncompress
                                - async
                                - auto-template
                                - bd-vif
                                - bdi
                                - bvi
                                - bluetooth
                                - cdma-ix
                                - cem-acr
                                - cem-pg
                                - ctunnel
                                - container
                                - dialer
                                - esconphy
                                - ethernet-internal
                                - fcpa
                                - filter
                                - filtergroup
                                - gmpls
                                - gigabitethernet
                                - group-async
                                - ima-acr
                                - lisp
                                - longreachethernet
                                - loopback
                                - lspvif
                                - mfr
                                - multilink
                                - nvi
                                - null_interface
                                - overlay
                                - protection_group
                                - port-channel
                                - portgroup
                                - pos-channel
                                - sbc
                                - sdh_acr
                                - serial-acr
                                - sonet_acr
                                - sslvpn-vif
                                - sysclock
                                - serial-pg
                                - service-engine
                                - tls-vif
                                - tunnel
                                - tunnel-tp
                                - vpn
                                - vif
                                - vir-cem-acr
                                - virtual-ppp
                                - virtual-template
                                - virtual-tokenring
                                - virtualportgroup
                                - vlan
                                - multiservice
                                - nve
                                - ucse
                                - vasileft
                                - vasiright
                                - vmi
                                - voabypassin
                                - voabypassout
                                - voafilterin
                                - voafilterout
                                - voain
                                - voaout
                        interface_number:
                            description:
                                - The number of the interface to match.
                                - Refer to the manual for the correct range for each type of interface.
                            type: int
                            required: true
                ip_dscp:
                    description:
                        - Match at least one and at most four IP DSCP values.
                        - Valid options include the following
                        - Numbers (0 to 63) representing differentiated services code point values
                        - AF numbers (for example, af11) identifying specific AF DSCPs
                        - CS numbers (for example, cs1) identifying specific CS DSCPs
                        - the string 'default' matches packets with default dscp (000000)
                        - the string 'ef' matches packets with EF dscp (101110)
                    type: dict
                    suboptions:
                        dscp_value_1:
                            description: The first DSCP value to match.
                            type: str
                            required: true
                        dscp_value_2:
                            description: The second DSCP value to match.
                            type: str
                            required: true
                        dscp_value_3:
                            description: The third DSCP value to match.
                            type: str
                            required: true
                        dscp_value_4:
                            description: The fourth DSCP value to match.
                            type: str
                            required: true
                ip_precedence:
                    description:
                        - A list of up to 4 IP precedence values to use as match criteria.
                        - Valid range is 0-7
                    type: list
                    elements: int
                ip_rtp:
                    description: Use the Real-Time Protocol (RTP) port as the match criterion.
                    type: dict
                    suboptions:
                        starting_port_number:
                            description:
                                - The starting RTP port number.
                                - Values range from 2000 to 65535.
                            type: int
                            required: true
                        port_range:
                            description:
                                - The RTP port number range.
                                - Values range from 0 to 16383.
                            type: int
                            required: true
                metadata:
                    description: Use call metadata as match criterion.
                    type: dict
                    mutually_exclusive: [[cac_status, called_uri, caller_uri, device_model, global_session_id, multi_party_session_id]]
                    suboptions:
                        called_uri:
                            description: Called URI
                            type: str
                        calling_uri:
                            description: Calling URI
                            type: str
                        device_model:
                            description: Device model
                            type: str
                        global_session_id:
                            description: Global Session ID (24 Chars)
                            type: str
                        multi_party_session_id:
                            description: Multi Party Session ID
                            type: str
                mpls_experimental_topmost:
                    description:
                        - Value or values of the topmost experimental (EXP) field as a match criteria
                        - EXP field values (any number from 0 through 7) to be used as a match criterion
                    type: list
                    elements: int
                packet_length:
                    description: Specify the Layer 3 packet length in the IP header as a match criterion
                    type: dict
                    suboptions:
                        max:
                            description:
                                - Maximum length value of the Layer 3 packet length, in bytes.
                                - The range is from 1 to 9216.
                            type: int
                        min:
                            description:
                                - Minimum length value of the Layer 3 packet length, in bytes.
                                - The range is from 1 to 9216.
                            type: int
                protocol:
                    description:
                        - Configure Network-Based Application Recognition (NBAR) to match traffic by a protocol (and subprotcol options) that is known to NBAR.
                        - Refer to your manual for a complete list of available protocols and subprtocol options!
                    type: dict
                    suboptions:
                        protocol_name:
                            description: The name of the protocol to be used as a match criterion.
                            required: true
                            type: str
                        subprotocol_parameter:
                            description: The subprotocol parameter to be used as a match criterion.
                            required_together: [[subprotocol_parameter_name, subprotocol_parameter_value]]
                            type: dict
                            suboptions:
                                subprotocol_parameter_name:
                                    description: The name of the subprotocol parameter to be used as match criterion.
                                    type: str
                                subprotocol_parameter_value:
                                    description: The value of the subprotocol parameter to be used as match criterion.
                                    type: str
                protocol_attribute:
                    description: Configure the match criterion based on the specified application group
                    type: dict
                    suboptions:
                        attribute_name:
                            description: Name of the protocol attribute to be used as a match criterion
                            required: true
                            type: str
                        attribute_value:
                            description: The value of the protocol attribute to be used as a match criterion
                            required: true
                            type: str
                qos_group:
                    description:
                        - To identify a specific quality of service (QoS) group value as a match criterion
                        - Values from 0 to 99 are acceptable
                    type: int
                security_group:
                    description: Security group to match.
                    type: dict
                    mutually_exclusive: [[source_tag, destination_tag]]
                    suboptions:
                        source_tag:
                            description:
                                - Source security group tag id to match.
                                - 0-65533
                            type: int
                        destination_tag:
                            description:
                                - Destination security group tag id to match.
                                - 0-65533
                            type: int
                source_mac_address:
                    description: Use the source MAC address as a match criterion
                    type: str
                start:
                    description: Configure match criteria on the basis of the datagram header (Layer 2 ) or the network header (Layer 3).
                    type: dict
                    mutually_exclusive: [[eq, neq, gt, lt, range, regex]]
                    suboptions:
                        layer:
                            description: Determines the layer which the criterion will start from.
                            type: str
                            required: true
                            choices:
                                - l2
                                - l3
                        offset:
                            description:
                                - Match criterion can be made according to any aribitrary offset.
                                - Valid values 0-255
                            type: int
                            required: true
                        size:
                            description:
                                - The number of bytes to match on
                                - Valid values 1-32
                            type: int
                            required: true
                        eq:
                            description: Match criteria is met if the packet is equal to the specified value or mask.
                            type: dict
                            suboptions:
                                value:
                                    description:
                                        - Value for which the packet must be in accordance with.
                                        - Valid range is 0-255
                                    type: int
                                    required: true
                                mask:
                                    description:
                                        - Mask value
                                        - Valid range is 0-255
                                    type: int
                        neq:
                            description: Match criteria is met if the packet is not equal to the specified value or mask.
                            type: dict
                            suboptions:
                                value:
                                    description:
                                        - Value for which the packet must be in accordance with.
                                        - Valid range is 0-255
                                    type: int
                                    required: true
                                mask:
                                    description:
                                        - Mask value
                                        - Valid range is 0-255
                                    type: int
                        gt:
                            description:
                                - Match criteria is met if the packet is greater than the specified value.
                                - Valid range is 0-255
                            type: int
                        lt:
                            description:
                                - Match criteria is met if the packet is less than the specified value.
                                - Valid range is 0-255
                            type: int
                        range:
                            description: Match critera is based upon a lower and upper boundary protocol field range.
                            type: dict
                            suboption:
                                lower_boundary:
                                    description: Acceptable range is 0-255
                                    type: int
                                    required: true
                                upper_boundary:
                                    description: Acceptable range is 0-255
                                    type: int
                                    required: true
                        regex:
                            description: Match critera is based upon a string that is to be matched.
                            type: str
                traffic_category:
                    description: 
                    type: str
                    choices:
                        - allow
                        - optimize
                vlan_id:
                    description:
                        - Use the VLAN IDas a match criterion.
                        - Valid from 1 to 4049
                    type: int
                vlan_id_inner:
                    description:
                        - Use the inner VLAN IDas a match criterion.
                        - Valid from 1 to 4049
                    type: int
                negate:
                    description: Negate this match result.
                    type: bool
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
    description: description here
    type: str
"""

EXAMPLES = """

"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.class_maps.class_maps import (
    Class_mapsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.class_maps.class_maps import (
    Class_maps,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Class_mapsArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Class_maps(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
