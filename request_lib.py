import requests
import json

#### VARIABLES ####


host_name_and_bu_disks = {'Aris_sr-ts': 'E:', 'Elemaar-SR-SQL-ELM': 'E:', 'MZKRS-sr-ts-mzkrs': 'F:',
                          'PRIME-sr-ts': 'E:', 'Vielton-SR-TS': 'O:', 'VRPZ-Terminal_Server': 'D:',
                          'Inkast-Moscow-FIleserver': 'G:', 'NEO-Germany-SQL-1C': 'E:',
                          'NEO-MOSCOW-sr-sql-ea': 'E:'}

url = 'http://10.1.0.43/zabbix/api_jsonrpc.php'
headers = {'Content-type': 'application/json',
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}
auth_token = '7dc47a1d63ceeac28db905b8cae1f7aa'

hosts_by_templateids_data = {"jsonrpc": "2.0",
                             "method": "host.get",
                             "params": {
                                 "templateids": ["10272", "10484"]},
                             "id": 1,
                             "auth": auth_token}


def get_hosts_hostid_by_templateids(url, headers, data):
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    response = answer.json()

    len_response = len(response['result'])
    host_hostid_dict = {}

    for i in range(len_response):
        host = response['result'][i]['host']
        hostid = response['result'][i]['hostid']
        host_hostid_dict[host] = hostid

    return host_hostid_dict


def get_hosts_history_dict(host_hostid_dict):
    hosts_history_dict = {}

    for key, value in host_hostid_dict.items():
        last_backup_data = {"jsonrpc": "2.0",
                            "method": "item.get",
                            "params": {
                                "hostids": value},
                            "id": 1,
                            "auth": auth_token}

        answer = requests.post(url, data=json.dumps(last_backup_data), headers=headers)
        response = answer.json()
        len_response = len(response['result'])
        for i in range(len_response):
            if response['result'][i]['name'] == "Backup Status":
                last_backup_status = response['result'][i]['lastvalue']
                hosts_history_dict[key] = last_backup_status

    return hosts_history_dict


def get_hostid_by_name(host_name_and_bu_disks):
    host_hostid_dict = {}
    for host_name in host_name_and_bu_disks:
        hosts_by_name_data = {"jsonrpc": "2.0",
                              "method": "host.get",
                              "params": {
                                  "filter": {"host": host_name}
                              },
                              "id": 1,
                              "auth": auth_token}
        answer = requests.post(url, data=json.dumps(hosts_by_name_data), headers=headers)
        response = answer.json()
        len_response = len(response['result'])

        for i in range(len_response):
            host = response['result'][i]['host']
            hostid = response['result'][i]['hostid']
            host_hostid_dict[host] = hostid
    return host_hostid_dict


def get_bu_disk_size(host_hostid_dict):
    hosts_bu_disk_size = {}

    for key, value in host_hostid_dict.items():
        last_bu_disk_size_data = {"jsonrpc": "2.0",
                                  "method": "item.get",
                                  "params": {
                                      "hostids": value},
                                  "id": 1,
                                  "auth": auth_token}

        answer = requests.post(url, data=json.dumps(last_bu_disk_size_data), headers=headers)
        response = answer.json()
        len_response = len(response['result'])
        bu_disk_item_string = "Total disk space on " + host_name_and_bu_disks[key]
        for i in range(len_response):
            if response['result'][i]['name'] == bu_disk_item_string:
                bu_disk_size = round(int(response['result'][i]['lastvalue']) / 1024 / 1024 / 1024, 2)
                hosts_bu_disk_size[key] = bu_disk_size

    return hosts_bu_disk_size


def get_bu_disk_used_size(host_hostid_dict):
    hosts_bu_disk_used_size = {}

    for key, value in host_hostid_dict.items():
        bu_disk_used_size_data = {"jsonrpc": "2.0",
                                  "method": "item.get",
                                  "params": {
                                      "hostids": value},
                                  "id": 1,
                                  "auth": auth_token}

        answer = requests.post(url, data=json.dumps(bu_disk_used_size_data), headers=headers)
        response = answer.json()
        len_response = len(response['result'])
        bu_disk_item_string = "Used disk space on " + host_name_and_bu_disks[key]
        for i in range(len_response):
            if response['result'][i]['name'] == bu_disk_item_string:
                bu_disk_used_size = round(int(response['result'][i]['lastvalue']) / 1024 / 1024 / 1024, 2)
                hosts_bu_disk_used_size[key] = bu_disk_used_size

    return hosts_bu_disk_used_size


def get_bu_disk_free_size(bu_disk_size, bu_disk_used_size):
    bu_disk_free_size = {}
    for server_name in host_name_and_bu_disks:
        disk_free_size = bu_disk_size[server_name] - bu_disk_used_size[server_name]
        bu_disk_free_size[server_name] = round(disk_free_size, 2)
    return bu_disk_free_size


def get_post_request(request_url, post_request_data):
    print(request_url)
    requests.post(request_url, data=post_request_data)
