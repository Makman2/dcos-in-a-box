#!/bin/bash
from getpass import getpass
from ipaddress import IPv4Network
import sys

from networking import scan
from shell import ask_for_permission, bash
from templating import template_file


def main():
    print("DC/OS-IN-A-BOX installer")
    print()
    print("Before you proceed, be sure to read the README file.")
    print("AND BE SURE TO TURN ON ALL NODES!")
    print("")

    print("Proceed with installing?", end='')
    if not ask_for_permission():
        return 255

    print('Scanning for nodes...')
    masters, private_agents, public_agents = find_nodes()

    print('Following nodes were found:')
    print_found_nodes(masters, private_agents, public_agents)

    print('Enter node credentials. These will be reused on all nodes.')
    print('Proceed?')
    if not ask_for_permission():
        return 255

    build_dcos_package(masters)

    install(masters, private_agents, public_agents)

    print('SUCCESS!')
    print('You can examine the ZooKeeper state at '
          'http://{}:8181/exhibitor/v1/ui/index.html !'.format(masters[0]))

    return 0

def find_nodes():
    masters = scan('1.0.10.0/255', verbose=True)
    private_agents = scan('1.0.20.0/255', verbose=True)
    public_agents = scan('1.0.30.0/255', verbose=True)
    return masters, private_agents, public_agents

def print_found_nodes(masters, private_agents, public_agents):
    print('Masters:')
    for master in masters:
        print('- {}'.format(master))

    print('Private agents:')
    for agent in private_agents:
        print('- {}'.format(agent))

    print('Public agents:')
    for agent in public_agents:
        print('- {}'.format(agent))

def build_dcos_package(masters)
    print('Building DC/OS package...')

    template_file('genconf/config.yaml.jinja', 'genconf/config.yaml', masters=masters)

    bash('curl -z -O https://downloads.dcos.io/dcos/EarlyAccess/'
         'commit/14509fe1e7899f439527fb39867194c7a425c771/dcos_generate_config.sh')

    bash('bash dcos_generate_config.sh')

def install(masters, private_agents, public_agents, root_password):
    print('Serving build file to nodes on port 80...')

    container_id = bash(
        'docker run -d -p 80:80 -v $(pwd)/genconf/serve:/usr/share/nginx/html:ro nginx')[0]

    def install_node(role, nodes):
        remote_cmds = ['mkdir /tmp/dcos',
                       'cd /tmp/dcos',
                       'curl -O http://1.0.0.0:80/dcos_install.sh',
                       'sudo bash dcos_install.sh {}'.format(role),
                       'rm /tmp/dcos/dcos_install.sh']

        for node in nodes:
            bash(
                'ssh -o "StrictHostKeyChecking no" root@{} {}'.format(
                    node, shlex.quote(' && '.join(remote_cmds))),
                'root', )

    install_node('master', masters)
    install_node('slave', private_agents)
    install_node('slave_public', public_agents)

    bash('docker stop {}'.format(container_id))

if __name__ == '__main__':
    sys.exit(main())
