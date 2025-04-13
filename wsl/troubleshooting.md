# Troubleshooting for WSL

<!--toc:start-->

- [Troubleshooting for WSL](#troubleshooting-for-wsl)
  - [Setup service on WSL, expose the port](#setup-service-on-wsl-expose-the-port)
  <!--toc:end-->

## Setup service on WSL, expose the port

After setup a html server, or ssh server, we need to port forwarding from the wsl service port to the host exposed port. First route the port:

```powershell
# This output the address of the WSL instance, the first one would
# match the IPv4 Address of the output of ipconfig of the WSL Ethernet
# adapter
wsl -d "Ubuntu" hostname -I
#
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=<expose host port> connectaddress=<wsl ip> connectport=<wsl service port>
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
endfunction
```
