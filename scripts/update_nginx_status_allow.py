#!/usr/bin/env python


import yaml
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):
    cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
    cluster_data_yaml = open(cluster_config_file, 'r')
    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    cluster_data_yaml.close()
    cluster_serverlist = cluster_data_yaml_parsed.keys()
    mergedlist = []
    for server in cluster_serverlist:
        connect_server_dict = cluster_data_yaml_parsed.get(server)
        ipmap_dict = connect_server_dict.get("ipmap")
        dnsmap_dict = connect_server_dict.get("dnsmap")
        mergedlist = mergedlist + ipmap_dict.keys() + ipmap_dict.values() + dnsmap_dict.keys() + dnsmap_dict.values()
    the_iplist = list(set(mergedlist))
    print(the_iplist)
