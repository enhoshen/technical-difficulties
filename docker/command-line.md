# Docker command line 

<!--toc:start-->
- [Docker command line](#docker-command-line)
  - [Interactive with a shell in container](#interactive-with-a-shell-in-container)
<!--toc:end-->

## Interactive with a shell in container
A container with `CMD` or `ENTRYPOINT` will serve as an executable. If trying to run a shell and in detached mode with `docker run -d`, the shell will immediately **returns** and the detached container stops as designed.  
> [docker run reference](https://docs.docker.com/engine/reference/run/#detached--d)  
> the root process (service nginx start) returns and the detached container stops as designed. 
We have to run the shell in forground/attached mode:
```shell
#--rm Automatically remove the container when it exits
docker build -t <docker image> . && docker run -it --rm --entrypoint=bash <docker image>
```
Or the container must first run a background process (in `CMD`/`ENTRYPOINT`), so the container doesn't stop immediately after detach, and then
```shell
docker exec -it <container identifier> bash
```
which is as tedious as can be when you have to first retreive the container identifier.
