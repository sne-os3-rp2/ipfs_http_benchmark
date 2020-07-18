#!/usr/bin/python3
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import argparse
import subprocess
import time
import datetime

setLogLevel('info')

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--count", help="Number of nodes", default=1)
parser.add_argument("-s", "--size", help="filesize in MiB; e.g. 10", default="10")
parser.add_argument("-d", "--delay", help="delay between nodes and switch", default="50ms")
parser.add_argument("-b", "--bandwidth", help="bandwidth between all nodes and switch", default=1000)
parser.add_argument("-t", "--type", help="type of benchmark to run", default="https")
parser.add_argument("-ds", "--delayserver", help="delay between node hosting data and switch", default="150ms")
parser.add_argument("-n", "--naptime", help="Sleep time before test start. (may influence results)", default="10")
parser.add_argument("-cf", "--file_count",  help="Number of files to create. Size of each file is specified by -s flag", default="10")
parser.add_argument("-cb", "--bandwidth_sample_count",  help="Number of files to sample the bandwidth", default="5")
parser.add_argument("-wd", "--with_data",  help="Do bandwidth test with data", default=False)


args = parser.parse_args()
count = int(args.count)
file_size = int(args.size) * 256 # Convert MiB to chunks of 4096 bytes
delay = args.delay #General delay between all hosts
delay_server = args.delayserver
bw = int(args.bandwidth)
t_type = args.type
naptime = int(args.naptime)
file_count = int(args.file_count)
bandwidth_sample_count = int(args.bandwidth_sample_count)
watch_with_data = args.with_data

net = Containernet(controller=Controller)

info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')

info('*** Adding switches\n')
s1 = net.addSwitch('s1')
#s2 = net.addSwitch('s2')

#net.addLink(s1, s2, cls=TCLink, delay='1500ms', bw=2)

http_dir_location = "/usr/share/nginx/html/"
ipfs_dir_location = "/tmp/upload/"
peerid = None #peerid of publishing node

def generate_data(file_size, count, node, location):
    for i in range(1, count + 1):
        node.cmd(f'sudo dd if=/dev/urandom of={location}/{i}.txt bs=4096 count={file_size}')



docks = []
for i in range(1, count+1):
    d_node = f'd{i}'
    bootnode = True if i == 1 else False

    info(f'*** Adding container {d_node}.\n')
    docks.append(net.addDocker(d_node, ip=f'192.168.1.{i}/24', dimage="ubuntu-ipfs:latest", ports=[80], #mem_limit="1g",
        environment={
            "ENV_SWARM_KEY":"09b7fe038a241d5e38650b0f1811933644d6195814f863902d44698fa38b8cfa",
            "BOOTNODE_IP":"192.168.1.1",
            "IS_BOOTNODE":bootnode
            },
        cpu_quota=40000, cpu_period=100000
        ))

    if (i == 1):
       # linking node hosting download data to switch
       info(f'*** Linking node hosting download data (d1) to switch with delay of {delay} and bandwidth of {bw} \n')
       net.addLink(s1, net[d_node], cls=TCLink, delay=delay_server, bw=bw)

       if (t_type == "https"): # Configure HTTPS server
            # starting ngnix on d1
            info('*** Installing nginx on d1\n')
            net[d_node].cmd('sudo /etc/init.d/nginx start')
            # generating data on http server
            #info(f'*** Generating file of size {file_size} at /usr/share/nginx/html/data.txt for HTTPS \n')

            generate_data(file_size, file_count, net[d_node], http_dir_location)

            #net[d_node].cmd(f'sudo dd if=/dev/urandom of=/usr/share/nginx/html/data.txt bs=4096 count={file_size}')

            #net.addLink(net[d_node], s2, cls=TCLink)
       elif (t_type == "ipfs"): # Configure IPFS "server". File origin.
            # generating data on first ipfs node
            info(f'*** Generating file of size {file_size} at /tmp/data.txt for IPFS  \n')
            generate_data(file_size, file_count, net[d_node], ipfs_dir_location)
            # net[d_node].cmd(f'sudo dd if=/dev/urandom of=/tmp/data.txt bs=4096 count={file_size}')
       elif t_type == "bandwidth" and watch_with_data == "True":
            info(f'*** Generating file of size {file_size} at /tmp/data.txt for IPFS bandwidth watch  \n')
            generate_data(file_size, file_count, net[d_node], ipfs_dir_location)
       else:
            print("unexpected experiment type")
    else:
        info(f'*** Linking switch {s1} and node {d_node}  \n')
        net.addLink(s1, net[d_node],delay=delay, cls=TCLink, bw=bw)

info('*** Starting network\n')
net.start()


cid = None
peerid = None
# Configure and boot IPFS nodes
if (t_type == "ipfs" or t_type == "bandwidth"):
    for i in range(1, count+1):
        d_node = f'd{i}'
        print(f"running on {d_node}")

        net[d_node].cmd('ipfs init --profile=badgerds')

        if d_node == 'd1':
#           time.sleep(2)
           garbo = net[d_node].cmd('echo "ravioli"') # "flush" stdout on host
           #cid = net[d_node].cmd('ipfs add -Q /tmp/data.txt').rstrip()
           time.sleep(2)
           garbo = net[d_node].cmd('echo "ravioli"') # "flush" stdout on host
           time.sleep(0.1)
           if t_type == 'ipfs':
               info('*** Adding generated data to ipfs\n')
               cid = net[d_node].cmd(f'ipfs add -Q -r {ipfs_dir_location}').rstrip()
               print(f"*** CID of data is {cid}")
           if t_type == 'bandwidth' and watch_with_data == 'True':
               pass
               info('*** Adding generated data to ipfs for bandwidth watch\n')
               cid = net[d_node].cmd(f'ipfs add -Q -r {ipfs_dir_location}').rstrip()
               print(f"*** CID of data is {cid}")
           while peerid == None:
               peerid = net[d_node].cmd('ipfs id -f "<id>"')
               while ("failed" in peerid or "error" in peerid):
                    peerid = net[d_node].cmd('ipfs id -f "<id>"')

        # Change bootstrap node:
        #net[d_node].cmd('ipfs shutdown')
        net[d_node].cmd('ipfs bootstrap rm --all')
        time.sleep(0.5)
        garbolo = net[d_node].cmd('echo "fermioli"') # used to filter out stdout from verbose errors
        time.sleep(0.1)
        garbolo = net[d_node].cmd('echo "fermioli"') # used to filter out stdout from verbose errors
        interm = "failed"
        while ("failed" in interm or "error" in interm):
            interm = net[d_node].cmd(f'ipfs bootstrap add /ip4/192.168.1.1/tcp/4001/p2p/{peerid}')
        info(f'*** bootstrap command result: {interm}')
        net[d_node].cmd(f'echo "/key/swarm/psk/1.0.0/\n/base16/" > ~/.ipfs/swarm.key')
        net[d_node].cmd(f'echo $ENV_SWARM_KEY >> ~/.ipfs/swarm.key')
        info(f'*** PEERID after boot {peerid}')

        ## DISABLE eth0 to enforce private network 
        net[d_node].cmd(f'ip link set eth0 down')
        docks[i-1].start()
        if d_node == 'd1':
           net[d_node].cmd(f'ipfs name publish {cid}')

#CLI(net)
tadedime = datetime.datetime.now().strftime('%Y%b%d-%H:%M')
if t_type == "bandwidth":
    f = open(f'./results/{tadedime}-{t_type}-{count}.csv', "w")
    f.write("node,total_in,total_out,rate_in,rate_out\n")
else:
    f = open(f'./results/{tadedime}-{t_type}-{int(args.size)}.csv', "w")
    f.write("node,type,filesize,filecount,server_delay,delay,bandwidth,sleep,real,user,sys\n")

### Sleep before tests.
time.sleep(naptime)


def run_bandwidth():
    for i in range(1, count+1):
        d_node = f'd{i}'
        result = net[d_node].cmd(f'ipfs stats bw')
        print(result)
        total_in = result.split("\n")[1].split(" ")[1]
        total_out = result.split("\n")[2].split(" ")[1]
        rate_in = result.split("\n")[3].split(" ")[1]
        rate_out = result.split("\n")[4].split(" ")[1]
        #f.write("node,total_in,total_out,rate_in,rate_out\n")
        f.write(f"d{i},{total_in},{total_out},{rate_in},{rate_out}\n")

# perform retrieval
def run_ipfs():

  for i in range(2, count+1):
      d_node = f'd{i}'

      #result = net[d_node].cmd(f'time -p ipfs get {cid} --output=/tmp/ipfs/data.txt; sync')
      result = net[d_node].cmd(f'time -p ipfs get /ipns/{peerid} --output={ipfs_dir_location}; sync')
      #info(f'*** Finished data retrieval via ipfs on node {d_node} \n')


      splitted = result.split('\n')
      length = len(splitted)

      real = splitted[length-4].split(" ")[1].rstrip()
      user = splitted[length-3].split(" ")[1].rstrip()
      sys  = splitted[length-2].split(" ")[1].rstrip()
      f.write(f"d{i},ipfs,{int(args.size)},{file_count},{delay_server},{delay},{bw},{naptime},{real},{user},{sys}\n")
      info(f'zzz.. {naptime}\n')
      time.sleep(naptime)

def run_http():

  for i in range(2, count+1):

      d_node = f'd{i}'

#      result = net[d_node].cmd(f"time -p wget --ca-certificate=/etc/ssl/issuer.crt -q https://192.168.1.1/data.txt -P /tmp/http/data.txt; sync")
#      result = net[d_node].cmd(f'time -p parallel -a <(seq 0 {file_count}) -P 4 --citation wget --ca-certificate=/etc/ssl/issuer.crt -q https://192.168.1.1/{1}.txt -P /tmp/http/{1}.txt; sync')
      smile = "{1}"
      parallelcmd = f'time -p parallel --will-cite -a <(seq 0 {file_count}) -j 4 wget -q --ca-certificate=/etc/ssl/issuer.crt https://192.168.1.1/{smile}.txt -P /tmp/http/{smile}.txt; sync'
      result = net[d_node].cmd(parallelcmd)
      time.sleep(2)
      info(f'*** Finished data retrieval via http on node {d_node} \n')

      splitted = result.split('\n')
      print(splitted)

      length = len(splitted)
      real = splitted[length-4].split(" ")[1].rstrip()
      user = splitted[length-3].split(" ")[1].rstrip()
      sys  = splitted[length-2].split(" ")[1].rstrip()
      f.write(f"d{i},https,{int(args.size)},{file_count},{delay_server},{delay},{bw},{naptime},{real},{user},{sys}\n")


if (t_type == "https"):
    info('*** Starting HTTPS benchmark run')
    run_http()
elif (t_type == "ipfs"):
    info('*** Starting IPFS benchmark run')
    run_ipfs()
elif (t_type == "bandwidth"):
    times = 0
    while True: 
        run_bandwidth()
        times = times + 1
        if times == bandwidth_sample_count:
            break
        time.sleep(60)
else:
    exit("wrong experiment type")


#info('*** Running CLI\n')
#CLI(net)
info('*** Finished tests!')
info('*** Stopping network')

net.stop()
