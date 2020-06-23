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
parser.add_argument("-d", "--delay", help="delay between nodes and switch", default="500ms")
parser.add_argument("-b", "--bandwidth", help="bandwidth between all nodes and switch", default=1)
parser.add_argument("-t", "--type", help="type of benchmark to run", default="http")
parser.add_argument("-ds", "--delayserver", help="delay between node hosting data and switch", default="1500ms")
args = parser.parse_args()
count = int(args.count)
file_size = args.size
delay = args.delay #General delay between all hosts
delay_server = args.delayserver 
bw = int(args.bandwidth)
t_type = args.type 


net = Containernet(controller=Controller)

info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')

info('*** Adding switches\n')
s1 = net.addSwitch('s1')
#s2 = net.addSwitch('s2')

#net.addLink(s1, s2, cls=TCLink, delay='1500ms', bw=2)

docks = []
for i in range(1, count+1):
    d_node = f'd{i}'

    info(f'*** Adding container {d_node}.\n')
    docks.append(net.addDocker(d_node, ip=f'192.168.1.{i}/24', dimage="ubuntu-ipfs", ports=[80], mem_limit="1g"))

    #if (i % 2) == 0:
    #    info(f'*** Linking node {d_node} to switch {s1}  \n')
    #    net.addLink(s1, net[d_node], cls=TCLink)
    #else:
    if (i == 1):
       # linking node hosting download data to switch
       info(f'*** Linking node hosting download data (d1) to switch with delay of {delay} and bandwidth of {bw} \n')
       net.addLink(s1, net[d_node], cls=TCLink, delay=delay_server, bw=bw)

       if (t_type == "http"): # Configure HTTP server
            # starting ngnix on d1
            info('*** Installing nginx on d1\n')
            net[d_node].cmd('sudo /etc/init.d/nginx start')
            # generating data on http server
            info(f'*** Generating file of size {file_size} at /usr/share/nginx/html/data.txt for HTTP \n')
            net[d_node].cmd(f'sudo truncate -s {file_size} /usr/share/nginx/html/data.txt')

            #net.addLink(net[d_node], s2, cls=TCLink)
       elif (t_type == "ipfs"): # Configure IPFS "server". File origin.
            # generating data on first ipfs node
            info(f'*** Generating file of size {file_size} at /tmp/data.txt for IPFS  \n')
            resu=net[d_node].cmd(f'time sudo dd if=/dev/urandom of=/tmp/data.txt bs=4096 count=12800')
            info(f'{resu} TIM TIME TIME\n')
       else:
            print("unexpected experiment type")
    else:
        info(f'*** Linking switch {s1} and node {d_node}  \n')
        net.addLink(s1, net[d_node],delay=delay, cls=TCLink, bw=bw)

info('*** Starting network\n')
net.start()

cid = ''
# do the ipfs thing
if (t_type == "ipfs"):
  for i in range(1, count+1):
      d_node = f'd{i}'
      print(f"running on {d_node}")
#      net[d_node].cmd(f'export IPFS_PATH=/tmp/{d_node}')

      net[d_node].cmd('ipfs init --profile=badgerds')
      if d_node == 'd1':
         info('*** Adding generated data to ipfs\n') 
         cid = net[d_node].cmd('ipfs add -Q /tmp/data.txt').rstrip()
         print(f"*** CID of data is {cid}")
         info(f'*** Starting ipfs for node d1\n')
         docks[i-1].start()
         #start_result = net[d_node].cmd('sudo ipfs daemon --migrate=true &')
         print("result of starting ipfs command")
         #print(start_result)
      else:
         info(f'*** Starting ipfs for node {d_node}\n') 
         docks[i-1].start()
         #start_result = net[d_node].cmd('sudo ipfs daemon --migrate=true &')
         print("result of starting ipfs command")
         #print(start_result)


f = open("output.csv", "w")
f.write("'node','type','filesize','real','user','sys'\n")

time.sleep(30)
# perform retrieval
def run_ipfs():

  for i in range(2, count+1):
      d_node = f'd{i}'


      result = net[d_node].cmd(f'time -p ipfs get {cid} --output=/tmp/ipfs/data.txt; sync')
      info(f'*** Finished data retrieval via ipfs on node {d_node} \n')

      print(result)
      
      splitted = result.split('\n')
      print(splitted)
      length = len(splitted)

      real = splitted[length-4].split(" ")[1].rstrip()
      user = splitted[length-3].split(" ")[1].rstrip()
      sys  = splitted[length-2].split(" ")[1].rstrip()
      f.write(f"{d_node},'ipfs','{file_size}','{real}','{user}','{sys}'\n")


def run_http():

  for i in range(2, count+1):
    
      d_node = f'd{i}'
    
      result = net[d_node].cmd(f"time -p wget -q http://192.168.1.1/data.txt -P /tmp/http/data.txt; sync")
      time.sleep(2)
      info(f'*** Finished data retrieval via http on node {d_node} \n')
    
      splitted = result.split('\n')
      print(splitted)

      length = len(splitted)
      real = splitted[length-4].split(" ")[1].rstrip()
      user = splitted[length-3].split(" ")[1].rstrip()
      sys  = splitted[length-2].split(" ")[1].rstrip()
      f.write(f"d{i},'http','{file_size}','{real}','{user}','{sys}'\n")

if (t_type == "http"):
    info('*** Starting HTTP benchmark run')
    run_http()
elif (t_type == "ipfs"):
    info('*** Starting IPFS benchmark run')
    run_ipfs()
else:
    exit("wrong experiment type")


info('*** Running CLI\n')

CLI(net)
#info('*** Stopping network')

#net.stop()
