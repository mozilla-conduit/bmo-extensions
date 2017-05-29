# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# This Source Code Form is "Incompatible With Secondary Licenses", as
# defined by the Mozilla Public License, v. 2.0.

FROM mozillaconduit/docker-bmo
MAINTAINER David Lawrence <dkl@mozilla.com>

# Set ownership to bugzilla:bugzilla to allow git operations
RUN chown -R $BUGZILLA_USER.$BUGZILLA_USER /var/www/html/bmo
