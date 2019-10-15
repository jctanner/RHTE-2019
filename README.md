# RHTE-2019

# WHOAMI

Good morning/afternoon/evening all ...

For those that have never seen me or heard of me before, that's a sign my master plan is working </dadjoke>

Seriously though, I'm a long term contributor to ansible (top 10 for a long time) and now manage the ansible core engineering team. 

My contributions were typically in places that most people wouldn't see or notice, but were helpful to almost all users. I won't list them out, but if you are curious ...

* https://github.com/jctanner
* https://github.com/ansible/ansible/commits?author=jctanner
* https://github.com/ansible/ansibullbot/commits?author=jctanner

Now on to the demo ...


# DEMO


I'll be referencing a public github repo for everything you'll see going forward: 
    https://github.com/jctanner/RHTE-2019

Beware ... I'm a manager these days, so I reserve my right to be completely wrong about this this stuff and implore you to try it out for yourself if you want to know the whole truth and please file bugs if you find any!

So what are we going to do here? What are we hoping to accomplish? ...

* To see how the sausage will be made in the near future ...
* We're going to create a "collection" and put something interesting into it (a module and a role) ...
* We're going to take on the persona of a customer/user and install the collection and put it to use ...

For those of you in the audience who are allergic to consoles, don't be afraid and bear with me, I'll tie this back to ansible tower's point-n-click nirvana at the end.



1. prep script 

	So we're about to leave kansas and veer into the realm of upstream development processes where nothing gets installed from RPM. I'm using a "virtual environment" to make an isolated set of python packages installed directly with the "pip" command and wedge ansible's git development branch right on top with some fancy syntax ...


    ```
    ./demo_prep.sh
    source venv/bin/activate
    ```

2. If you've ever used the ansible-galaxy CLI to "init" a role, this next step should be very similar ...


	```
	ansible-galaxy --help
	```


	What's this "collection" subcommand all about you ask? Well, we had a choice to make:
    ```
	* productize an experimental project called "mazer" in a short window of time
	* break backwards compat with ansible-galaxy install to support collections
	* merge mazer's functionality into ansible-galaxy as a new subcommand by 2.9.0 GA
    ```
	We chose the latter for numerous reasons and here it is ...


	```
	ansible-galaxy collection --help
	```

	
	The collection subcommand isolates "collection" workflows from "role" workflows. We also added a "role" subcommand that is still presumed to be the default ... for now ...


    ```
    ansible-galaxy collection init rhte.2019
    ```

	Now let's take a look at what this "init" command put on the disk ...


    ```
	tree rhte
    ```

3. 88 miles per hour shortcut ...


    ```
	cd ~/demos/rhte-2019
    rm -rf /tmp/ansible_collections
    mkdir -p /tmp/ansible_collections
    cp -Rp examples/rhte /tmp/ansible_collections/.
    cd /tmp/ansible_collections/rhte/2019
	```


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

