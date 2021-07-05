# Template for building PHP based CTF

Various docker file and docker-compose to bring everything together
Lets us the classic LAMP stack:

  - Apache / PHP
  - MySQL 

## Notes

We have two ways of working with this.

  - Development mode:  Lets is work with a "Live" version of the site
  - Deploy Mode: "Bakes" the site into a single image.
  

I tend to work with the development version, as it lets me bugger 
around and get everything setup.

When its time to deploy, I then build a deploy version, with the
content "baked" into the image.  This means that we have our final cut
of the machine can be recreated at any time.

## Compose Files

We can start things up with the docker-compose files.  This will build
a "stack" of docker images, with PHP and mySQL.  Items in the stack
are segregated from the base OS, bt can talk to each other, like they
are on the same machine.

 - **devel-compose.yaml** Development version, use this for testing.
 
 - **deploy-compose.yaml** The Deploy version of the site.  I would
   rename this to docker-compose when you are ready to go


## Working with It.

For development start the version

```
docker-compose -f devel-compose up
```

For deploy you need to 

```
docker-compose -f deploy-compose build
docker-compose -f deploy-compose up
```

### Convenience 

When it comes to deploy time (or for convenience) 
you might want to link the version you are working with to be called docker-compose
This lets you start and stop the service without specifing the compose file

For example you can do this to work with the development version by defaul

```
ln -s devel-compose.yaml docker-compose.yaml
 
#Then start with 
docker-compose up
```
 

# Dvelopment

The PHP stuff live in ```PHP/content```  use this as the equivilent of the ```/var/www/html```

  - I have stuck an index.php file in there, 
  - conn.php is giving an example of connecting to the database
