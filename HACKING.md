# Setting up a project development environment

## Bringing the machine up
From the `bmo-extensions` directory, do `docker-compose up --build`.  At this point http://phabricator.test and http://bmo.test should work (remember to proxy your IP at `1090`).

## Configuration

1.  Navigate to http://bmo.test/ and log in as `admin@mozilla.bugs` with password `password123456789!`.
2.  Navigate to http://bmo.test/editparams.cgi?section=phabbugz and ensure it's turned on
3.  Navigate to http://phabricator.test/config/group/bugzilla/ and make sure your settings match your local setup

## Getting into each machine:
```
# Phabricator
docker exec -it bmoextensions_phabricator_1 /bin/sh

# Bugzilla
docker exec -it bmoextensions_bmo.test_1 su - bugzilla

```

## Hacking on phabricator-extensions at the same time as bmo-extensions

1.  Clone https://github.com/mozilla-services/phabricator-extensions

## bmo-extensions Modifications

In the `bmo-extensions` project directory:

1. Create a new file in the `bmo-extensions` project directory called `docker-compose.override.yml`.  Add the following contents:

```yaml
version: '2'
services:
  phabricator:
    build:
      context: /YOUR/PATH/TO/phabricator-extensions
      dockerfile: ./Dockerfile
```

## Using arc

To use `arc` with your new account:

1. In the `bmo-extensions` project root run `invoke shell` - a Bash shell will open:
```bash
$ invoke shell
```
2. (optional) Change the account `arc` uses to talk with phabricator (default is the _admin_ account):
```bash
$ arc install-certificate
```

3. Create a test repo with an example commit:
```bash
$ git init test_repo
$ cd test_repo
$ echo "test file" > foo.txt
$ git add foo.txt
$ git commit -m "test commit"
```

4. Send a diff to Phabricator:
```bash
$ arc diff
```

## phabricator-extensions modifications

In the `phabricator-extensions` project directory:

1. Create a `phabext.json` file with the contents `{}`. (It prevents the Dockerfile from breaking.)
2. Create a directory called `test_repo`; in that repo, do `git init` and then create a commit.  This repo will appear in the phabricator container which will allow us to use arc diff.
3. Add the following to `Dockerfile`:

```
# THROW ME AWAY
USER root
COPY test_repo /test_repo
RUN apk add bash
RUN chown -R app:app /test_repo
USER app
```

Those commands move our test repo into the box, as well as give us permissions to read/write that dir.

## Caveats
1.  The BMO container isn't pulling fresh code from mozilla-bteam/bmo master. To update, change to the bugzilla root directory (`/var/www/html/bmo`) and run `git pull`. This will pull the latest changes from the bugzilla repo. modperl is disabled for the 
bugzilla instance so any changes you make to the code should show up immediately. You can create a diff of your changes by doing `git diff > /tmp/some.patch`. And then from the host system, do `docker cp bmoextensions_bmo.test_1:/tmp/some.patch .` to copy the patch out of the running container.

2.  We just mounting a volume to local phabricator but it's incredibly slow.

3.  ProTip:  In your `bmo-extensions/docker-compose.yml`, add the following to the `phabdb` service:

```
ports:
  - "3306:3306"
```

Being able to look at the Phabricator database tables has been very useful for some tasks.
