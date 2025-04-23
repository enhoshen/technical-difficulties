# Docker troubleshooting

<!--toc:start-->

- [Docker troubleshooting](#docker-troubleshooting)
  - [Unable to start docker service](#unable-to-start-docker-service)
  <!--toc:end-->

## Unable to start docker service

This a multi-stage problem. First I was trying to start docker systemd

```shell
sudo service start docker
# or systemctl start docker
Job for docker.service failed because the control process exited with error code.
See "systemctl status docker.service" and "journalctl -xe" for details.
```

And with `journalctl -u docker.service --since today` I got:

> Apr 23 10:18:00 <machine> dockerd[448]: unable to configure the Docker daemon with file /etc/docker/daemon.json: the following directives are specified both as a flag and in the configuration file: insecure-registries: (from flag: [<ip 1>], from file: [<ip 2>])

I have `/etc/docker/daemon.json` with the following entry

```
{
    "insecure-registries":["<ip 2>"]
}
```

defined in /etc/docker/daemon.json

Now I ask gemini, it points out that
I'm specifying the `insecure-registries` option in two places:

1.  In the `/etc/docker/daemon.json` file.
2.  As a command-line flag when starting the Docker daemon (dockerd)

Now, I have to know where the flag is set. I don't have a `/etc/systemd/system/docker.service` set up,
but clearly there is such config file existing somewhere...

Turns out, if user defined config file is overide default from `/lib/systemd/system/*` (on ubuntu)
I can also find out by `systemctl status docker.service`

```shell
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2025-04-23 10:38:03 CST; 5min ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 2801 (dockerd)
      Tasks: 17
     Memory: 42.1M
     CGroup: /system.slice/docker.service
             └─2801 /usr/bin/dockerd --insecure-registry <ip 1>
```

Now we've located the problem. Let's just follow the practice and use a
`/etc/systemd/system/docker.service`. I didn't find out why the flag is there,
it is likely set when installing docker...

Both insecure registries are needed, so let's also expand the list in `/etc/docker/daemon.json`

```json
{
  "insecure-registries": ["<ip 2>", "<ip 1>"]
}
```

I wasn't sure if `daemon.json` is correctly loaded, beside checking the service
with command mentioned, use `docker info` to see that both insecure registries
are there.

Take home ideas:

- use these commands when messing with system service:

  ```
  systemctl status docker.service
  journalctl -u docker.service --since today
  ```

- System service configs are under `/etc/systemd/system/`, create own overide
  file by copying from `/lib/systemd/system/`
- docker daemon config goes to `/etc/docker/daemon.json`
- Check docker info with `docker info`
