## Synopsis
Manage docker plugins.

## Requirements
- [Docker](http://github.com) python module should be installed on target host.
- *ansible_user* should be in *docker* group or use *become: yes*

## Install
The easiest way to install module is to put it in **library/** folder near your playbook.
Like this:
```buildoutcfg
playbook.yml
library/
  |_ docker_plugin.py
```

## Parameters

- **name** (*required*) - Name of plugin without tag or version.
- **tag** - Tag or version of plugin. Default: *latest*.
- **enabled** - Enable or disable plugin. Choices: yes/no. Default: *yes*.
- **state** - State of plugin. Choices: present/absent. Default: *present*.

## Example

```buildoutcfg
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
```
