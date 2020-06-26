# System imports
from sys import argv
# import for program layer
from request_lib import *

wb_url = "http://10.1.0.43/zabbix/wbreceiver.php"

bu_free_url = "http://10.1.0.43/zabbix/budiskfreereceiver.php"

if argv[1] == "b":
    # Getting dictionary with hostname and it's hostid from zabbix {hostname: hostid}
    host_hostid_dict = get_hosts_hostid_by_templateids(url, headers, hosts_by_templateids_data)

    # Getting dictionary with hostname and it's last backup status {hostname: last_backup_status}
    hosts_history_dict = get_hosts_history_dict(host_hostid_dict)

    # POST request to WEB server
    get_post_request(wb_url,  hosts_history_dict)

if argv[1] == "f":

    host_hostid_dict = get_hostid_by_name(host_name_and_bu_disks)

    bu_disk_size = get_bu_disk_size(host_hostid_dict)

    bu_disk_used_size = get_bu_disk_used_size(host_hostid_dict)

    bu_disk_free_size = get_bu_disk_free_size(bu_disk_size, bu_disk_used_size)

    # POST request to WEB server
    get_post_request(bu_free_url, bu_disk_free_size)
