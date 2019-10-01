# RHTE-2019

# DEMO

1. prepare the env

    ```
    ./demo_prep.sh
    source venv/bin/activate
    ```

2. ansible-galaxy init collection

    ```
    mkdir ansible_collections
    cd ansible_collections
    ansible-galaxy collection init rhte.2019
    ```

3. create a simple no-op module

    ```
    cp examples/module_noop.py rhte/2019/plugins/modules/.
    ```

4. ansible-test sanity

    ```
    cd ansible_collections/rhte/2019
    ansible-test sanity --docker=default
    ```

5. ansible-test units 

    ``` 
    mkdir -p ansible_collections/rhte/2019/tests/units
    cd ansible_collections/rhte/2019
    ansible-test unit --docker=default
    ```

6. ansible-test integration

    ```
    mkdir -p ansible_collections/rhte/2019/tests/integration/targets/module_noop/tasks
    cp examples/integration_module_noop.yml \
        ansible_collections/rhte/2019/tests/integration/targets/module_noop/tasks/main.yml
    cd ansible_collections/rhte/2019
    ansible-test integration --docker=default
    ```

7. ansible-galaxy collection build
8. ansible-galaxy collection publish
9. ansible-galaxy collection install
10. ansible-playbook ...

