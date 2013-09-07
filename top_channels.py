#	This script WHOIS'es every single user on the channels you are on,
# and collects/lists the channels they are on. It also ranks them
# by the number of people present on it, and lists them.

__module_name__ = "Top Channels"
__module_author__ = "Rohitt Shinde (http://xworkspace.blogspot.com)"
__module_version__ = "0.1a"
__module_description__ = "list the top channels in people you hang out with"

import xchat
import operator
import time
import sys
import os

users_lists = []
users = []
joined_channels = {}
channels = {}

myhook = None

# Get a list of all the channels, process it to make a user list
for chan in xchat.get_list('channels'):
	if chan.channel not in joined_channels.keys():
		joined_channels[chan.channel] = chan

for channel in joined_channels.itervalues():
	users_lists.append(channel.context.get_list('users'))

for user_list in users_lists:
	for user in user_list:
		nick = user.nick
		if nick not in users:
			users.append(nick)

print 'Number of users: %d\n' % (len(users))

# Try opening a file to write the results in
pathh = xchat.get_info('xchatdir') + '/top_channels.txt'
f = None
try:
	if(os.path.exists(pathh)):
		f = open(pathh, 'a')
	else:
		f = open(pathh, 'w')	
except IOError as e:
	print 'IO Error'

def add_channel(words, word_eol, userdata):
	global users
	global channels
	
	# Get channels for *current* event, remove ':' from first channel name
	channs = words[4:]
	channs[0] = channs[0][1:]
	
	for channel in channs:
		if channel in channels.keys():
			channels[channel] += 1
		else:
			channels[channel] = 1
	
	return xchat.EAT_ALL

def eat_all(words, word_eol, userdata):
	return xchat.EAT_ALL

def timer(userdata):
	global channels
	channels_by_rank = sorted(channels.iteritems(), key=operator.itemgetter(1),
														reverse=True)
	print '-------------------------------'
	for tup in channels_by_rank:
		print ' %30s :   %5s' %(tup[0], tup[1])
	return 1

def stop_timer(word, word_eol, userdata):
	global myhook
	if myhook is not None:
		xchat.unhook(myhook)
		myhook = None
		print 'Timer removed!'

myhook = xchat.hook_timer(60000, timer)
xchat.hook_command("STOP", stop_timer)
xchat.hook_server("319", add_channel)

xchat.hook_server("312", eat_all)
xchat.hook_server("330", eat_all)
xchat.hook_server("318", eat_all)
xchat.hook_server("311", eat_all)
xchat.hook_server("671", eat_all)
xchat.hook_server("317", eat_all)

# Now whois all the users
for user in users:
	command = 'WHOIS ' + user
	xchat.command(command)


