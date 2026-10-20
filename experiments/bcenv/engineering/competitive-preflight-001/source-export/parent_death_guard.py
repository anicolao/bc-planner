"""Fixed trusted link from adapter process lifetime to its unshare child.

This runs before any candidate code. It changes only its own death signal.
"""
import ctypes
import os
import signal
import sys


def main():
    expected_parent = int(sys.argv[1])
    command = sys.argv[2:]
    if not command or command[0] != '/usr/bin/unshare':
        raise ValueError('invalid_guard_command')
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
        raise OSError(ctypes.get_errno(), 'parent_death_signal_failed')
    # Close the race where the parent died before prctl installed the signal.
    if os.getppid() != expected_parent:
        return 1
    os.execv(command[0], command)


if __name__ == '__main__':
    raise SystemExit(main())
