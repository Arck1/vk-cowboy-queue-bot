#!python

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from vk_api import vk_api

from settings import *

vk_session = None
vk: vk_api.VkApi = None
params: dict = {}
parsed_args = {}
work: bool = False


def send_message(peer_id, msg):
    global vk
    vk.messages.send(peer_id=peer_id, message=msg)
    if DEBUG:
        print(f'message sended to {peer_id}: {msg}')  # TODO change to logging


def check_group_wall(group_id, count: int = 5):
    global vk
    result = vk.wall.get(owner_id=group_id, count=count, filter='owner')
    return result


def send_comment(group_id, post_id, msg: str = '+'):
    global vk
    result = vk.wall.createComment(owner_id=group_id, post_id=post_id, message=msg)
    if 'comment_id' in result:
        return result['comment_id']
    if DEBUG:
        print(result['error_code'], result['error_msg'], result['error_text'], file=sys.stderr)
    return -1


def main(group_id, message):
    work = True
    last_check = datetime.now()
    response = check_group_wall(group_id)
    res_count = response['count']
    records = response.get('items', [])
    last_post_id = records[0].get('id', -1) if res_count > 0 else -1
    while work:
        if datetime.now() - last_check > timedelta(milliseconds=TIMEOUT):
            response = check_group_wall(group_id)
            res_count = response['count']
            records = response.get('items', [])
            post_id = records[0].get('id', -1) if res_count > 0 else -1
            if post_id != last_post_id:
                res = send_comment(group_id, post_id, message)
                if res > 0:
                    last_post_id = post_id
                elif DEBUG:
                    print(f"post send error: post={post_id} in group={group_id}", file=sys.stderr)


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser(description='')
    args_parser.add_argument('--login', '-l', type=str, dest='login', help='vk login',
                             default=LOGIN)
    args_parser.add_argument('--password', '-p', type=str, dest='password', help='vk password',
                             default=PASSWORD)
    args_parser.add_argument('--group_id', '-g', type=int, dest='group_id', help='vk group_id',
                             default=GROUP_ID)
    args_parser.add_argument('--timeout', '-t', type=int, dest='timeout', help='requests timeout',
                             default=TIMEOUT)
    args_parser.add_argument('--message', '-m', type=str, dest='message', help='response message',
                             default=MESSAGE)
    parsed_args = args_parser.parse_args()

    LOGIN = parsed_args.login
    PASSWORD = parsed_args.password
    GROUP_ID = parsed_args.group_id
    TIMEOUT = parsed_args.timeout
    MESSAGE = parsed_args.message

    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth(token_only=True)
    vk = vk_session.get_api()

    main(parsed_args.group_id, MESSAGE)


