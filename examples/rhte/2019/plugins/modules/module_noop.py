#!/usr/bin/python

# (c) 2019, James Tanner <jtanner@localhost>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: module_noop
author:
    - James Tanner (@jctanner)
version_added: "1.0"
short_description: Does nothing useful but is great for demos!
description:
    - Use this in production if you having nothing better to do.
'''

EXAMPLES = '''
'''

RETURN = '''
'''


from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule({})
    module.exit_json(changed=False, msg="I did nothing useful", foo="bar")


if __name__ == "__main__":
    main()
