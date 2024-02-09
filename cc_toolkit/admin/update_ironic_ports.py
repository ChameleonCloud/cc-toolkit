#!python3

import openstack
import json
from openstack.exceptions import ConflictException

def main():

    with open("all_ports2.json") as fp:
        portinfodict = json.load(fp)

    node_port_dict = {}

    for key, val in portinfodict.items():
        nodename = str.split(key,".")[0]

        port_dict = {}
        for port in val:
            mac_address = str.lower(port.get("mac_address"))
            port_dict[mac_address] = {
                "name": port.get("name"),
                "switch_id": str.lower(port.get("switch_id")),
                "switch_info": str.lower(port.get("switch_info")),
                "switch_port_id" : str.replace(port.get("switch_port_id"), "ethernet",""),
            }
        node_port_dict[nodename]=port_dict


    conn = openstack.connect(cloud='uc_admin')

    for node_name, ports in node_port_dict.items():
        current_node = conn.baremetal.get_node(node_name)

        for mac_address, values in ports.items():

            new_llc = {
                "switch_id": values["switch_id"],
                "port_id": values["switch_port_id"],
                "switch_info": values["switch_info"],
            }

            new_extra = {"name":  values["name"]}


            current_ports = list(conn.baremetal.ports(details=True,  address=mac_address))
            if len(current_ports) > 1:
                raise Exception("Duplicate MAC Addr!")
            elif len(current_ports) == 1:
                # if the port exists already, just update it
                current_port = current_ports[0]
                current_llc = current_port.get("local_link_connection")
                current_extra = current_port.get("extra")
                is_maintenance = current_node.is_maintenance
                if current_llc!=new_llc or current_extra!=new_extra:
                    print(f"updating info for node {current_node.name} port {current_port.id}")
                    print(current_llc, new_llc,current_extra,new_extra)
                    try:
                        conn.baremetal.update_port(current_port.id, local_link_connection=new_llc, extra=new_extra)
                    except ConflictException as ex:
                        conn.baremetal.set_node_maintenance(current_node.id)
                        conn.baremetal.update_port(current_port.id, local_link_connection=new_llc)
                    finally:
                        if not is_maintenance:
                            conn.baremetal.unset_node_maintenance(current_node.id)
            else:
                # need to make a new port
                new_port = conn.baremetal.create_port(
                    address = mac_address,
                    local_link_connection=new_llc,
                    extras = new_extra,
                    node_uuid = current_node.id
                )
                print(new_port)

if __name__ == "__main__":
    main()
