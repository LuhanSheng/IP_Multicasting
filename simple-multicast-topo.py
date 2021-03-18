from __future__ import print_function
# Copyright (C) 2016 Huang MaChi at Chongqing University
# of Posts and Telecommunications, China.
# Copyright (C) 2016 Li Cheng at Beijing University of Posts
# and Telecommunications. www.muzixing.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
#from mininet.util import dumpNodeConnections

import logging
import os
import time



class Star(Topo):
    """
        Class of Leaf Spine Topology.
    """
    def __init__(self, 
            host_num=5, 
            of_version='OpenFlow13',
            bw=100,
            max_queue_size=1000,
            lat=1,
        ):

        self.of_version = of_version
        # Init Topo
        #Topo.__init__(self)
        super().__init__()
        self.host_num = host_num
        self.switch = self.addSwitch('s1')

        for i in range(host_num):
            host_name = self.gen_host_name(i)
            ip = "10.%d.%d.%d" % (0, i, 100)
            h = self.addHost(host_name, ip=ip)
            self.addLink(
                self.switch, 
                h, 
                bw=bw,
                max_queue_size=max_queue_size,
                lat=lat,
            ) 
            # TODO: update link bandwidth and latency .....

        self.net = None

    def sys_shell(self, cmd):
        cmd = cmd.replace('\t', "").replace('\n', "")
        print('# debug, cmd:', cmd)
        return os.system(cmd)

    def set_ovs_protocol(self):
        for sw_name in self.switches():
            cmd = "sudo ovs-vsctl set bridge %s protocols=%s" % (sw_name, self.of_version)
            self.sys_shell(cmd)
    
    def configure_default_multicast_routes(self, net=None):
        if net is None:
            net = self.net
        for i in range(self.host_num):
            host_name = self.gen_host_name(i)
            h = net.get(host_name)
            cmd_str = "route add -net 224.0.0.0 netmask 224.0.0.0 " + host_name + '-eth0'
            h.cmd(cmd_str)
    
    def get_host_ip(self, host_name):
        h = self.net.get(host_name)
        return h.IP()

    def get_port_pairs(self, u, v):
        port_pairs = self.port(u, v)
        if isinstance(port_pairs[0], int):
            return [port_pairs, ]
        else:
            return port_pairs

    def gen_host_name(self, i):
            return 'H{0}'.format(i)

    def install_forwarding_rules(self, net=None):
        """
        """
        if net is None:
            net = self.net

        protos = ['ip', ]
        
        # switch
        default_table_id = 0
        for i in range(self.host_num):
            port_at_switch, _ = self.get_port_pairs(self.switch, self.gen_host_name(i))[0]
            subnet = '10.{0}.{1}.0/24'.format(0, i) #"10.%d.%d.%d
            # ip,nw_dst=%s
            
            cmd = "ovs-ofctl add-flow %s -O %s \
                'table=%d,idle_timeout=0,hard_timeout=0,priority=50,ip,nw_dst=%s,actions=output:%d'" % (
                    self.switch, self.of_version, default_table_id, subnet, port_at_switch)
            self.sys_shell(cmd)
        
        # multicast forwarding rules
        for i in range(self.host_num):
            mgroup_ip = "239.0.0.{0}".format(i+1)
            lst = []
            for j in range(self.host_num):
                if i == j:
                    continue
                port = self.get_port_pairs(self.switch, self.gen_host_name(j))[0][0]
                lst.append('bucket=output:{0}'.format(port))

            bucket_s = ','.join(lst)
            mgroup_id = i + 1
            cmd = "ovs-ofctl add-group %s -O %s \
            'group_id=%d,type=all,%s'" % (self.switch, self.of_version, mgroup_id, bucket_s)
            self.sys_shell(cmd)
            
            for pro in protos:
                cmd = "ovs-ofctl add-flow %s -O %s \
                    'table=%d,priority=10,%s,nw_dst=%s,actions=group:%d'" % (self.switch, self.of_version, default_table_id, pro, mgroup_ip, mgroup_id) # TODO
                self.sys_shell(cmd)


    def build_net(self):	
        # Start Mininet.
        net = Mininet(topo=self, link=TCLink, autoSetMacs=True, autoStaticArp=True, controller=None)
        
        net.start()

        self.net = net

        # Set OVS's protocol as OF13.
        self.set_ovs_protocol()
        # Set hosts IP addresses.
        #time.sleep(1)
        self.configure_default_multicast_routes()
        self.install_forwarding_rules()
        return net

    def cli(self):
        net = self.net

        CLI(net)
        net.stop()

    def run(self):
        if self.net is None:
            self.build_net()
        return self.cli()



def run_exmaple():
    net = Star()
    print('dcn created!')
    net.run()
        

if __name__ == '__main__':
    setLogLevel('info')
    # ryu-manager --observe-links ryu.app.gui_topology.gui_topology

    if os.getuid() != 0:
        logging.debug("You are NOT root")
    elif os.getuid() == 0:
        run_exmaple()
