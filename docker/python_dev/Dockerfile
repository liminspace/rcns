FROM python:3.7-stretch

ARG HOST_UID=1000
ARG HOST_GID=1000

ENV PYTHONUNBUFFERED 1
ENV PYTHONUSERBASE /home/user/.pyvenv

ENV APP_DIR=/app

RUN set -eux \
 && apt update \
 && apt install -y --no-install-recommends \
        sudo htop mc nano less apt-utils gettext libargon2-0-dev libffi-dev \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN groupadd --gid "${HOST_GID}" user \
 && useradd --uid "${HOST_UID}" --gid "${HOST_GID}" --create-home --shell /bin/bash user \
 && echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

COPY entrypoint.sh /entrypoint.sh

RUN chmod 755 /entrypoint.sh

RUN chmod 777 /opt

RUN mkdir -p $APP_DIR && chown user. $APP_DIR

USER user

ENV PATH $PYTHONUSERBASE/bin:$PATH

WORKDIR $APP_DIR

ENTRYPOINT ["/entrypoint.sh"]
