import os
import subprocess
import sys


def run_command_detached(command: list[str]):
    # First fork
    if os.fork() > 0:
        return  # Parent exits

    # Decouple from parent environment
    os.setsid()

    # Second fork
    if os.fork() > 0:
        sys.exit(0)  # Child exits, grandchild continues

    # Redirect standard I/O to /dev/null
    with open(os.devnull, 'wb') as devnull:
        os.dup2(devnull.fileno(), 0)  # stdin
        os.dup2(devnull.fileno(), 1)  # stdout
        os.dup2(devnull.fileno(), 2)  # stderr

    # Run the command
    subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Exit the second child to avoid lingering processes
    sys.exit(0)