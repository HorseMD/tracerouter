#Tracerouter

Now accepting: a better name

A cross-platform python script that lets you rapidly traceroute to a particular server from a list.

##Usage

In a fresh installation, the `servers.json` file contains a few mock entries which provide
a reference as to how to add servers to the list.

1. `name:` is a human-readable name to use when referencing the servers in the logs.
2. `address:` is the address of the server. This is the addressed passed to the traceroute program and
so can be any format supported by traceroute.

Traceroute logs are saved inside a directory called `logs/` which is created in the directory in
which the script is run.

