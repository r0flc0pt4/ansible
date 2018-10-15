#!/usr/bin/env python

import os
import re
import sys


def main():
    skip = set([
        'test/sanity/code-smell/%s' % os.path.basename(__file__),
        'lib/ansible/module_utils/pycompat24.py',
        'lib/ansible/module_utils/six/__init__.py',
        # the following files should be fixed and removed from this list
        'lib/ansible/modules/network/cloudengine/ce_file_copy.py',
        'lib/ansible/modules/network/panos/panos_dag_tags.py',
        'lib/ansible/modules/network/panos/panos_match_rule.py',
        'lib/ansible/modules/network/panos/panos_op.py',
        'lib/ansible/modules/system/sefcontext.py',
    ])

    basic_allow_once = True

    for path in sys.argv[1:] or sys.stdin.read().splitlines():
        if path in skip:
            continue

        with open(path, 'r') as path_fd:
            for line, text in enumerate(path_fd.readlines()):
                match = re.search(r'(get_exception)', text)

                if match:
                    if path == 'lib/ansible/module_utils/basic.py' and basic_allow_once:
                        # basic.py is allowed to import get_exception for backwards compatibility but should not call it anywhere
                        basic_allow_once = False
                        continue

                    print('%s:%d:%d: do not use `get_exception`' % (
                        path, line + 1, match.start(1) + 1))


if __name__ == '__main__':
    main()
