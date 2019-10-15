# RHTE-2019

# WHOAMI

https://github.com/jctanner
https://github.com/ansible/ansible/commits?author=jctanner
https://github.com/ansible/ansibullbot/commits?author=jctanner


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
    cat galaxy.yml
    ```

3. create a simple no-op module

    ```
    mkdir plugins/modules
    cp ../../../examples/module_noop.py plugins/modules/.
    ```

4. create a simple role

    ```
    mkdir -p roles/lunchtime/tasks
    cp ../../../examples/examples/role_lunchtime.yml roles/lunchtime/tasks/main.yml
    ```


5. ansible-test sanity

    ```
    ansible-test sanity --docker=default
    ```

6. ansible-test units 

    ``` 
    mkdir -p tests/unit
    cp ../../../examples/unit_module_noop.py tests/unit/test_module_noop.py
    ansible-test units --docker=default --python=3.6 --coverage
    ```

7. ansible-test integration

    ```
    mkdir -p tests/integration/targets/module_noop/tasks
    cp ../../../examples/integration_module_noop.yml \
        tests/integration/targets/module_noop/tasks/main.yml

    mkdir -p tests/integration/targets/role_lunchtime/tasks
    cp ../../../examples/integration_role_lunchtime.yml \
        tests/integration/targets/role_lunchtime/tasks/.

    ansible-test integration --docker=default --python=3.6 --coverage
    ```

8. ansible-galaxy collection build

    ```
    ansible-galaxy collection build
    tar tzvf rhte-2019-1.0.0.tar.gz
    tar -xzvf rhte-2019-1.0.0.tar.gz MANIFEST.json
    cat MANIFEST.json
    ```

9. ansible-galaxy collection publish

10. ansible-galaxy collection install

    ```
    ansible-galaxy collection install rhte-2019-1.0.0.tar.gz
    ```

11. ansible-playbook ...

    # unqualified names
    ```
    cd /tmp

    echo "- hosts: localhost" > testplay.yml
    echo "  gather_facts: False" >> testplay.yml
    echo "  tasks:" >> testplay.yml
    echo "    - module_noop:" >> testplay.yml

    ansible-playbook -vvvv testplay.yml
    ```

    # FQN usage
    ```
    cd /tmp

    echo "- hosts: localhost" > testplay.yml
    echo "  gather_facts: False" >> testplay.yml
    echo "  tasks:" >> testplay.yml
    echo "    - rhte.2019.module_noop:" >> testplay.yml

    ansible-playbook -vvvv testplay.yml
    ```

    # collections keyword + unqualified names
    ```
    cd /tmp

    echo "- hosts: localhost" > testplay.yml
    echo "  gather_facts: False" >> testplay.yml
    echo "  collections:" >> testplay.yml
    echo "    - rhte.2019" >> testplay.yml
    echo "  tasks:" >> testplay.yml
    echo "    - module_noop:" >> testplay.yml

    ansible-playbook -vvvv testplay.yml
    ```

