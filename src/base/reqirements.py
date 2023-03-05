import subprocess, sys, pkg_resources


def install():

    required = {"psutil", "requests"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if len(missing) != 0:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
