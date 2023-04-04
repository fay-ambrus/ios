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
        class_map_type:
            description:
                - Determines the type of the class map.
                - For more informtion on different Class-Map types, refer to the manual.
            default: inspect
            type: str
            choices:
                - access-control
                - appnav
                - control
                - inspect
                - multicast-flows
                - site-manager
                - stack
                - traffic
        class_map_decription:
            description: Comment or a description that is added to the class map.
            type: str
        matches:
            description: A list of classification criteria.
            type: list
            elements: dict
            suboptions:
                match:
                    description: A criterion to match.
                    type: dict
                    required: true
                    mutually_exclusive:
                        - [access_groups]
                        - [any]
                        - [application_metadata]
                        - [class_map_name]
                        - [cos]
                        - [cos_inner]
                        - [desination_address_mac]
                        - [discard_class]
                        - [object_group_security]
                        - [input_interface]
                        - [ip_dscp]
                        - [ip_precedence]
                        - [ip_rtp]
                        - [metadata]
                        - [mpls_experimental]
                        - [packet_length]
                        - [protocol]
                        - [protocol_nbar]
                        - [protocol_attribute]
                        - [qos_group]
                        - [security_group]
                        - [source_mac_address]
                        - [traffic_category]
                        - [vlan_id]
                        - [vlan_id_inner]
                    suboptions:
                        access_groups:
                            description:
                                - Access-groups to match.
                                - Identified by a name or number.
                            type: dict
                            mutually_exclusive: [[name], [number]]
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
                            description:
                                - Configures the match criteria to be successful for all packets.
                            type: bool
                        application_metadata:
                            description:
                                - Use application metadata as a match criterion for classification.
                            type: list
                            elements: dict
                            mutually_exclusive: [[regexp], [application_group], [attribute], [application_name]]
                            suboptions:
                                application_group:
                                    description:
                                        - Application Group to match
                                    type: str
                                    choices:
                                        - telepresence-group
                                        - vmware-group
                                        - webex-group
                                application:
                                    description:
                                        - Specific applications to match.
                                        - Also restrictable to source, vendor etc.
                                    type: dict
                                    mutually_exclusive: [[application_name], [application_name_regexp]]
                                    suboptions:
                                        application_name:
                                            description: The name of the application to match.
                                            type: dict
                                            suboptions:
                                                cisco_phone:
                                                    description: Cisco IP Phones and PC-based Unified Communicators
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
                                                        traffic_type:
                                                            description: Traffic Type
                                                            type: str
                                                            choices:
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
                                        application_name_regexp:
                                            description: Match all packets with applicaiton name matching the given regular expression.
                                            type: str
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
                                attribute:
                                    description:
                                        - Specifies the relevant attribute to match.
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
                        class_map_name:
                            description: Name of the traffic class to use as a match criterion.
                            type: str
                        cos:
                            description:
                                - Match a packet on the basis of a Layer 2 class of service (CoS)/Inter-Switch Link (ISL) marking
                                - Up to 8  class-of-service values may be entered
                            type: list
                            elements: int
                        cos_inner:
                            description:
                                - Match the inner cos of QinQ packets on a Layer 2 class of service (CoS) marking
                                - UP to 4 class-of-service values may be entered.
                            type: list
                            elements: int
                        desination_address_mac:
                            description:
                                - Use the destination MAC address as a match criterion
                                - address format -> 00:00:00:00:00:00
                            type: str
                        discard_class:
                            description:
                                - Number of the discard class being matched.
                                - Valid values are 0 to 7.
                            type: int
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
                                interface_nubmer:
                                    description:
                                        - The number of the interface to match.
                                        - Refer to the manual for the correct range for each type of interface.
                                    type: int
                                    required: true
                        ip_dscp:
                            description:
                            type: dict
                            mututually_exclusive: [[dscp_values], [dscp_af_values], [dscp_cp_values], [default_value], [ef_value]]
                            suboptions:
                                dscp_values:
                                    description: Numbers (0 to 63) representing differentiated services code point values
                                    type: list
                                    elements: int
                                dscp_af_values:
                                    description: AF numbers (for example, af11) identifying specific AF DSCPs
                                    type: dict
                                    suboptions:
                                        af11:
                                            description: Match packets with AF11 dscp (001010)
                                            type: bool
                                        af12:
                                            description: Match packets with AF12 dscp (001100)
                                            type: bool
                                        af13:
                                            description: Match packets with AF13 dscp (001110)
                                            type: bool
                                        af21:
                                            description: Match packets with AF21 dscp (010010)
                                            type: bool
                                        af22:
                                            description: Match packets with AF22 dscp (010100)
                                            type: bool
                                        af23:
                                            description: Match packets with AF23 dscp (010110)
                                            type: bool
                                        af31:
                                            description: Match packets with AF31 dscp (011010)
                                            type: bool
                                        af32:
                                            description: Match packets with AF32 dscp (011100)
                                            type: bool
                                        af33:
                                            description: Match packets with AF33 dscp (011110)
                                            type: bool
                                        af41:
                                            description: Match packets with AF41 dscp (100010)
                                            type: bool
                                        af42:
                                            description: Match packets with AF42 dscp (100100)
                                            type: bool
                                        af43:
                                            description: Match packets with AF43 dscp (100110)
                                            type: bool
                                dscp_cp_values:
                                    dscription: CS numbers (for example, cs1) identifying specific CS DSCPs
                                    type: dict
                                    suboptions:
                                        cs1:
                                            description: Match packets with CS1(precedence 1) dscp (001000)
                                            type: bool
                                        cs2:
                                            description: Match packets with CS2(precedence 2) dscp (010000)
                                            type: bool
                                        cs3:
                                            description: Match packets with CS3(precedence 3) dscp (011000)
                                            type: bool
                                        cs4:
                                            description: Match packets with CS4(precedence 4) dscp (100000)
                                            type: bool
                                        cs5:
                                            description: Match packets with CS5(precedence 5) dscp (101000)
                                            type: bool
                                        cs6:
                                            description: Match packets with CS6(precedence 6) dscp (110000)
                                            type: bool
                                        cs7:
                                            description: Match packets with CS7(precedence 7) dscp (111000)
                                            type: bool
                                default_value:
                                    description: Match packets with default dscp (000000)
                                    type: bool
                                ef_value:
                                    description: Match packets with EF dscp (101110)
                                    type: bool
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
                            mutually_exclusive: [[cac_status], [called_uri], [caller_uri]]
                            suboptions:
                                cac_status:
                                    description: Call Admission Control status
                                    type: str
                                    choices:
                                        - admitted
                                        - un-admitted
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
                        mpls_experimental:
                            description:
                                - Value or values of the experimental (EXP) field as a match criteria
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
                                - Match criterion on the basis of a specified protocol
                                - For a complete list of supported protocols, see the online help for the matchprotocol command on the router that you are using.
                            type: str
                        protocol_nbar:
                            description:
                                - Configure Network-Based Application Recognition (NBAR) to match traffic by a protocol type that is known to NBAR.
                                - To get a complete list of the available NBAR protocols, refer to your manual.
                            type: dict
                            suboptions:
                                protocol_name:
                                    description: Particular protocol type that is known to NBAR.
                                    type: str
                                    required: true
                                variable_field_name:
                                    description:  Predefined variable that was created when you created a custom protocol.
                                    type: str
                                value:
                                    description: Specific value in the custom payload to match.
                                    type: str
                        protocol_attribute:
                            description: Configure the match criterion based on the specified application group
                            type: dict
                            mutually_exclusive: [[application_family], [application_group], [application_set], [business_relevance], [category], [encrypted], [sub_category], [traffic-class], [tunnel]]
                            suboptions:
                                application_family:
                                    description:
                                        - Name of the application family as a matching criterion
                                        - Refer to the manual for available application families!
                                    type: str
                                application_group:
                                    description:
                                        - Name of the application group as a matching criterion
                                        - Refer to the manual for available application families!
                                    type: str
                                application_set:
                                    description:
                                        - Name of the application set as a matching criterion
                                        - Refer to the manual for available application families!
                                    type: str
                                business_relevance:
                                    description: Relevance of business traffic to use as matching criterion
                                    type: str
                                    choices:
                                        - business-ireelevant
                                        - business-relevant
                                        - default
                                category:
                                    description:
                                        - Name of the application category used as a matching criterion.
                                        - Refer to the manual for available application families!
                                    type: str
                                encrypted:
                                    description:
                                    type: str
                                    choices:
                                        - encrypted_yes
                                        - encrypted_no
                                        - encrypted_unassigneds
                                sub_category:
                                    description:
                                        - Name of the application sub-category used as a matching criterion.
                                        - Refer to the manual for available application families!
                                    type: str
                                traffic_class:
                                    description: Name of the SRND class to match.
                                    type: str
                                    choices:
                                        - broadcast-video
                                        - bulk-data
                                        - multimedia-conferencing
                                        - multimedia-streaming
                                        - network-control  
                                        - ops-admin-mgmt
                                        - real-time-interactive
                                        - signaling
                                        - transactional-data
                                        - voip-telephony
                        qos_group:
                            description:
                                - To identify a specific quality of service (QoS) group value as a match criterion
                                - Values from 0 to 99 are acceptable
                            type: int
                        security_group:
                            description: Security group to match.
                            type: dict
                            mutually_exclusive: [[source_tag], [destination_tag]]
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
                        traffic_category:
                            description: I literally can't find anything on what this actually means...
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
                    default: false
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
from ansible_collections.cisco.class_maps.plugins.module_utils.network.ios.argspec.class_maps.class_maps import (
    Class_mapsArgs,
)
from ansible_collections.cisco.class_maps.plugins.module_utils.network.ios.config.class_maps.class_maps import (
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
