#!python

import argparse
import json
import sys
from datetime import datetime, timedelta
from vk_api import vk_api

vk_session = None
vk: vk_api.VkApi = None
params: dict = {}
parsed_args = {}
work: bool = False


def send_message(peer_id, msg):
    global vk
    vk.messages.send(peer_id=peer_id, message=msg)


def check_group_wall(group_id, count: int = 5):
    global vk
    result = vk.wall.get(owner_id=group_id, count=count, filter='owner')
    return result


def send_comment(group_id, post_id, msg: str = '+'):
    global vk
    result = vk.wall.createComment(owner_id=group_id, post_id=post_id, message=msg)
    if 'comment_id' in result:
        return result['comment_id']

    print(result['error_code'], result['error_msg'], result['error_text'], file=sys.stderr)
    return -1


def main(group_id, message):
    work = True
    last_check = datetime.now()
    response = check_group_wall(group_id)
    res_count = response['count']
    records = response.get('items', [])
    last_post_id = records[0].get('id', -1) if res_count > 0 else -1
    post_id = -2
    timeout = params.get('timeout', 50)
    while work:
        d = datetime.now() - last_check
        if datetime.now() - last_check > timedelta(milliseconds=5):
            print(d)

            response = check_group_wall(group_id)
            res_count = response['count']
            records = response.get('items', [])
            post_id = records[0].get('id', -1) if res_count > 0 else -1
            if post_id != last_post_id:
                res = send_comment(group_id, post_id, message)
                if res > 0:
                    last_post_id = post_id
                else:
                    print(f"post send error: post={post_id} in group={group_id}", file=sys.stderr)
            print(last_post_id)
            print(records)


if __name__ == '__main__':
    json_params = open("env.json").read()
    params = json.loads(json_params)

    args_parser = argparse.ArgumentParser(description='')
    args_parser.add_argument('--login', '-l', type=str, dest='login', help='vk login',
                             default=params["login"])
    args_parser.add_argument('--password', '-p', type=str, dest='password', help='vk password',
                             default=params["password"])
    args_parser.add_argument('--group_id', '-g', type=str, dest='group_id', help='vk group_id',
                             default=params["group_id"])
    parsed_args = args_parser.parse_args()
    login = parsed_args.login
    password = parsed_args.password
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth(token_only=True)
    vk = vk_session.get_api()
    main(parsed_args.group_id, '+')


