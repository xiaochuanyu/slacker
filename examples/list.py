#!/usr/bin/env python
"""List items in slack."""

# https://github.com/os/slacker
# https://api.slack.com/methods

import os
import functools
from slacker import Slacker


def paginated(list_func):
    # See https://api.slack.com/docs/pagination
    next_cursor = None
    while True:
        response = list_func(cursor=next_cursor)
        yield response
        next_cursor = response.body['response_metadata']['next_cursor']
        if not next_cursor:
            break


def list_slack():
    """List channels & users in slack."""
    try:
        token = os.environ['SLACK_TOKEN']
        slack = Slacker(token)

        # Get users list, with pagination
        for response in paginated(functools.partial(slack.users.list, limit=150)):
            print("=== page === ")
            users = response.body['members']
            for user in users:
                if not user['deleted']:
                    print(user['id'], user['name'], user['is_admin'], user[
                        'is_owner'])
        print()
    except KeyError as ex:
        print('Environment variable %s not set.' % str(ex))


if __name__ == '__main__':
    list_slack()
