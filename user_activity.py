# Quick and dirty solution to:
#   Alert when particular user gets "active" in channel.

__module_name__ = "User Activity Monitor"
__module_author__ = "Rohitt Shinde (http://www.rohitt.com)"
__module_version__ = "0.1"
__module_description__ = """User is online but away/inactive? Waiting for her
                            to get active in the public channel so that you can
                            start a private conversion? I think this could help."""


import xchat
import os


print "\0034",__module_name__, __module_version__,"has been loaded\003"

# you can change mplayer with your favorite option
ALERTER = "mplayer"
AUDIO_FILE = "/path/to/alert_tone"

COMMAND = ALERTER + ' ' + AUDIO_FILE
# replace with the nick name(s) you want to track
TARGETS = ['nick1', 'nick2']

def on_public_message(word, word_eol, userdata):
    # all that we need is current nickname
    nick = word[0]
    # strip out the color codes
    nick = nick[3:]
    if nick in TARGETS:
        # bajav :D
        os.system(COMMAND)


xchat.hook_print("Channel Message", on_public_message)
