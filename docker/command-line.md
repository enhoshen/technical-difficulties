# Docker command line

<!--toc:start-->

- [Docker command line](#docker-command-line)
  - [Interactive with a shell in container](#interactive-with-a-shell-in-container)
  <!--toc:end-->

## Interactive shell in containers

A container with `CMD` or `ENTRYPOINT` will serve as an executable. If trying to run a shell and in detached mode with `docker run -d`, the shell will immediately **returns** and the detached container stops as designed.

> [docker run reference](https://docs.docker.com/engine/reference/run/#detached--d)  
> the root process (service nginx start) returns and the detached container stops as designed.
> We have to run the shell in forground/attached mode:

```shell
#--rm Automatically remove the container when it exits
docker build -t <docker image> . && docker run -it --rm --entrypoint=bash <docker image>
```

Or the container must first run a background process (in `CMD`/`ENTRYPOINT`), so the container doesn't stop immediately after detach, and then

```shell
docker exec -it <container identifier> bash
```

which is as tedious as can be when you have to first retreive the container identifier.

## Undertanding `--add-host=host.docker.internal:host-gateway`

[--add-host=\<host\>:\<ip\>](https://docs.docker.com/engine/reference/commandline/run/#add-host) is a `docker run` option. [connect to service on the host](https://docs.docker.com/desktop/networking/#i-want-to-connect-from-a-container-to-a-service-on-the-host) shows that in the container the special DNS name `host.docker.internal` resolves to the internal IP address used by the host. And what about `host-gateway`? Reading [dockerd command line reference](https://docs.docker.com/engine/reference/commandline/dockerd/) and we can see an argument `--host-gateway-ip`

> IP address that the special 'host-gateway' string in --add-host resolves to. Defaults to the IP address of the default bridge
> It is clear now that `host-gateway` is the IP address of the docker [bridge](https://docs.docker.com/network/bridge/), so now we can connect to the docker host service like this

```shell
# Open a service in the host
python -m http.server 8000
# In a container shell, connects to the service via the host host.docker.internal
curl http://host.docker.internal:8000
```
