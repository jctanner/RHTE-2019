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

2. ansible-galaxy init collection [example]

    ```
    mkdir ansible_collections
    cd ansible_collections
    ansible-galaxy collection init rhte.2019
    cd rhte/2019
    git init .
    cat galaxy.yml
    ```

3. shortcut ...

    ```
    rm -rf /tmp/ansible_collections
    mkdir -p /tmp/ansible_collections
    cp -Rp examples/rhte /tmp/ansible_collections/.
    cd /tmp/ansible_collections/rhte/2019

4. the no-op module

    ```
    cat plugins/modules/module_noop.py
    ```

5. a simple role

    ```
    cat roles/lunchtime/tasks/main.yml
    ```


6. ansible-test sanity

    ```
    ansible-test sanity --docker=default --docker-no-pull
    ```

7. ansible-test units 

    ``` 
    cat tests/unit/test_module_noop.py
    ansible-test units --docker=default --python=3.6 --coverage --docker-no-pull
    ```

8. ansible-test integration

    ```
    cat tests/integration/targets/module_noop/tasks/main.yml

    cat tests/integration/targets/role_lunchtime/tasks/main.yml

    ansible-test integration --docker=default --python=3.6 --coverage --docker-no-pull
    ```

9. ansible-galaxy collection build

    ```
    ansible-galaxy collection build
    tar tzvf rhte-2019-1.0.0.tar.gz
    tar -xzvf rhte-2019-1.0.0.tar.gz MANIFEST.json
    cat MANIFEST.json
    ```

10. ansible-galaxy collection publish

11. ansible-galaxy collection install

    ```
    ansible-galaxy collection install rhte-2019-1.0.0.tar.gz
    ```

12. ansible-playbook ...

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

