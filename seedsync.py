import pprint
from deluge.ui.client import client
from twisted.internet import reactor
from deluge.log import setupLogger

STATUS_KEYS = [
    "state",
    "save_path",
    "name",
    "is_finished",
]

pp = pprint.PrettyPrinter(indent=4)
host = "########"
port = 58846
username = "###########"
password = "###########"
d = client.connect(host, port, username, password)

def on_connect_success(result):
    print "Connection Success!"
    def on_get_torrent_status(status):
        if status["save_path"] == '/var/lib/deluge/downloads/New/':
            pp.pprint(status)
    def on_get_session_state(state):
        print "Got state."
        for torrent_id in state:
            client.core.get_torrent_status(torrent_id, STATUS_KEYS).addCallback(on_get_torrent_status)
    client.core.get_session_state().addCallback(on_get_session_state)

def on_connect_fail(result):
    print "Connection failed!"
    print "result:", result

d.addCallback(on_connect_success)
d.addErrback(on_connect_fail)

reactor.run()
