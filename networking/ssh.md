# About SSH

## Public-key authentication

User can generate a key pair and upload the public key to a ssh host. If I'm not mistaken, public key is used by the remote host to generate a challenge text for the user to decrypt using the private key, proving that the user has the private key.
Generate and upload the key:

```shell
# follow the prompts
ssh-keygen
# copy public key to the host, <key identifier path> defautls to ./ssh/id_*
ssh-copy-id -i <key identifier path> <user>@<host> -p <port>
# look for section AUTHENTICATION in ssh manual
man ssh
```

## Manage host in `.ssh/config`

Let's get head into an example:

```config
Host <host alias>
    HostName <host ip>
    Port <host port>
    User <user name>
```

Related document is in `ssh_config` manual

```shell
man ssh_config
```
