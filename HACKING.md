# Setting up a project development environment

1.  Clone https://github.com/mozilla-conduit/bmo-extensions
2.  Clone https://github.com/mozilla-services/phabricator-extensions

## bmo-extensions Modifications
1.  In `docker-compose.yml`, for the `phabricator` service, comment out `image: mozilla/phabext`.  In its place, add:

```
build:
+      context: /path/to/phabricator-extensions
+      dockerfile: ./Dockerfile
```

This update allows you to use your local phabricator-extensions so that your changes to files appear in the machine.

## phabricator-extensions modifications
1. Create an empty `phabext.json` file; that prevents Dockerfile from breaking
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

## Bringing the machine up
From the `bmo-extensions` directory, do `docker-compose up --build`.  At this point http://phabricator.test and http://bmo.test should work (remember to proxy your IP at `1090`).

## Configuration

1.  Navigate to http://bmo.test/ and log in as `admin@mozilla.bugs` with password `password`.
2.  Navigate to http://bmo.test/editparams.cgi?section=phabbugz and ensure it's turned on
3.  Navigate to http://phabricator.test/config/group/bugzilla/ and make sure your settings match your local setup

## Getting into each machine:
```
# Phabricator
docker exec -it bmoextensions_phabricator_1 /bin/sh

# Bugzilla
docker exec -it bmoextensions_bmo.test_1 su - bugzilla

```

## Using arc
Start by getting into the phabricator container with the command above.  Then:

```
cd ../test_repo/
./../app/arcanist/bin/arc set-config default http://phabricator.test
./../app/arcanist/bin/arc install-certificate

[ HERE YOU NEED TO OPEN YOUR BROWSER TO GET AND PASTE IN THE CONDUIT API KEY]

git config --global user.email "you@example.com"
git config --global user.name "Your Name"

./../app/arcanist/bin/arc diff
```

That will start your commit revision.  Fill in the desired info and yay, you create a diff!

## Caveats
1.  The BMO container isn't pulling fresh code from mozilla-bteam/bmo master.  In fact, it's a bit behind.  I don't know how to update that but what I do know you must `docker-compose down && docker-compose up --build` every time you make a change.  Note that any changes to BMO files must be done *every time you `d-c down && dc-up --b`*.  Reallly annoying.

2.  We just mounting a volume to local phabricator but it's incredibly slow.

3.  ProTip:  In your `bmo-extensions/docker-compose.yml`, add the following to the `phabdb` service:

```
ports:
  - "3306:3306"
```

Being able to look at the Phabricator database tables has been very useful for some tasks.
