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



