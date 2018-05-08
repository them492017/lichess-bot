from time import time

class Conversation():
    def __init__(self, game, engine, xhr, version):
        self.game = game
        self.engine = engine
        self.xhr = xhr
        self.version = version

    command_prefix = "!"

    def react(self, line, game):
        print("*** {} [{}] {}: {}".format(self.game.url(), line.room, line.username, line.text.encode("utf-8")))
        if (line.text[0] == self.command_prefix):
            self.command(line, game, line.text[1:].lower())
        pass

    def command(self, line, game, cmd):
        if cmd == "name":
            self.send_reply(line, "{} (lichess-bot v{})".format(self.engine.name(), self.version))
        elif cmd == "howto":
            self.send_reply(line, "How to run your own bot: lichess.org/api#tag/Chess-Bot")
        elif cmd == "eval" and line.room == "spectator":
            stats = self.engine.get_stats()
            self.send_reply(line, ", ".join(stats))
        elif cmd == "commands" or cmd == "help":
            msg = "Supported commands: !name, !parameters, !hardware, !howto and !eval"
            self.send_reply(line, msg)
        elif cmd == "engine parameters" or cmd == "parameters":
            msg = "2 Threads, Hash: 6144, Slow Mover:10, Contempt:100, Move Overhead:5000"
            self.send_reply(line, msg)
        elif cmd == "hardware":
            msg = "MacBook Air (Early 2015), 1.6 GHz Dual Core and 8 GM RAM"
            self.send_reply(line, msg)

    def send_reply(self, line, reply):
        self.xhr.chat(self.game.id, line.room, reply)


class ChatLine():
    def __init__(self, json):
        self.room = json.get("room")
        self.username = json.get("username")
        self.text = json.get("text")
