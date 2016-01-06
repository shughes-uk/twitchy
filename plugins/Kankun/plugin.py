from plugins.BasePlugin import BasePlugin
from plugins.devices import KankunSocket
from yaml import load


class KankunPlugin(BasePlugin):

    def __init__(self, twitchy):
        super(KankunPlugin, self).__init__(twitchy)
        self.config = load(open('config.txt', 'r'))
        self.logger.info(self.config)
        self.registerCommand('secret', self.popcorn)
        self.kankun = KankunSocket(self.config['kankun_ip'])
        self.voted = []
        self.triggered = False

    def popcorn(self, user, args, full_message):
        if not self.triggered:
            if full_message['username'] not in self.voted:
                self.voted.append(full_message['username'])
                if len(self.voted) >= 30:
                    self.triggered = True
                    self.twitchy.send_message("ITTTTSSS POPCORN TIIIIME!!!", full_message['channel'])
                    self.kankun.do_turn_on_timer(10)
                else:
                    msg = "Thanks for voting for popcorn {0}, current votecount is {1}".format(user, len(self.voted))
                    self.twitchy.send_message(msg, full_message['channel'])
