#!/usr/bin/python3
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import argparse
import subprocess
import time

setLogLevel('info')

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--count", help="Number of nodes", default=1)
parser.add_argument("-s", "--size", help="filesize", default="10M")
parser.add_argument("-d", "--delay", help="delay between node hosting data and switch", default="500ms")
parser.add_argument("-b", "--bandwidth", help="bandwidth between node hosting data and switch", default=1)
args = parser.parse_args()
count = int(args.count)
file_size = args.size
delay = args.delay
bw = int(args.bandwidth)


net = Containernet(controller=Controller)

info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')

info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')

net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=2)

for i in range(1, count+1):
    d_node = f'd{i}'

    net.addDocker(d_node, ip=f'192.168.1.{i}', dimage="ubuntu-ipfs", ports=[80])

    if (i % 2) == 0:
        info(f'*** Linking node {d_node} to switch {s1}  \n')
        net.addLink(s1, net[d_node], cls=TCLink)
    else:
        if i == 1:
            # starting ngnix on d1
            info('*** Installing nginx on d1\n')
            net[d_node].cmd('sudo /etc/init.d/nginx start')
            # generating data on http server
            info(f'*** Generating file of size {file_size} at /usr/share/nginx/html/data.txt  \n')
            net[d_node].cmd(f'sudo truncate -s {file_size} /usr/share/nginx/html/data.txt')

            # linking node hosting download data to switch
            info(f'*** Linking node hosting download data (d1) to switch with delay of {delay} and bandwidth of {bw} \n')
            net.addLink(net[d_node], s2, cls=TCLink, delay=delay, bw=bw)
        else:
           # install wget 
           info(f'*** Linking switch {s2} and node {d_node}  \n')
           net.addLink(s2, net[d_node], cls=TCLink)

info('*** Starting network\n')
net.start()

# do the ipfs thing
cid = ''
for i in range(1, count+1):
    d_node = f'd{i}'

    net[d_node].cmd('ipfs init --profile=badgerds')
    if d_node == 'd1':
       info('*** Adding generated date to ipfs\n') 
       cid = net["d1"].cmd('ipfs add -Q /usr/share/nginx/html/data.txt').rstrip()
       info(f'*** Starting ipfs for node d1\n')
       net['d1'].cmd('sudo ipfs daemon --migrate=true &')
    else:
       info(f'*** Starting ipfs for node {d_node}\n') 
       net[d_node].cmd('sudo ipfs daemon --migrate=true &')


# perform retrieval
f = open("output.csv", "w")
f.write("'node','type','filesize','real','user','sys'\n")
for i in range(2, count+1):
    d_node = f'd{i}'

    result = net[d_node].cmd(f'time -p ipfs get {cid} --output=/tmp/ipfs/data.txt')
    info(f'*** Finished data retrieval via ipfs on node {d_node} \n')

    splitted = result.split('\n')
    
    #print(f'ipfs: length of result: {len(splitted)}')
    if (len(splitted) == 10):
        # strange first time is always with previous log outputi
        real = splitted[6].split(" ")[1].rstrip()
        user = splitted[7].split(" ")[1].rstrip()
        sys  = splitted[8].split(" ")[1].rstrip()
        f.write(f"d{i},'ipfs','{file_size}','{real}','{user}','{sys}'\n")
    else:
        real = splitted[19].split(" ")[1].rstrip()
        user = splitted[20].split(" ")[1].rstrip()
        sys  = splitted[21].split(" ")[1].rstrip()
        f.write(f"{d_node},'ipfs','{file_size}','{real}','{user}','{sys}'\n")

for i in range(2, count+1):
    
    d_node = f'd{i}'
    
    result = net[d_node].cmd(f"time -p wget -q http://172.17.0.2/data.txt -P /tmp/http/data.txt")
    info(f'*** Finished data retrieval via http on node {d_node} \n')

    splitted = result.split('\n')
    #print(f'http: length of result: {len(splitted)}')

    if (len(splitted) == 21):
        real = splitted[17].split(" ")[1].rstrip()
        user = splitted[18].split(" ")[1].rstrip()
        sys  = splitted[19].split(" ")[1].rstrip()
        f.write(f"d{i},'http','{file_size}','{real}','{user}','{sys}'\n")
    elif (len(splitted) == 9):
        real = splitted[5].split(" ")[1].rstrip()
        user = splitted[6].split(" ")[1].rstrip()
        sys  = splitted[7].split(" ")[1].rstrip()
        f.write(f"d{i},'http','{file_size}','{real}','{user}','{sys}'\n")
    elif (len(splitted) == 4):
        real = splitted[0].split(" ")[1].rstrip()
        user = splitted[1].split(" ")[1].rstrip()
        sys  = splitted[2].split(" ")[1].rstrip()
        f.write(f"d{i},'http','{file_size}','{real}','{user}','{sys}'\n")
    else:
        exit("Unexpected output")

# TODO Add a final step that check in all the node that the file was indeed transfered and of the right size

info('*** Benchmark completed. You can now exit and check generated output.csv\n')

CLI(net)
#info('*** Stopping network')

#net.stop()
