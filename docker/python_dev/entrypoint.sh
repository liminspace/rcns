#!/bin/bash

if [ -f "deploy/requirements.txt" ] && [ ! -e "$PYTHONUSERBASE/.nonempty" ] && [ "$DISABLE_PIP_AUTOINSTALL" != "yes" ]; then
    bash deploy/install_requirements_dev.sh
    touch "$PYTHONUSERBASE/.nonempty"
fi

exec "$@"
