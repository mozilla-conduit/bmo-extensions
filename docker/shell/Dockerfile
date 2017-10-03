# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

FROM alpine:3.3

# Build/install dependencies
RUN apk --no-cache add ca-certificates curl bash php-cli php-curl php-json git vim

# add a non-privileged user
RUN addgroup -g 1000 phab && adduser -D -u 1000 -G phab -s /bin/bash phab

WORKDIR /home/phab

# Install Arcanist
RUN mkdir -p phabricator \
    && cd phabricator \
    && git clone https://github.com/phacility/libphutil.git \
    && git clone https://github.com/phacility/arcanist.git

COPY arcrc .arcrc
COPY gitconfig .gitconfig
RUN chmod 600 .arcrc \
    && echo "export PATH=/home/phab/phabricator/arcanist/bin:\$PATH" >> .bash_profile \
    && echo "export EDITOR=vim" >> .bash_profile \
    && chown -R phab:phab /home/phab

USER phab
CMD ["/bin/bash", "-l"]
