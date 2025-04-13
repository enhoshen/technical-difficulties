# Whatever does belong elsewhere about networking goes here

<!--toc:start-->

- [Whatever does belong elsewhere about networking goes here](#whatever-does-belong-elsewhere-about-networking-goes-here)
  - [How does `cheat.sh` detects user being in a terminal or browser?](#how-does-cheatsh-detects-user-being-in-a-terminal-or-browser)
  <!--toc:end-->

## How does `cheat.sh` detect user being in a terminal or browser?

```shell
# output the response from the curl request
# You will see response is formatted for terminal
$ curl cheat.sh/printf -o out.txt

# In out.txt
#[48;5;8m[24m cheat.sheets:printf [24m[0m
#[38;5;246;03m# printf[39;00m
#[38;5;246;03m# Format and print data[39;00m
```

If in a browser, examining the dev tool shows you the response is a html document.
This is done by the checking the field `User-Agent` in http header.
By running curl with verbose option set:

```shell
# run curl with verbose option
curl -v cheat.sh/printf
*   Trying 5.9.243.188:80...
* Connected to cheat.sh (5.9.243.188) port 80 (#0)
> GET /printf HTTP/1.1
> Host: cheat.sh
> User-Agent: curl/7.81.0
> Accept: */*
```

You can see the header of your request, and the `User-Agent` field being "curl/\*".
Although, in mdn web document, it is specifically stated to NOT use `User-Agent` for browser detection in general.

Ref:  
[Browser detection using the user agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Browser_detection_using_the_user_agent)  
[User-Agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent)
