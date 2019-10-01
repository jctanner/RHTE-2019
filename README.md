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
    cd rhte/2019
    git init .
    ```

3. create a simple no-op module

    ```
    mkdir plugins/modules
    cp ../../../examples/module_noop.py plugins/modules/.
    ```

4. ansible-test sanity

    ```
    ansible-test sanity --docker=default
    ```

5. ansible-test units 

    ``` 
    mkdir -p tests/unit
    cp ../../../examples/unit_module_noop.py tests/unit/test_module_noop.py
    ansible-test units --docker=default --python=3.6
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

    ```
    ansible-galaxy collection build
    tar tzvf rhte-2019-1.0.0.tar.gz
    tar -xzvf rhte-2019-1.0.0.tar.gz MANIFEST.json
    cat MANIFEST.json
    ```

8. ansible-galaxy collection publish
9. ansible-galaxy collection install
10. ansible-playbook ...

