# Intro

This repo provides a quick method to install the openstack client tools and SDK, with versions compatible with what Chameleon is running.

## Installation

Simply execute `./install.sh`. This will create a python virtualenv in the current directory, and install the client tools into the local directory.

## Auth and Connections

For best results, use an Openstack `clouds.yaml` file to configure your connections to each openstack site that you wish to interact with.

For system-wide use, this can be placed in `~/.config/openstack/clouds.yaml`, or you can place it in this directory instead.

## Usage

Select an entry from your `clouds.yaml` file by setting the envionment variable `OS_CLOUD`. For example, if your `clouds.yaml` contained the following entries:

```
clouds:
  chi_uc:
    ...
  chi_tacc:
    ...
```

You would run commands as follows:
```
source .venv/bin/activate
OS_CLOUD=chi_uc openstack token issue
```

## Handling client version conflicts

While openstack services recommend using an "upper-constraints.txt" file to limit what depenency versions are in use, this presents issues for
installation of develeopment-mode packages from git, as they don't obey the constraints file.

Instead of limiting the package versions, in the case where we need an older client to talk to an openstack service, we can limit the api microversion in use.
See https://docs.openstack.org/openstacksdk/latest/user/microversions.html


## References

OpenStack Docs

- https://governance.openstack.org/tc/reference/runtimes/xena.html
- https://docs.openstack.org/openstacksdk/latest/user/guides/intro.html



Other attempts at operator tools

- https://github.com/ChameleonCloud/climeleon
- https://github.com/ChameleonCloud/ciab-operator-tools
- https://github.com/ChameleonCloud/python-chi-operator
