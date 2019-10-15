#!/usr/bin/python

import commoninclude
import cgi
import cgitb
from requests import get
import yaml
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ansible_inventory_file = "/opt/nDeploy/conf/nDeploy-cluster/hosts"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"
master_config_file = installation_path+"/conf/ndeploy_master.yaml"

cgitb.enable()


def check_unique_id(id):
    if os.path.isfile(ansible_inventory_file):
        # parse the inventory and display its contents
        with open(ansible_inventory_file, 'r') as my_inventory:
            inventory = yaml.safe_load(my_inventory)
    for myslave in inventory['all']['children']['ndeployslaves']['hosts'].keys():
        if inventory['all']['children']['ndeployslaves']['hosts'][myslave]['server_id'] == id:
            return False
            break
    return True


form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')


if form.getvalue('action'):
    if form.getvalue('action') == "setup":
        master_ipdata = get('http://ip-api.com/json/'+form.getvalue('master_main_ip')).json()
        slave_ipdata = get('http://ip-api.com/json/'+form.getvalue('slave_main_ip')).json()
        master_lat = master_ipdata.get('lat')
        master_lon = master_ipdata.get('lon')
        slave_lat = slave_ipdata.get('lat')
        slave_lon = slave_ipdata.get('lon')
        inventory = {}
        # master
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['ansible_port'] = form.getvalue('master_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['mainip'] = form.getvalue('master_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['dbip'] = form.getvalue('master_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['dbmode'] = 'readconnroute'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['dns'] = 'geodns'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['latitude'] = master_lat
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['longitude'] = master_lon
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['repo'] = 'ndeploy'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['server_id'] = 1
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['ansible_connection'] = 'local'
        # dbslave
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['ansible_port'] = form.getvalue('slave_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['mainip'] = form.getvalue('slave_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbip'] = form.getvalue('slave_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbmode'] = 'rwsplit'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dns'] = 'geodns'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['latitude'] = slave_lat
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['longitude'] = slave_lon
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['repo'] = 'ndeploy'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['server_id'] = 2
        # slave
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['ansible_port'] = form.getvalue('slave_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['mainip'] = form.getvalue('slave_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbip'] = form.getvalue('slave_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbmode'] = 'rwsplit'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dns'] = 'geodns'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['latitude'] = slave_lat
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['longitude'] = slave_lon
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['repo'] = 'ndeploy'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['server_id'] = 2

        with open(ansible_inventory_file, 'w') as ansible_inventory:
            yaml.dump(inventory, ansible_inventory, default_flow_style=False)
        commoninclude.print_success('Cluster settings saved')
    elif form.getvalue('action') == 'editmaster':
        # If the inventory file exists
        if os.path.isfile(ansible_inventory_file):
            # parse the inventory and display its contents
            with open(ansible_inventory_file, 'r') as my_inventory:
                inventory = yaml.safe_load(my_inventory)
        # master
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['ansible_port'] = form.getvalue('master_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['mainip'] = form.getvalue('master_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['dbip'] = form.getvalue('master_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['dbmode'] = form.getvalue('master_dbmode')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['dns'] = form.getvalue('master_dns')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['latitude'] = form.getvalue('master_lat')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['longitude'] = form.getvalue('master_lon')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['repo'] = form.getvalue('master_repo')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['server_id'] = form.getvalue('master_server_id')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['ansible_connection'] = 'local'
        with open(ansible_inventory_file, 'w') as ansible_inventory:
            yaml.dump(inventory, ansible_inventory, default_flow_style=False)
        commoninclude.print_success('Master settings saved')
    elif form.getvalue('action') == 'editdbslave':
        # If the inventory file exists
        if os.path.isfile(ansible_inventory_file):
            # parse the inventory and display its contents
            with open(ansible_inventory_file, 'r') as my_inventory:
                inventory = yaml.safe_load(my_inventory)
        # slave
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['ansible_port'] = form.getvalue('dbslave_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['mainip'] = form.getvalue('dbslave_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['dbip'] = form.getvalue('dbslave_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['dbmode'] = form.getvalue('dbslave_dbmode')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['dns'] = form.getvalue('dbslave_dns')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['latitude'] = form.getvalue('dbslave_lat')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['longitude'] = form.getvalue('dbslave_lon')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['repo'] = form.getvalue('dbslave_repo')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['server_id'] = form.getvalue('dbslave_server_id')
        # dbslave
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['ansible_port'] = form.getvalue('dbslave_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['mainip'] = form.getvalue('dbslave_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['dbip'] = form.getvalue('dbslave_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['dbmode'] = form.getvalue('dbslave_dbmode')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['dns'] = form.getvalue('dbslave_dns')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['latitude'] = form.getvalue('dbslave_lat')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['longitude'] = form.getvalue('dbslave_lon')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['repo'] = form.getvalue('dbslave_repo')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('dbslave_hostname')]['server_id'] = form.getvalue('dbslave_server_id')
        with open(ansible_inventory_file, 'w') as ansible_inventory:
            yaml.dump(inventory, ansible_inventory, default_flow_style=False)
        commoninclude.print_success('DBSlave settings saved')
    elif form.getvalue('action') == 'addadditionalslave':
        # If the inventory file exists
        if os.path.isfile(ansible_inventory_file):
            # parse the inventory and display its contents
            with open(ansible_inventory_file, 'r') as my_inventory:
                inventory = yaml.safe_load(my_inventory)
        slave_ipdata = get('http://ip-api.com/json/'+form.getvalue('slave_main_ip')).json()
        slave_lat = slave_ipdata.get('lat')
        slave_lon = slave_ipdata.get('lon')
        # calculate slave server id
        num_slaves = len(inventory['all']['children']['ndeployslaves']['hosts'].keys())
        num_slaves = num_slaves + 2  # server id for master is 1 and dbslave is 2
        # check if the server id already exist,if yes we increment its value by 1
        while not check_unique_id(num_slaves):
            num_slaves = num_slaves + 1
        # slave
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['ansible_port'] = form.getvalue('slave_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['mainip'] = form.getvalue('slave_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbip'] = form.getvalue('slave_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbmode'] = 'rwsplit'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dns'] = 'geodns'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['latitude'] = slave_lat
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['longitude'] = slave_lon
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['repo'] = 'ndeploy'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['server_id'] = num_slaves
        with open(ansible_inventory_file, 'w') as ansible_inventory:
            yaml.dump(inventory, ansible_inventory, default_flow_style=False)
        commoninclude.print_success('New Slave added to cluster')
    elif form.getvalue('action') == 'editslave':
        # If the inventory file exists
        if os.path.isfile(ansible_inventory_file):
            # parse the inventory and display its contents
            with open(ansible_inventory_file, 'r') as my_inventory:
                inventory = yaml.safe_load(my_inventory)
        # slave
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['ansible_port'] = form.getvalue('slave_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['mainip'] = form.getvalue('slave_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbip'] = form.getvalue('slave_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbmode'] = form.getvalue('slave_dbmode')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dns'] = form.getvalue('slave_dns')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['latitude'] = form.getvalue('slave_lat')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['longitude'] = form.getvalue('slave_lon')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['repo'] = form.getvalue('slave_repo')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['server_id'] = form.getvalue('slave_server_id')
        with open(ansible_inventory_file, 'w') as ansible_inventory:
            yaml.dump(inventory, ansible_inventory, default_flow_style=False)
        commoninclude.print_success('Slave settings saved')
    elif form.getvalue('action') == 'deleteslave':
        # If the inventory file exists
        if os.path.isfile(ansible_inventory_file):
            # parse the inventory and display its contents
            with open(ansible_inventory_file, 'r') as my_inventory:
                inventory = yaml.safe_load(my_inventory)
        # slave
        del inventory['all']['children']['ndeployslaves']['hosts'][form.getvalue('slave_hostname')]
        with open(ansible_inventory_file, 'w') as ansible_inventory:
            yaml.dump(inventory, ansible_inventory, default_flow_style=False)
        commoninclude.print_success('Deleted slave from cluster')
    elif form.getvalue('action') == 'editip':
        with open(cluster_config_file, 'r') as cluster_data_yaml:
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
        with open(master_config_file, 'r') as master_data_yaml:
            master_data_yaml_parsed = yaml.safe_load(master_data_yaml)
        master_data_yaml_parsed[form.getvalue('master_hostname')]['dnsmap'][form.getvalue('master_lan_ip')] = form.getvalue('master_ip_resource')
        cluster_data_yaml_parsed[form.getvalue('slave_hostname')]['dnsmap'][form.getvalue('master_lan_ip')] = form.getvalue('slave_wan_ip')
        cluster_data_yaml_parsed[form.getvalue('slave_hostname')]['ipmap'][form.getvalue('master_lan_ip')] = form.getvalue('slave_lan_ip')
        with open(cluster_config_file, 'w') as cluster_data_yaml:
            yaml.dump(cluster_data_yaml_parsed, cluster_data_yaml, default_flow_style=False)
        with open(master_config_file, 'w') as master_data_yaml:
            yaml.dump(master_data_yaml_parsed, master_data_yaml, default_flow_style=False)
        commoninclude.print_success('IP mapping updated')
    elif form.getvalue('action') == 'delip':
        with open(cluster_config_file, 'r') as cluster_data_yaml:
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
        with open(master_config_file, 'r') as master_data_yaml:
            master_data_yaml_parsed = yaml.safe_load(master_data_yaml)
        del master_data_yaml_parsed[form.getvalue('master_hostname')]['dnsmap'][form.getvalue('master_lan_ip')]
        for theslave in cluster_data_yaml_parsed.keys():
            del cluster_data_yaml_parsed[theslave]['dnsmap'][form.getvalue('master_lan_ip')]
            del cluster_data_yaml_parsed[theslave]['ipmap'][form.getvalue('master_lan_ip')]
        with open(cluster_config_file, 'w') as cluster_data_yaml:
            yaml.dump(cluster_data_yaml_parsed, cluster_data_yaml, default_flow_style=False)
        with open(master_config_file, 'w') as master_data_yaml:
            yaml.dump(master_data_yaml_parsed, master_data_yaml, default_flow_style=False)
        commoninclude.print_success('IP resource deleted')
    elif form.getvalue('action') == 'addip':
        with open(cluster_config_file, 'r') as cluster_data_yaml:
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
        with open(master_config_file, 'r') as master_data_yaml:
            master_data_yaml_parsed = yaml.safe_load(master_data_yaml)
        master_data_yaml_parsed[form.getvalue('master_hostname')]['dnsmap'][form.getvalue('master_lan_ip')] = form.getvalue('master_ip_resource')
        for theslave in cluster_data_yaml_parsed.keys():
            cluster_data_yaml_parsed[theslave]['dnsmap'][form.getvalue('master_lan_ip')] = form.getvalue(theslave+"_wan_ip")
            cluster_data_yaml_parsed[theslave]['ipmap'][form.getvalue('master_lan_ip')] = form.getvalue(theslave+"_lan_ip")
        with open(cluster_config_file, 'w') as cluster_data_yaml:
            yaml.dump(cluster_data_yaml_parsed, cluster_data_yaml, default_flow_style=False)
        with open(master_config_file, 'w') as master_data_yaml:
            yaml.dump(master_data_yaml_parsed, master_data_yaml, default_flow_style=False)
        commoninclude.print_success('IP mapping added')
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')