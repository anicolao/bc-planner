"""Trusted disposable-fixture launcher; never called with model-selected config.

Runs only inside an already-created user/mount/PID/IPC/UTS/empty-network
namespace. Does not open netlink sockets or configure network interfaces.
This is a probe component, not an accepted production sandbox.
"""
import ctypes
import argparse
import errno
import json
import os
from pathlib import Path
import resource
import subprocess
import sys

BASE = Path('/workspace/shared/bc23-source-export-probe')
ROOT = BASE / 'fixture-root'
PYTHON = '/nix/store/h3l4z7p6wny3phbckwwhy1i2g52pdnj4-python3-3.13.15/bin/python3'
LIBC = ctypes.CDLL(None, use_errno=True)
LIBC.mount.argtypes = [ctypes.c_char_p] * 3 + [ctypes.c_ulong, ctypes.c_char_p]
LIBC.mount.restype = ctypes.c_int


def mount(source, target, filesystem=None, flags=0, options=None):
    values = [None if value is None else os.fsencode(value)
              for value in (source, target, filesystem)]
    if LIBC.mount(*values, flags, None if options is None else options.encode()) != 0:
        error = ctypes.get_errno()
        raise OSError(error, 'namespace_mount_failed:' + str(target))


def setup(readonly_workspace=False):
    # Bind only this newly created synthetic fixture, never the host root/home.
    mount(ROOT, ROOT, flags=4096)  # MS_BIND
    for name in ('src', 'scratch'):
        mount(BASE / 'writable' / name, ROOT / 'workspace' / name, flags=4096)
        if readonly_workspace:
            mount(None, ROOT / 'workspace' / name, flags=4096 | 32 | 1 | 2 | 4 | 8)
    mount('proc', ROOT / 'proc', 'proc', 2 | 4 | 8)  # nosuid,nodev,noexec
    mount('tmpfs', ROOT / 'tmp', 'tmpfs', 2 | 4 | 8, 'size=4194304,mode=1777')
    mount(None, ROOT, flags=4096 | 32 | 1 | 2 | 4)  # bind,remount,ro,nosuid,nodev
    os.chroot(ROOT)
    os.chdir('/workspace')
    # Drop every permitted/effective/inheritable capability for candidate code.
    class Header(ctypes.Structure):
        _fields_ = [('version', ctypes.c_uint32), ('pid', ctypes.c_int)]
    class Data(ctypes.Structure):
        _fields_ = [('effective', ctypes.c_uint32), ('permitted', ctypes.c_uint32),
                    ('inheritable', ctypes.c_uint32)]
    if LIBC.prctl(38, 1, 0, 0, 0) != 0:  # PR_SET_NO_NEW_PRIVS
        raise OSError(ctypes.get_errno(), 'no_new_privileges_failed')
    # Drop the bounding set while the setup-only namespace capabilities still
    # exist, so a later exec cannot restore them through root/file semantics.
    last_capability = int(Path('/proc/sys/kernel/cap_last_cap').read_text())
    if not 0 <= last_capability <= 63:
        raise ValueError('unsupported_capability_range')
    for capability in range(last_capability + 1):
        if LIBC.prctl(24, capability, 0, 0, 0) != 0:  # PR_CAPBSET_DROP
            raise OSError(ctypes.get_errno(), 'capability_bounding_drop_failed')
    header, data = Header(0x20080522, 0), (Data * 2)()
    if LIBC.capset(ctypes.byref(header), ctypes.byref(data)) != 0:
        raise OSError(ctypes.get_errno(), 'capability_drop_failed')
    os.closerange(3, 65536)
    os.environ.clear()
    os.environ.update(HOME='/workspace', PATH=str(Path(PYTHON).parent),
                      LANG='C.UTF-8', PYTHONDONTWRITEBYTECODE='1')


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--cwd', default='.')
        parser.add_argument('--memory', type=int, default=268435456)
        parser.add_argument('--readonly-workspace', action='store_true')
        parser.add_argument('command', nargs=argparse.REMAINDER)
        args = parser.parse_args()
        command = args.command[1:] if args.command[:1] == ['--'] else args.command
        if not command or not 16777216 <= args.memory <= 268435456:
            raise ValueError('invalid_launcher_request')
        setup(args.readonly_workspace)
        # chdir happens only after chroot; this field can never select a host cwd.
        os.chdir(args.cwd)
        # Per-process limits supplement the test supervisor; they are explicitly
        # not aggregate process-tree/cgroup CPU, memory, process or disk quotas.
        resource.setrlimit(resource.RLIMIT_AS, (args.memory, args.memory))
        resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
        resource.setrlimit(resource.RLIMIT_FSIZE, (1048576, 1048576))
        resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        # Keep a trusted PID1. Candidate code must never own the death signal
        # that unshare uses to destroy this PID namespace: an untrusted PID1
        # could clear PDEATHSIG, setsid(), and survive supervisor group cleanup.
        # Non-dumpable init prevents its child from changing this trusted state
        # through ptrace or proc memory/descriptor handles. Its environment and
        # descriptors contain only the already-sanitized sandbox inputs anyway.
        if LIBC.prctl(4, 0, 0, 0, 0) != 0:  # PR_SET_DUMPABLE
            raise OSError(ctypes.get_errno(), 'trusted_init_dumpability_failed')
        process = subprocess.Popen(command, close_fds=True, env=os.environ)
        code = process.wait()
        # Exiting trusted namespace PID1 kills any surviving descendants,
        # including candidate-created sessions and double-forked workers.
        return code if code >= 0 else 128 - code
    except OSError as error:
        # Setup errors contain only fixed fixture paths/reason labels.
        print(json.dumps({'status': 'setup_failed', 'errno': error.errno,
                          'action': error.strerror}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
