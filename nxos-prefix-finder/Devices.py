#!/usr/bin/env python
import xml.etree.ElementTree as ET
from ncclient import manager

VLAN_POOL_NAME = 'acimigrate-vlan-pool'


class Nexus(object):
    """
    Class for gleaning useful information from an NX-OS device

    """

    def __init__(self, host, user, passwd):

        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = 22
        self.hostkey_verify = False
        self.device_params = {'name': 'nexus'}
        self.allow_agent = False
        self.look_for_keys = False
        self.manager = manager.connect(host=self.host,
                                       port=22,
                                       username=self.user,
                                       password=self.passwd,
                                       hostkey_verify=False,
                                       device_params={'name': 'nexus'},
                                       allow_agent=False,
                                       look_for_keys=False)



    def build_xml(self, cmd):
        args = cmd.split(' ')
        xml = ""
        for a in reversed(args):
            xml = """<%s>%s</%s>""" % (a, xml, a)
        return xml

    def run_cmd(self, cmd):
        xml = self.build_xml(cmd)
        ncdata = str(self.manager.get(('subtree', xml)))
        return ncdata

    @staticmethod
    def format_mac_address(mac):
        """
        Re-format IOS mac addresses
        :param mac: string mac address in 0000.0000.0000 format
        :return: string 00:00:00:00:00
        """
        return '{0}:{1}:{2}:{3}:{4}:{5}'.format(mac[:2],
                                                mac[2:4],
                                                mac[5:7],
                                                mac[7:9],
                                                mac[10:12],
                                                mac[12:14])


    def search_for_prefix(self, prefix):
        """
        Find VRF name containing a prefix
        """
        query = self.build_xml('show ip route vrf all')
        ncdata = str(self.manager.get(('subtree', query)))
        root = ET.fromstring(ncdata)
        neighbors = {}
        mod = {'mod': 'http://www.cisco.com/nxos:1.0:urib'}

        # it is entirely possible that the prefix could exist in many prefixes
        vrfs = list()

        for vrf in root.iter(tag='{http://www.cisco.com/nxos:1.0:urib}ROW_vrf'):
            name = vrf.find('mod:vrf-name-out', mod)
            for pfx in vrf.iter(tag='{http://www.cisco.com/nxos:1.0:urib}ipprefix'):
                if pfx.text == prefix:
                    vrfs.append(name.text)

        return vrfs
        
