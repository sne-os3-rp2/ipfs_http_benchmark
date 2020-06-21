### TODO
- Add a check after the data transfer to check that data indeed was downloaded to requesting nodes and is of the expected size
- the `.cmd` method _seems_ to behave in unpredicatable manner sometimes regarding the output. Try and identify the method to its maddness.

### IPFS/HTTP Benchmark

#### Overview

Tool for performing data transfer benchmark of IPFS and HTTP within Mininet (via containernet) environment.

To use this tool containernet needs to be installed. Follow the installation instructions of containernet [here](https://containernet.github.io/#installation)

Once installed, copy `ipfs_http_benchmark.py` into the required directory within containernet where it can be run.

Before running the benchmark build the docker image that is used in the benchmark by cd'ing into `ubuntu-ipfs-docker` and run:

```
sudo docker build -t ubuntu-ipfs .
```

Ensure the image is tagged as `ubuntu-ipfs` as this is what is used within containernet

An example of how to run the bechmark is to run the following command:

```
sudo python3 ipfs_example.py -c 10 -s 500M -d 100ms -b 100
```

This would create the result of the benchmark in the `output.csv` file. The csv file will look like this:

```
daderemi@amiens:~/containernet/examples$ cat output.csv
'node','type','filesize','real','user','sys'
d2,'ipfs','500M','1.77','0.43','1.21'
d3,'ipfs','500M','1.81','0.39','1.28'
d4,'ipfs','500M','1.88','0.39','1.34'
d5,'ipfs','500M','1.89','0.44','1.32'
d6,'ipfs','500M','2.01','0.44','1.35'
d7,'ipfs','500M','1.94','0.45','1.23'
d8,'ipfs','500M','1.91','0.42','1.33'
d9,'ipfs','500M','1.91','0.41','1.33'
d10,'ipfs','500M','5.67','0.29','1.05'
d2,'http','500M','4.75','0.11','0.79'
d3,'http','500M','7.01','0.09','0.82'
d4,'http','500M','11.46','0.31','1.51'
d5,'http','500M','11.80','0.47','1.98'
d6,'http','500M','10.78','0.17','1.39'
d7,'http','500M','10.66','0.16','0.53'
d8,'http','500M','10.58','0.10','0.60'
d9,'http','500M','10.56','0.08','0.99'
d10,'http','500M','10.58','0.22','1.36'
```

#### Options

The following options can be passed when running the benchmark:

```
parser.add_argument("-c", "--count", help="Number of nodes", default=1)
parser.add_argument("-s", "--size", help="filesize", default="10M")
parser.add_argument("-d", "--delay", help="delay between node hosting data and switch", default="500ms")
parser.add_argument("-b", "--bandwidth", help="bandwidth between node hosting data and switch", default=1)
```
