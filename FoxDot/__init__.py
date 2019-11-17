#!/usr/bin/python
"""
FoxDot is a Python library and programming environment that provides a fast and
user-friendly abstraction to the powerful audio-engine, SuperCollider. It comes
with its own IDE, which means it can be used straight out of the box; all you need
is Python and SuperCollider and you're ready to go!

For more information on installation, check out [the guide](http://foxdot.org/installation),
or if you're already set up, you can also find a useful starter guide that introduces the
key components of FoxDot on [the website](http://foxdot.org/).

Please see the [documentation](http://docs.foxdot.org/) for more detailed information on
the FoxDot classes and how to implement them.

Copyright Ryan Kirkbride 2015
"""

import atexit
import datetime
import getpass
import os
import platform
import psutil
import select
import subprocess
import sys
import time


def check_and_kill_sclang_linux():
    for p in psutil.process_iter(attrs=["name", "cmdline"]):
        if (p.info["name"] == "sclang") or (
            p.info["cmdline"] and p.info["cmdline"][0] == "sclang"
        ):
            print("Killing running instance of sclang!")
            p.kill()


def boot_supercollider():
    """ Uses subprocesses to boot supercollider from the cli """
    atexit.register(check_and_kill_sclang_linux)
    thisdir = os.getcwd()
    arg = thisdir + "/FoxDot/startup.scd"
    OS = platform.system()

    if OS == "Windows":
        print("OS: Windows")
        sclangloc = os.popen('where /R "C:\\Program Files" sclang.exe').read()
        thiscwd = str(sclangloc)
        ourcwd = thiscwd.replace("\\sclang.exe\n", "")

        def is_proc_running(name):
            for p in psutil.process_iter(attrs=["name", "exe", "cmdline"]):
                procname = (
                    p.info["name"]
                    or p.info["exe"]
                    and os.path.basename(p.info["exe"]) == name
                    or p.info["cmdline"]
                    and p.info["cmdline"][0] == name
                )
                if procname.startswith(name):
                    return True
            return False

        running = is_proc_running("sclang")

        if running == False:
            subprocess.Popen([sclangloc, arg], cwd=ourcwd, shell=True)

    elif OS == "Linux":
        check_and_kill_sclang_linux()
        print("Starting sclang...")
        process = subprocess.Popen(
            ["sclang", arg], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        # Now check that FoxDot actually started by
        # waiting for at least 5 seconds of no output.
        # TODO: We could just check that the server is responding here
        poll_obj = select.poll()
        poll_obj.register(process.stdout, select.POLLIN)
        time_limit = datetime.datetime.now() + datetime.timedelta(seconds=5)
        while datetime.datetime.now() < time_limit:
            poll_result = poll_obj.poll(0)
    else:
        print("Operating system unrecognised")


# Boot supercollider first?
# boot_supercollider()

# This import releases the kraken
from .lib import *
print("FoxDot initialized. Happy hacking!")
