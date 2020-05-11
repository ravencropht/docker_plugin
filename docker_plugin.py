# Copyright: (c) 2020, Konstantin Galushko <galushko.kp@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['release'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: docker_plugin

short_description: Module for managing docker plugins

version_added: "2.4"

description:
    - "Module for managing docker plugins"

options:
    name:
        description:
            - Name without tag of docker plugin.
        required: true
    state:
        description:
            - State of plugin. Can be present or absent. Default present.
        required: false
    tag:
        description:
            - Tag or version of plugin. Default latest.
        required: false
    enabled:
        description:
            - Enable/disable plugin. Can be yes or no. Default yes.
        required: false

author:
    - Konstantin Galushko
'''

EXAMPLES = '''
# Install grafana/loki-docker-driver
- name: Install plugin
  docker_plugin:
    name: "grafana/loki-docker-driver"

# Install and disable weaveworks plugin
- docker_plugin:
    name: "store/weaveworks/net-plugin"
    tag: 2.5.2
    enabled: no
    state: present

# Remove plugins
- docker_plugin:
    name: "{{ item.name }}"
    state: absent
    tag: "{{ item.tag }}"
  loop:
    - { name: store/weaveworks/net-plugin, tag: 2.5.2 }
    - { name: store/elastic/elastic-logging-plugin, tag: 7.6.0 }
'''

import docker
from ansible.module_utils.basic import AnsibleModule


def main():
# Nest arguments
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, default='present', choices=['present', 'absent']),
        tag=dict(type='str', required=False, default='latest'),
        enabled=dict(type='bool', required=False, default=True)
    )
# Attach args to module
    module = AnsibleModule(
                     argument_spec=module_args,
                     supports_check_mode=True
                 )
# Connect to docker
    client = docker.from_env()
    image = module.params['name'] + ':' + module.params['tag']
# Set initial result
    result = 0

# State is present
    if module.params['state'] == 'present':
        try:
            client.plugins.get(image)
        except docker.errors.NotFound:
            client.plugins.install(image)
            result += 1
# Enable/Disable plugin
        if module.params['enabled'] == True and module.params['state'] == 'present':
            if not client.plugins.get(image).enabled:
                client.plugins.get(image).enable()
                result += 1
        elif module.params['enabled'] == False and module.params['state'] == 'present':
            if client.plugins.get(image).enabled:
                client.plugins.get(image).disable()
                result += 1
# State is absent
    elif module.params['state'] == 'absent':
        try:
            plugin = client.plugins.get(image)
        except docker.errors.NotFound:
            pass
        else:
            if client.plugins.get(image).enabled:
                client.plugins.get(image).disable()
            plugin.remove()
            result += 1

    if result > 0:
        module.exit_json(changed=True)
    else:
        module.exit_json(changed=False)


if __name__ == '__main__':
    main()
