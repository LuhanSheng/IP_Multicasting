# Semi-Reliable IP Multicast

![Mininet](https://img.shields.io/badge/Mininet-2.3.0-blue)
![ovs](https://img.shields.io/badge/ovs-2.13.1-yellowgreen)
![Platform](https://img.shields.io/badge/platform-Linux-lightgray.svg)
![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04.1-orange)

This repository is a demo of SRIMP: A Semi-reliable IP multicast protocol.  
Implementation of this demo is in the folder named semi-reliable-multicast.  


## <a name="versions"></a> Versions

The most up-to-date version provided here is 5.1.2.


## Install
Please install Mininet(v2.3.0) and ovs(2.13.1) on the machine.  
This demo requires python version >= 3.6 and is based on Ubuntu(v20.04.1).  

## About this demo
Implementation of the sender of SRIMP is in folder semi-reliable-multicast/multicast_send  
Implementation of the receiver of SRIMP is in folder semi-reliable-multicast/multicast_receive  

## Run this demo
1. Download or clone this repository to your machine.  
2. Construct the multicast network topology. 
```
cd semi-reliable-multicast  
sudo python3 simple-multicast-topo.py  
xterm H0 H1 H2 H3 H4  
```
3. 5 terminals should be opened after doing step 2, with H0 as the sender and H1, H2, H3, H4 as the receivers.  

In each terminal of the receivers:  
```
cd multicast_receive  
python3 receive_process.py  
```
In the terminal of the sender:  
```
cd multicast_send  
python3 send_process.py  
```
4. Note: 
To send file, please add file you want to send in the folder named multicast_send and change the line 25 in send_process.py of
```
self.file_buffer = [[i, bytes(10000)] for i in range(self.block_num)]
```
to
```
self.file_buffer = buffer(filename)
```
## Author

Implemented by Luhan Sheng.

Maintained by Luhan Sheng.

## Contact

wc36170565@gmail.com

