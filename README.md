# RHTE-2019

# DEMO

1. ansible-galaxy init collection

    `ansible-galaxy collection init rhte.2019`

2. create a simple no-op module

    `cp examples/module_noop.py rhte/2019/plugins/modules/.`

3. ansible-test sanity

    `cd ansible_collections/rhte/2019`
    `ansible-test sanity --docker=default`

4. ansible-test units 

    `mkdir -p ansible_collections/rhte/2019/tests/units`
    `cd ansible_collections/rhte/2019`
    `ansible-test unit --docker=default`

5. ansible-test integration

    `mkdir -p ansible_collections/rhte/2019/tests/integration/targets/module_noop/tasks`
    `cp examples/integration_module_noop.yml ansible_collections/rhte/2019/tests/integration/targets/module_noop/tasks/main.yml`
    `cd ansible_collections/rhte/2019`
    `ansible-test integration --docker=default`

6. ansible-galaxy collection build
7. ansible-galaxy collection publish
8. ansible-galaxy collection install
9. ansible-playbook ...

