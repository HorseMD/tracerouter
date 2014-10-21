# A quick and dirty traceroute helper script.
#
# Traceroute to a given server in a list.
#
# You can also add and remove servers from servers.json, should
# you need/not need them.
# Make sure servers.json is in the same directory as this program.
#
# If ever the servers.json file gets lost from this file, it's format is
# [ { "name": server_name, "address": ip_address }, { "name": server2_name... etc } ]
#

from subprocess import check_output
import json
import os.path
import platform
import sys
import time

# Get the path where this program is running.
def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep

# Users may edit the following two variables as they like:
tracert_args = "" #any arguments you want to give tracer(oute) should go here. e.g. "-n"
date_format  = "%y-%m-%d %H-%M-%S"

# Users may (carefully) edit the following two variables as they see fit:
traceroute  = "tracert" if platform.system() == "Windows" else "traceroute"
server_file = getScriptPath() + "servers.json"

# Get the path of the directory we place the logs in.
def getLogDir():
    return getScriptPath() + os.sep + "logs" + os.sep

# Ensure that the given directory actually exists.
# if it doesnt, make it.
def ensure_dir(dire):
    d = os.path.dirname(dire)
    if not os.path.exists(d):
        os.makedirs(d)

# Whether or not the given num is between 1 and max_num.
def valid_choice(num, max_num):
    return num - 1 in range(max_num)

# User choses a number between 0 and how ever many servers there are.
# The numbers are displayed +1 more than they are, and then 1 is removed
# before this method returns the choice.
def get_choice(max_choice):
    choice = -1
    while choice == -1:
        try:
            choice = int(input("\nPlease make a choice: "))
            if not valid_choice(choice, max_choice):
                print("Invalid choice, please type a number that is actually there.")
                choice = -1
        except ValueError:
            print("Invalid choice, please type a number.")
            choice = -1
    return choice - 1

# Run the given command and save it to the given file.
def save_command(command, file_path, verbose=True):
    with open(file_path, 'w') as save_file:
        try:
            if verbose:
                print("Running {cmd}. This may take a while.").format(cmd=command[0])
            text = check_output(command)
            save_file.write(text.decode("utf-8"))
        except OSError:
            print("Couldn't run the {cmd} executable. (Is it installed?)").format(cmd=command[0])

# Begin the main part of the program. It's so simple that it's not really worth making it
# particularly object oriented.
if os.path.isfile(server_file):
    servers = json.loads(open(server_file).read())
    ensure_dir(getLogDir())

    print("Please choose a server by number:")
    for i in range(len(servers)):
        print("\t{index}. {name}").format(index=i + 1, name=servers[i]["name"])

    server   = servers[get_choice(len(servers))]
    # filter empty elements from command so its easy for users to set/unset arguments
    command  = filter(None, 
        [traceroute] + [tracert_args] + [server["address"]]
    )
    filename = "traceroute {name} ({address}) {time}.txt".format(
        name=server["name"],
        address=server["address"],
        time=time.strftime(date_format)
    )

    save_command(command, getLogDir() + filename)
    print("Traceroute saved to \"{name}\"").format(name=filename)
else:
    print("You are missing the %s file, so I cannot offer any servers." % server_file)
    print("It should be placed in the same folder that this program is located.")

