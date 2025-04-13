# All about nginx

<!--toc:start-->

- [All about nginx](#all-about-nginx)
  - [Troubleshooting](#troubleshooting) - [Failed (13: Permission denied)](#failed-13-permission-denied) - [Solution](#solution) - [Thrown off by redirect](#thrown-off-by-redirect) - [Solution](#solution)
  <!--toc:end-->

## Troubleshooting

### Failed (13: Permission denied)

For the following config

```conf
location /docs/ {
    alias html/;
    index index.html;
    try_files $uri $uri/ =404;
}
```

with request `/docs/doc1` and `error.log`

```log
2023/05/17 17:28:22 [debug] 26079#26079: *1 try files handler
2023/05/17 17:28:22 [debug] 26079#26079: *1 http script var: "/docs/doc1/"
2023/05/17 17:28:22 [debug] 26079#26079: *1 trying to use file: "doc1/" "./doc1/html/doc1/"
2023/05/17 17:28:22 [crit] 26079#26079: *1 stat() "./doc1/html/doc1/" failed (13: Permission denied), client: ::1, server: _, request: "GET /docs/doc1/ HTTP/1.1", host: "localhost"
```

#### Solution

- Change permission with `chmod`
- Change ownership `sudo chown -R :<nginx user> static_folder`
  - remember to change the ownership/permission of the entire path for instance don't just change ownership of `B/C` under `/A` for path `/A/B/C` where `A/` is still owned by other users.
- Use user that has the proper permission in the `nginx.conf`
  ```conf
  # If in a docker, use root as user is not as insecure
  user root
  ```
  Use `ps aux` to see the user of the `nginx` process
  ```shell
  $ ps aux | grep nginx
  USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
  www-data 26079  0.0  0.0  10840  3596 pts/19   S+   17:28   0:00 nginx: worker process
  ```

### Thrown off by redirect

The following config doesn't work with `/usr/app/doc1/html` exists and with proper permission

```conf
server {
    # default root
    root /var/www/html;
    location ~ ^/docs/(\w+)(.*)$ {
        root /usr/app/;
        index index.html;
        try_files /$1/html$2 /$1/html$2/ =404;
    }
```

with log

```
2023/05/17 17:41:22 [debug] 26900#26900: *1 test location: ~ "^/docs/(\w+)(.*)$"
2023/05/17 17:41:22 [debug] 26900#26900: *1 using configuration "^/docs/(\w+)(.*)$"
...
2023/05/17 17:41:22 [debug] 26900#26900: *1 trying to use file: "/doc1/html/" "/usr/app/doc1/html/"
2023/05/17 17:41:22 [debug] 26900#26900: *1 http script copy: "/"
2023/05/17 17:41:22 [debug] 26900#26900: *1 http script capture: "doc1"
2023/05/17 17:41:22 [debug] 26900#26900: *1 http script copy: "/html"
2023/05/17 17:41:22 [debug] 26900#26900: *1 http script capture: "/"
2023/05/17 17:41:22 [debug] 26900#26900: *1 trying to use dir: "/doc1/html/" "/usr/app/doc1/html/"
2023/05/17 17:41:22 [debug] 26900#26900: *1 try file uri: "/doc1/html/"
...
2023/05/17 17:41:22 [debug] 26900#26900: *1 open index "/usr/app/doc1/html/index.html"
2023/05/17 17:41:22 [debug] 26900#26900: *1 internal redirect: "/doc1/html/index.html?"
2023/05/17 17:41:22 [debug] 26900#26900: *1 rewrite phase: 1
2023/05/17 17:41:22 [debug] 26900#26900: *1 test location: ~ "^/docs/(\w+)(.*)$"
2023/05/17 17:41:22 [debug] 26900#26900: *1 using configuration ""
...
2023/05/17 17:41:22 [debug] 26900#26900: *1 http filename: "/var/www/html/doc1/html/index.html"
2023/05/17 17:41:22 [debug] 26900#26900: *1 add cleanup: 000055E4BC508EF0
2023/05/17 17:41:22 [error] 26900#26900: *1 open() "/var/www/html/doc1/html/index.html" failed (2: No such file or directory), client: ::1, server: _, request: "GET /docs/doc1/ HTTP/1.1", host: "localhost"

```

I just couldn't get my head around that it tried `open index "/usr/app/doc1/html/index.html"` but still failed to serve the file, and retry with default configuration and thus failing to locate the file.  
As a novice web developer I overlooked the message `internal redirect: "/doc1/html/index.html?"`, where it redirected the request to another uri, and then looking for valid location once again and undoubtly the uri `/doc1/html/index.html` doesn't match the location I have in mind and the default root was chosen.

#### Solution

**TODO**
