# -*- encoding: utf-8 -*-
'''
Created on 16 авг. 2015 г.

@author: Руслан
'''

#!/usr/bin/python

import struct, socket

RANGE_LIMIT = 80
IP_DEC_LENGTH = 10
IPV4_BITS = 32

ip2dec = lambda ip: struct.unpack("!L", socket.inet_aton(ip))[0]
dec2ip = lambda dec: socket.inet_ntoa(struct.pack('!L',dec))
leastbyte = lambda dec: (dec >> 8 << 8) ^ dec

makeIdIp = lambda net_id, ip_decimal: int(str(net_id) + "%%0%sd" % IP_DEC_LENGTH % ip_decimal)
splitIdIp = lambda Id: (int(str(Id)[:-IP_DEC_LENGTH]), int(str(Id)[-IP_DEC_LENGTH:]))

if __name__ == '__main__':
    _host_table = []
    _host_used_by_network = {}

    net1 = {'id':1, 'mask':24, 'ip':'192.168.0.0'}
    net2 = {'id':2, 'mask':20, 'ip':'192.168.1.0'}
    net3 = {'id':3, 'mask':29, 'ip':'186.25.10.1'}

    all_ids = [
        23232235778,23232235790,23232235791,23232235792,23232235854,23232235853,23232235856,
        33122203138L,33122203142L,33122203141L
    ]

    for a in all_ids:
        net_id, ip_dec = splitIdIp(a)
        _host_used_by_network.setdefault(net_id, []).append(ip_dec)

    ### CURRENT NETWORK ###
    net = net2
    #######################

    ### return 'host_range' for function _get_hosts ###
    shift_mask = IPV4_BITS-net['mask']
    host_min = (ip2dec(net['ip']) >> shift_mask << shift_mask)
    host_max = (ip2dec(net['ip']) >> shift_mask << shift_mask)+pow(2, shift_mask)
    #if host_max-host_min > RANGE_LIMIT:
    #    host_max = host_min + RANGE_LIMIT + len(_host_used_by_network.get(net['id'],[]))
    host_range = range(host_min, host_max)
    host_range = list(set(host_range)-set(_host_used_by_network.get(net['id'],[])))
    ###################################################

    ### return 'ids' for function search ###
    _host_table = map(lambda ip:{'id':ip,'ip':dec2ip(ip),'network_id':net['id']}, host_range)

    search_name = "192.168.1" # example
    
    host_range = filter(lambda ip_dec: \
        dec2ip(ip_dec).startswith(search_name) and \
        leastbyte(ip_dec) not in [0,255], host_range)

    ids = map(lambda ip: makeIdIp(net['id'], ip), host_range)
    ########################################

    print map(dec2ip, host_range)[:RANGE_LIMIT]
    print ids[:RANGE_LIMIT], len(ids)
    ids = ids[:RANGE_LIMIT]


    #### return 'res' for function read ###
    res = map(lambda id: {'id':id, 'ip':dec2ip(splitIdIp(id)[1])}, ids)
    print res
    #######################################
    

    
