#!python3

import openstack
from datetime import datetime
from blazarclient.client import Client as blazar_client

time_now = datetime.utcnow()

conn = openstack.connect()
session = conn.session
blazar = blazar_client(session=session)

# We make two (expensive) API calls
blazar_hosts_list = blazar.host.list()
blazar_allocations_list = blazar.host.list_allocations()


# get sets for later math
blazar_host_id_set = set(h.get('id') for h in blazar_hosts_list)
blazar_nonreservable_set = set(h.get('id') for h in blazar_hosts_list if h.get("reservable")==False)

# for each "current" reservation, add the resource_id of the relevant host
blazar_reserved_host_ids = set()
for alloc in blazar_allocations_list:
    resource_id = alloc.get("resource_id")
    for res in alloc.get("reservations"):
        start_datetime = datetime.fromisoformat(res.get("start_date"))
        end_datetime = datetime.fromisoformat(res.get("end_date"))
        if (time_now >= start_datetime) and (time_now < end_datetime):
            blazar_reserved_host_ids.add(resource_id)

# final list of hosts that can be reserved is all hosts - non-reservable hosts - reserved hosts
# note that there may be reservations for hosts that are currently non-reservable, since they could have been made earlier

reservable_host_ids = blazar_host_id_set - blazar_nonreservable_set - blazar_reserved_host_ids


# create list of hosts indexed by resource ID so we can get names and node_types
blazar_hosts_by_resource_id = {h.get("id"): h for h in blazar_hosts_list}

for resource_id in reservable_host_ids:
    blazar_host = blazar_hosts_by_resource_id[resource_id]
    print(blazar_host.get("node_name"), blazar_host.get("node_type"))
