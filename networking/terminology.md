# Terminologies of networking/telecommunications

## Gateway

Hardware or software to allow data flow from one _network to another_. Straight into examples:

- A host with address `192.168.4.3`
- The router's inside address `192.168.4.1`
- subnet mask `255.255.255.0`/`/24`

The address range assignable to hosts is from 192.168.4.1 to 192.168.4.254. TCP/IP defines the addresses 192.168.4.0 (network ID address) and 192.168.4.255 (broadcast IP address). A packet outside of the subnet range is sent to the default gateway that is `192.168.4.1` (happens to be the router, is it always the case?). The routes will go on to the router's default gateway (if any) if it has no route for the packet.

> references

    [wiki: gateway](https://en.wikipedia.org/wiki/Gateway_(telecommunications))
    [wiki: default gatway](https://en.wikipedia.org/wiki/Default_gateway)

## Bridge

**TODO**
