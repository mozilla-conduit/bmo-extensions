# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from invoke import task


@task
def shell(c):
    """Run a shell with 'arc' installed."""
    c.run('docker-compose'
          ' -f docker-compose.yml'
          ' -f docker-compose.shell.yml'
          ' run shell',
        pty=True
    )

