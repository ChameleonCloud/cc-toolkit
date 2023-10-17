#!/usr/bin/env bash

# create virtualenv
python3 -m venv .venv

# install using upper-constraints
# -c https://opendev.org/openstack/requirements/raw/branch/stable/xena/upper-constraints.txt \
.venv/bin/pip install \
    -r requirements.txt
