"""Bounded Nix sshd loopback startup/banner probe. No login credentials."""
import glob
import os
from pathlib import Path
import socket
import shlex
import subprocess
import tempfile
import time

root = Path(os.environ['BC_RUNTIME']) / 'root'
package = root / os.environ['BC_OPENSSH'].lstrip('/')
loader = root / 'nix/store/7nbi22pcc92y2fqbkyp7h3srvvklmckb-glibc-2.40-224/lib/ld-linux-x86-64.so.2'
prefix = [str(loader), '--library-path', ':'.join(glob.glob(str(root / 'nix/store/*/lib')))]
with tempfile.TemporaryDirectory(prefix='bc-sshd-') as tmp:
    d = Path(tmp)
    subprocess.run(prefix + [str(package/'bin/ssh-keygen'), '-q', '-t', 'ed25519', '-N', '', '-f', str(d/'host')], check=True)
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
    for helper in ('sshd-session', 'sshd-auth'):
        wrapper = d/helper
        wrapper.write_text('#!/bin/sh\nexec ' + shlex.join(prefix + [str(package/'libexec'/helper)]) + ' "$@"\n')
        wrapper.chmod(0o700)
    config = d/'sshd_config' 
    config.write_text(f'''ListenAddress 127.0.0.1
Port {port}
HostKey {d}/host
PidFile {d}/pid
SshdSessionPath {d}/sshd-session
SshdAuthPath {d}/sshd-auth
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication no
PermitRootLogin no
UsePAM no
AuthorizedKeysFile none
DisableForwarding yes
PermitTTY no
LoginGraceTime 5
''')
    command = prefix + [str(package/'bin/sshd'), '-f', str(config)]
    subprocess.run(command + ['-t'], check=True)
    print('PASS: sshd configuration validated', flush=True)
    with (d/'log').open('w+') as log:
        process = subprocess.Popen(command + ['-D', '-e'], stdout=log, stderr=log)
        try:
            for _ in range(30):
                if process.poll() is not None:
                    raise RuntimeError('sshd exited before banner')
                try:
                    with socket.create_connection(('127.0.0.1', port), timeout=1) as client:
                        client.settimeout(2)
                        banner = client.recv(256)
                        if not banner.startswith(b'SSH-2.0-'):
                            raise RuntimeError(f'no SSH banner: {banner!r}')
                        print('PASS: loopback banner: ' + banner.decode().strip())
                        break
                except ConnectionRefusedError:
                    time.sleep(.1)
            else:
                raise RuntimeError('startup deadline exceeded')
        finally:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            log.seek(0)
            print(log.read())
