Docker Development Environment for BMO and Phabricator Integration
==================================================================

## How to install Docker

Visit [Docker](https://docker.com) and get Docker up and running on your system.

## How to build BMO Docker image

To build a fresh image, just change to the directory containing the checked out
files and run the below command:

```bash
$ docker-compose build
```
## How to start BMO Docker image

To start a new container (or rerun your last container) you simply do:

```bash
$ docker-compose up
```

This will stay in the foreground and you will see the log output in your console. You
can optionally use the `-d` option to run the containers in the background instead.

To stop, start and remove the containers that were created from the last run, you can do:

```bash
$ docker-compose stop
$ docker-compose start
$ docker-compose rm
```

## Configure Firefox Proxy

Go to the options section of your browser. You will need to update the proxy settings of
your browser to point to port 1090 of the IP address of your docker host. In Firefox,
this is under 'Privacy and Security'. Then click on 'Connection Settings'. Choose
'Manual proxy configuration'. For 'HTTP Proxy' enter the IP address of the docker host.
For Linux this would normally be localhost and for other systems it would be the IP of
the VM running docker. And then enter 1090 in the 'Port' field to the right. Click 'OK'.

## How to access the BMO container

After you configure you proxy settings as outlined above, you can simply point your
browser to `http://bmo.test` to see the the BMO home page. The bmo.test domain is recognized
on the internal Docker network so no need to find out the IP address of the container.

The Administrator login is `admin@mozilla.bugs` and the password is `password123456789!`.
You can use the Administrator account to creat other users, add products or
components, etc.

## How to access the Phabricator container.

To access the Phabricator site, point your browser to 'http://phabricator.test'.

The administrator login is `admin` and the password is `admin`. You can use this
account to create other accounts, projects, etc.

## BMO Development

You can access code in the container using `docker exec -it bmoextensions_bmo.test_1 su - bugzilla`
command. The 'bmoextensions_bmo.test_1' name may vary depending on how you checked out
the GitHub repo code and what the name of the checkout directory is.

Once you have logged in to a shell, change to the '/var/www/html/bmo' directory. This is
the BMO code root. The Phabricator extension code lives in 'extensions/PhabBugz'. mod_perl
is disabled for the webroot so any changes you make should show up immediately on the site.
Git is installed so you should be able to use git to create branches, update, and generate
diffs as normal. You can use 'docker cp' to copy patches to your local host filesystem
as needed. An example workflow may look like:

```bash
$ cd /var/www/html/bmo
$ git status
$ git checkout -b my-feature
$ vi extensions/PhabBugz/Extension.pm (make some changes and save)
$ git add extensions/PhabBugz/Extension.pm
$ git diff --staged > /tmp/my-feature.patch
$ exit
$ d cp bmoextensions_bmo.test_1:/tmp/my-feature.patch ~/my-feature.patch
```

Then you can upload the patch as needed for review. Or you can create a pull request
directly from inside the container.

## Starting the Push Daemon
If your development requires the use of a push connector, you'll need to
manually start the push daemon.

Start by opening a new terminal and accessing the container:

```bash
docker exec -it bmoextensions_bmo.test_1 su - bugzilla
```

Navigate to the bmo directory:

```bash
cd /var/www/html/bmo
```

Start the push daemon:

```bash
perl extensions/Push/bin/bugzilla-pushd.pl -f -d start
```

Push messages will display in the terminal as they are executed.
