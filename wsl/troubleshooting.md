# Troubleshooting for WSL

<!--toc:start-->

- [Troubleshooting for WSL](#troubleshooting-for-wsl)
  - [Setup service on WSL, expose the port](#setup-service-on-wsl-expose-the-port)
  <!--toc:end-->

## Setup service on WSL, expose the port

After setup a html server, or ssh server, we need to port forwarding from the wsl service port to the host exposed port. First route the port:

```sh
# on wsl
ip addr | grep eth0
# sample output
# 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
#     inet 172.31.10.56/20 brd 172.31.15.255 scope global eth0
# use the ip after inet for the following steps
```

```powershell
# This output the address of the WSL instance, the first one would
# match the IPv4 Address of the output of ipconfig of the WSL Ethernet
# adapter
# Or use the IP reported by the `ip addr` command in WSL
wsl -d "Ubuntu" hostname -I
#
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=<expose host port> connectaddress=<wsl ip> connectport=<wsl service port>
# example to port forward 22 for ssh
netsh interface portproxy add v4tov4 listenport=22 listenaddress=0.0.0.0 connectport=22 connectaddress=172.31.10.56
```

Then setup windows Firewall inbound rule for the port.

```
-> Windows Defender Firewall with Advanced Security
    -> Inbound Rules (left pane)
    -> Action (right pane)
        -> New Rule
            -> Port
            -> Specific local ports
                -> Fill in the exposed host port
```
