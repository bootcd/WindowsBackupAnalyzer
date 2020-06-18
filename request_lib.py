import requests
import json

#### VARIABLES ####

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
            if response['result'][i]['name'] == 'Backup Status':
                last_backup_status = response['result'][i]['lastvalue']
                hosts_history_dict[key] = last_backup_status

    return hosts_history_dict

def get_post_request(post_request_data):
    requests.post("http://10.1.0.43/zabbix/wbreceiver.php", data=post_request_data)
