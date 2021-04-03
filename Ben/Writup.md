# Bens Writup

## Note

Weirdness when starting docker

```
flask_1  | /home/manager/source.c:1:10: fatal error: stdio.h: No such file or directory
flask_1  |     1 | #include <stdio.h>
flask_1  |       |          ^~~~~~~~~
```

## Initial Recon

```
dang@dang-laptop ~/Github/Teaching/BuildEvent/Writeups/Ben$ docker ps                      ✭Smoos 
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS         PORTS                                                            NAMES
bf7965fe0df0   docker_ftpd              "/init"                  11 seconds ago   Up 5 seconds   0.0.0.0:20-21->20-21/tcp, 0.0.0.0:65500-65515->65500-65515/tcp   docker_ftpd_1
4829678f439b   docker_flask             "./home/intern/runap…"   11 seconds ago   Up 9 seconds   0.0.0.0:5000->5000/tcp                                           docker_flask_1
```


```
$ docker run --rm -v "/home/dang/Wordlists:/wordlists" devalias/gobuster -w /wordlists/common.txt -u http://192.168.1.4:5000 -x html -s 200,403

Gobuster v1.3                OJ Reeves (@TheColonial)
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://192.168.1.4:5000/
[+] Threads      : 10
[+] Wordlist     : /wordlists/common.txt
[+] Status codes : 200,403
[+] Extensions   : .html
=====================================================
/admin (Status: 403)
/console (Status: 200)
/login (Status: 200)
/register (Status: 200)
=====================================================
```


Web page

Create some creds

 - foo@bar.net
 - foo
 - bar
 
Tells me to go to the notes page...

## So with the login

 - Unknown user we get "user does not exist"
 - Known user we get "invalid password"
 - Not sure that SQLi works though


## FTP

Anoynmous login is ok

```
dang@dang-laptop ~/Github/Teaching/BuildEvent/Writeups/Ben$ ftp 172.23.0.3                 ✭Smoos 
Connected to 172.23.0.3.
220 Welcome to an awesome public FTP Server
Name (172.23.0.3:dang): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0           56457 Apr 03 20:50 wordlist.txt
226 Directory send OK.
```

Leaks a bit of info,  about strong paswords / common passowrds etc


```
Staff Annoucement!

We are now diverting all resources to project codename Stellavirus. This has meant our security teams have stopped the upgrade of our website. Please can we ensure we are using strong passwords, I have a list of passwords and I am disappointed to see some of you using passwords common enough to appear on this list! 

Until this project is complete. Myself and the intern managing the website shall have admin access to the website.

Regards,

~ Manager
```

## HTTP Logins

 - admin / administrator  FAIL
 - intern WORKS


## Back to FTP 

https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt

['ftp', 'b1uRR3']
Login Successful

Using those creds didnt seem to give my anything new for FTP, bugger, anything hidden
(Perhaps I should have checked this before... Turns out it also appears with the anon user.

```
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0             474 Apr 03 20:50 announcement.txt
226 Directory send OK.
ftp> 
```



## Brute Force Web

Not in the top 10k.. That sucks.

But we can try that wordlist we found (and fix my code)

```
Attempt my_wifes_birthday
Success
```

## Admin Panel 

So now we get an admin panel that lets us run commands.
Looks like system as standard.

No netcat and wget etc wont be too much use

ls /home/intern

```
Result:__pycache__ create_db.py main.py runapp.sh static templates 
```

ls /home/manager

```
Result:total 12 -rw-r--r-- 1 root root 3151 Apr 3 20:50 research.txt -rw-r--r-- 1 root root 159 Apr 3 20:50 source.c -r-------- 1 root root 36 Apr 3 20:50 user.txt 
```

## The Run app

Cuz we don't just run scripts 

cat /home/intern/runscript.sh

```
Result:#!/bin/bash gcc /home/manager/source.c -o /home/manager/runme chown manager /home/manager/runme sudo -u manager chmod +s /home/manager/runme sudo -u intern python3 /home/intern/create_db.py sudo -u intern python3 /home/intern/main.py
```

```
#!/bin/bash 
gcc /home/manager/source.c -o /home/manager/runme 
chown manager /home/manager/runme 
sudo -u manager chmod +s /home/manager/runme 
sudo -u intern python3 /home/intern/create_db.py 
sudo -u intern python3 /home/intern/main.py
```


Appears that the runme script isnt in manager...
