# System imports
import json

# import for program layer
from request_lib import *

# Getting dictionary with hostname and it's hostid from zabbix {hostname: hostid}
host_hostid_dict = get_hosts_hostid_by_templateids(url, headers, hosts_by_templateids_data)

# Getting dictionary with hostname and it's last backup status {hostname: last_backup_status}
hosts_history_dict = get_hosts_history_dict(host_hostid_dict)

# POST request to WEB server
get_post_request(hosts_history_dict)

