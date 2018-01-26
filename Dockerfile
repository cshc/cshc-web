FROM ubuntu:latest

# update apt cache
# upgrade preinstalled container packages
# install wget, curl, vim, (un)zip, and less
# clean apt cache
RUN set -xe; \
    DEBIAN_FRONTEND=noninteractive; \
    export DEBIAN_FRONTEND; \
    apt-get update -q; \
    apt-get dist-upgrade -q -y; \
    apt-get install -q -y --no-install-recommends wget curl vim-nox zip unzip less; \
    apt-get clean -q

# we want dumb-init as our entrypoint for all the reasons in their
# docs (see https://github.com/Yelp/dumb-init )
RUN set -xe; \
    wget -O /usr/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64; \
    chmod 0755 /usr/bin/dumb-init

ENTRYPOINT ["/usr/bin/dumb-init"]

# install python3, virtualenv, and pip
# clean apt cache
RUN set -xe; \
    DEBIAN_FRONTEND=noninteractive; \
    export DEBIAN_FRONTEND; \
    apt-get install -q -y --no-install-recommends python3 python3-virtualenv virtualenv python3-pip; \
    apt-get clean -q

# create virtualenv
# install requirements
COPY requirements/ /tmp/requirements/

# install git, needed to retrieve some python packages
# clean apt cache
RUN set -xe; \
    DEBIAN_FRONTEND=noninteractive; \
    export DEBIAN_FRONTEND; \
    apt-get install -q -y --no-install-recommends git; \
    apt-get clean -q

# install build-essential, needed to build some python packages
# clean apt cache
RUN set -xe; \
    DEBIAN_FRONTEND=noninteractive; \
    export DEBIAN_FRONTEND; \
    apt-get install -q -y --no-install-recommends build-essential; \
    apt-get clean -q

# install python3-dev, needed to build some python pacakges
# clean apt cache
RUN set -xe; \
    DEBIAN_FRONTEND=noninteractive; \
    export DEBIAN_FRONTEND; \
    apt-get install -q -y --no-install-recommends python3-dev; \
    apt-get clean -q

# create python virtualenv
RUN set -xe; \
    virtualenv -p /usr/bin/python3 /venv

# install local python requirements
RUN set -xe; \
    /venv/bin/pip install -r /tmp/requirements/local.txt; \
    rm -rf /root/.cache

# install npm and node
RUN set -xe; \
    DEBIAN_FRONTEND=noninteractive; \
    export DEBIAN_FRONTEND; \
    apt-get install -q -y --no-install-recommends npm nodejs; \
    ln -s nodejs /usr/bin/node; \
    apt-get clean -q

# install node packages
COPY package.json /npm_packages/

RUN set -xe; \
    cd /npm_packages; \
    npm install

RUN set -xe; \
    chown -Rf 1000.1000 /npm_packages

# @todo rm -rf /root/.npm

# create build user
RUN set -xe; \
    addgroup --gid 1000 build; \
    adduser --home /project --shell /bin/bash --uid 1000 --ingroup build --disabled-password --gecos Build build

# @todo install cshc-web into docker container (during dev we should be able to host mount over this)


# build with:
#   docker build -t prodenv .
#
# run with:
#   docker run --rm -t -i -u build -v $PWD:/project -w /project prodenv bash
