from nxos_prefix_finder.Devices import Nexus

n = Nexus('192.168.51.128','admin', 'c!sco123')
ncdata = n.search_for_prefix('192.168.2.0/24')
print ncdata # ['vrf2']
