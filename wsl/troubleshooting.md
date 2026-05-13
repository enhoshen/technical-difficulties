# Troubleshooting for WSL

<!--toc:start-->
- [Troubleshooting for WSL](#troubleshooting-for-wsl)
  - [Setup service on WSL, expose the port](#setup-service-on-wsl-expose-the-port)
  - [/usr/bin/node: 1: Syntax error: ")" unexpected](#usrbinnode-1-syntax-error-unexpected)
    - [Nodejs installation](#nodejs-installation)
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

Remember to change `/etc/ssh/sshd_config` if applicable:

```shl
UsePAM yes
PermitEmptyPasswords yes
PermitRootLogin yes
PubkeyAuthentication yes
```

## /usr/bin/node: 1: Syntax error: ")" unexpected

Annoying as hell bug when using `nodejs`, check wsl version and set it to
wsl WSL 2 using powershell

```ps1
# check wsl version
wsl --version
# check distribution version
wsl --status
wsl -l -v
# change distribution version to WSL 2
# EX: wsl --set-version Ubuntu-24.04 2
wsl --set-version <name> 2
```

### Nodejs installation
- [pre-built download](https://nodejs.org/en/download)
