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

    Not much to it really. It shouldn't be rocket science because that's the opposite of what we want ansible to be.


3. 88 miles per hour shortcut ...


    ```
	cd ~/demos/rhte-2019
    rm -rf /tmp/ansible_collections
    mkdir -p /tmp/ansible_collections
    cp -Rp examples/rhte /tmp/ansible_collections/.
    cd /tmp/ansible_collections/rhte/2019
	```


4. the no-op module


    To save you all from a lesson in python and module development, I've created a "null module". It's sole job is to look and behave like a module, but not to actually do anything.

    ```
    cat plugins/modules/module_noop.py
    ```

    If you really want to learn module dev, I have another link for you to peruse ...


    https://tannerjc.net/wiki/index.php?title=Ansible_Developer_Filament


5. a simple role


    In the immortal words of Andrius ... "this is how we role".

    ```
    cat roles/lunchtime/tasks/main.yml
    ```

    Collections can also contain roles (we've said this right?); a caveat ... you can not put plugins in those roles. Plugins must live in the top level plugins folder of the collection, otherwise it's still a boring ol' role.


6. ansible-test sanity


    Okay, now we're going to do something that in the past would have only been seen by folks who contribute to ansible/ansible.

    Sanity is a collection of static code linters and code analyzers that the core team and the community have built up over the years to assert that modules avoid certain gotchas and adhere to the coding styles that we need* to enforce (because of previous bugs and py2/3 compat). 

    These tests are available in 2.9.0 through a special command named "ansible-test". This command is quite powerful and has more bells and whistles than even I know about, but you can see a recording of Matt Clay's (the author's) ansiblefest presentation on the ansible website for a deeper dive.

    ```
    ansible-test --help
    ansible-test sanity --docker=default --python=3.6 --docker-no-pull
    ```

    We're hoping this becomes part of the import process within galaxy very soon.


7. ansible-test units 


    This again is something that typically is only seen by ansible contributors, but is a very important part of ensuring that the plugins are functional. It's the fastest way to verify oddball edgecases in a module in a short amount of time at the lowest cost possible.

    ``` 
    cat tests/unit/test_module_noop.py
    ansible-test units --docker=default --python=3.6 --coverage --docker-no-pull
    ```


8. ansible-test integration


	The last set of tests are integration. This will actually flex the module and role to make sure they really do what they're advertised to do. We get to use playbooks here and we refer to the set of playbooks in each integration test as a "target". We'll probably see these types of tests most often in collections because they are they lowest barrier to entry for tests which are not reliant on third party resources.

	"third party resources" ... PC LOAD LETTER!? ... I mean expensive/proprietary/slow/irritating infrastructure like public clouds, on-prem  virt-*cough* "clouds", black boxes, blue boxes (not really, but that would be neat!).


    ```
    cat tests/integration/targets/module_noop/tasks/main.yml

    cat tests/integration/targets/role_lunchtime/tasks/main.yml

    ansible-test integration --docker=default --python=3.6 --coverage --docker-no-pull
    ```

9. ansible-galaxy collection build

	Now we venture into a new concept for collections... BUILD. Roles on galaxy are currently indexes to a github repo. The install process fetches the source tarball from github rather than galaxy. In the collection world, galaxy now hosts the release tarballs as an "artifact" and no longer has a mandatory link to a github repo. To make the tarballs, we run ansible-galaxy collection build from inside the collection. 


    ```
    ansible-galaxy collection build
    ```

	Notice the tarball it leaves behind ... let's inspect it's content ...

	```
    tar tzvf rhte-2019-1.0.0.tar.gz
    tar -xzvf rhte-2019-1.0.0.tar.gz MANIFEST.json
    cat MANIFEST.json
    ```

10. ansible-galaxy collection publish

	To get the tarball on galaxy for everyone else to use, we need to run the "publish" subcommand. There's nothing special about this really, it's just an HTTP POST that uploads the tarball and waits for the server to process the content and do some minimal static analysis with ansible-lint. Let's not actually run it and move on ...


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

