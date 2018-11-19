from vk_api import vk_api


class Bot:
    def __init__(self, login, password, group_id, message, timeout=20*1000, DEBUG=False):
        """
        Bot for checking group new posts and write comment
        :param login:
        :param password:
        :param group_id:
        :param timeout: default = 20_000 = 20 sec, because vk api query limit 5000, 24*60*60 / 5000 = 18 sec
        :param DEBUG:
        """
        self.DEBUG = DEBUG
        self.login = login
        self.passwrod = password
        self.group_id = group_id
        self.timeout = timeout
        try:
            vk_session = vk_api.VkApi(login, password)
            vk_session.auth(token_only=True)
            vk = vk_session.get_api()
        except Exception as e:
            raise ValueError(f'incorrect login / password: {e}')

    def send_message(self, peer_id, msg):
        global vk
        vk.messages.send(peer_id=peer_id, message=msg)
        if self.DEBUG:
            print(f'message sended to {peer_id}: {msg}')  # TODO change to logging

    def check_group_wall(self, group_id, count: int = 5):
        global vk
        result = vk.wall.get(owner_id=group_id, count=count, filter='owner')
        return result

    def send_comment(self, group_id, post_id, msg: str = '+'):
        global vk
        result = vk.wall.createComment(owner_id=group_id, post_id=post_id, message=msg)
        if 'comment_id' in result:
            return result['comment_id']
        if self.DEBUG:
            print(result['error_code'], result['error_msg'], result['error_text'], file=sys.stderr)
        return -1

