"""Bounded synthetic adversarial probes. No credentials, models or hidden data."""
import base64
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from unittest.mock import patch

from probe_adapter import BASE, PYTHON, ProbeSandboxAdapter
from services.controller import (ControllerLimits, ExecRequest, FrozenContext,
    ReadRequest, ToolCall, TurnReply, WriteRequest, run_synthetic)

RESULTS = []
ADAPTER = ProbeSandboxAdapter()
TOKEN = str(time.time_ns())


def execute(source, *, wall=2, cap=16384, memory=268435456):
    reply = ADAPTER.exec(ExecRequest((PYTHON, '-I', '-B', '-c', source), '.', wall, memory, cap))
    return reply, dict(ADAPTER.last_execution)


def data(source, **kwargs):
    reply, meta = execute(source, **kwargs)
    assert reply.status == 'succeeded', (reply.status, reply.stderr, meta)
    return json.loads(reply.stdout), meta


def check(name, test):
    start = time.monotonic()
    try:
        evidence = test()
        result = {'test': name, 'status': 'passed', 'evidence': evidence}
    except Exception as error:
        result = {'test': name, 'status': 'failed', 'error': repr(error)}
    result['elapsed_seconds'] = round(time.monotonic() - start, 4)
    RESULTS.append(result)
    print(json.dumps(result), flush=True)


def filesystem_confidentiality():
    host = str(BASE / 'host-canary.txt')
    value, meta = data('''import os,json
paths = ''' + repr([host, '/proc/1/root' + host, '/proc/self/root' + host,
                    '/../../' + host.lstrip('/'), '/workspace/../../' + host.lstrip('/')]) + '''
out={}
for path in paths:
 try:
  out[path]={'read':open(path).read()}
 except OSError as e:
  out[path]={'errno':e.errno}
print(json.dumps(out))
''')
    assert all('errno' in v for v in value.values()), value
    return {'attempts': value, 'supervisor': meta}


def immutable_inputs():
    targets = ['/workspace/docs/canary.txt', '/opt/io_worker.py', PYTHON]
    before = {p: hashlib.sha256((BASE / 'fixture-root' / p.lstrip('/')).read_bytes()).hexdigest()
              for p in targets}
    value, meta = data('''import os,json
targets=''' + repr(targets) + '''
result={}
for p in targets:
 item={}
 for label,operation in [('write',lambda:open(p,'ab').write(b'synthetic-attempt')),
                         ('chmod',lambda:os.chmod(p,0o777))]:
  try: operation();item[label]='succeeded'
  except OSError as e: item[label]=e.errno
 result[p]=item
mounts={parts[4]:parts[5] for line in open('/proc/self/mountinfo') if (parts:=line.split())[4]
        in ('/','/workspace/src','/workspace/scratch','/tmp','/proc')}
print(json.dumps({'attempts':result,'mount_options':mounts}))
''')
    assert all(v['write'] in (13, 30) and v['chmod'] == 30 for v in value['attempts'].values()), value
    assert 'ro' in value['mount_options']['/'].split(',')
    assert all('rw' in value['mount_options'][p].split(',')
               for p in ('/workspace/src', '/workspace/scratch', '/tmp'))
    assert all(hashlib.sha256((BASE / 'fixture-root' / p.lstrip('/')).read_bytes()).hexdigest() == h
               for p, h in before.items())
    return {'candidate': value, 'hashes_unchanged': True, 'supervisor': meta}


def capabilities():
    value, meta = data('''import ctypes,json,os
libc=ctypes.CDLL(None,use_errno=True)
status={line.split(':')[0]:line.split(':')[1].strip() for line in open('/proc/self/status')
        if line.startswith(('Cap','NoNewPrivs','Seccomp'))}
result={'status':status,'pid':os.getpid()}
try: os.chroot('/workspace');result['chroot']='succeeded'
except OSError as e: result['chroot']=e.errno
rc=libc.mount(None,b'/workspace/docs',None,32,None)
result['remount']={'rc':rc,'errno':ctypes.get_errno()}
print(json.dumps(result))
''')
    assert value['pid'] == 2
    assert all(value['status'][key] == '0000000000000000'
               for key in ('CapEff', 'CapPrm', 'CapInh', 'CapAmb', 'CapBnd'))
    assert value['status']['NoNewPrivs'] == '1'
    assert value['chroot'] == 1 and value['remount'] == {'rc': -1, 'errno': 1}, value
    return {'candidate': value, 'supervisor': meta}


def descriptor_environment():
    descriptor = os.open(BASE / 'host-canary.txt', os.O_RDONLY)
    os.set_inheritable(descriptor, True)
    os.environ['SYNTHETIC_PARENT_ONLY'] = 'outside-environment-canary'
    try:
        value, meta = data('''import os,json
fds={}
for name in os.listdir('/proc/self/fd'):
 try:fds[name]=os.readlink('/proc/self/fd/'+name)
 except FileNotFoundError:pass
print(json.dumps({'fds':fds,'environment':dict(os.environ)}))
''')
    finally:
        os.close(descriptor)
        os.environ.pop('SYNTHETIC_PARENT_ONLY', None)
    assert set(value['fds']) == {'0', '1', '2'}, value
    assert set(value['environment']) <= {'HOME', 'PATH', 'LANG', 'PYTHONDONTWRITEBYTECODE', 'LC_CTYPE'}
    assert 'SYNTHETIC_PARENT_ONLY' not in value['environment']
    return {'candidate': value, 'supervisor': meta}


def process_boundary():
    process = subprocess.Popen([sys.executable, '-I', '-B', '-c', 'import time;time.sleep(10)'])
    try:
        assert process.pid > 10
        value, meta = data('''import os,json
pids=[int(n) for n in os.listdir('/proc') if n.isdigit()]
try:os.kill(''' + str(process.pid) + ''',0);signal='succeeded'
except OSError as e:signal=e.errno
print(json.dumps({'pids':pids,'outside_process_signal_zero':signal}))
''')
        assert value == {'pids': [1, 2], 'outside_process_signal_zero': 3}, value
        assert process.poll() is None
    finally:
        process.terminate()
        process.wait(timeout=2)
    return {'candidate': value, 'supervisor': meta}


def network_boundary():
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        listener.listen(1)
        port = listener.getsockname()[1]
        listener.settimeout(.2)
        value, meta = data('''import socket,json
s=socket.socket();s.settimeout(.2)
try:s.connect(('127.0.0.1',''' + str(port) + '''));result={'connected':True}
except OSError as e:result={'errno':e.errno}
s.close();print(json.dumps(result))
''')
        assert 'errno' in value, value
        try:
            connection, unused = listener.accept()
            connection.close()
            raise AssertionError('sandbox reached synthetic host listener')
        except TimeoutError:
            pass
    return {'candidate': value, 'host_listener_accepted': False, 'supervisor': meta,
            'network_configuration': 'none; no NETLINK_ROUTE use'}


def unified_io():
    path = 'src/roundtrip-' + TOKEN + '.txt'
    ADAPTER.write(WriteRequest(path, b'synthetic unified roundtrip'))
    assert ADAPTER.read(ReadRequest(path, 10, 7)) == b'unified'
    value, meta = data('import json;print(json.dumps(open(' + repr('/workspace/' + path) + ').read()))')
    assert value == 'synthetic unified roundtrip'
    return {'read_write_exec_same_file': True, 'supervisor': meta}


def symlink_io():
    leaf = 'outside-link-' + TOKEN
    interior = 'reference-link-' + TOKEN
    value, meta = data('''import os,json
os.symlink(''' + repr(str(BASE / 'host-canary.txt')) + ''','/workspace/src/''' + leaf + '''')
os.symlink('/workspace/docs/canary.txt','/workspace/src/''' + interior + '''')
print(json.dumps({'created_synthetic_symlinks':True}))
''')
    rejected = []
    for name in (leaf, interior):
        for op in ('read', 'write'):
            try:
                if op == 'read': ADAPTER.read(ReadRequest('src/' + name, 0, 128))
                else: ADAPTER.write(WriteRequest('src/' + name, b'synthetic replacement'))
            except RuntimeError:
                rejected.append(name + ':' + op)
            else:
                raise AssertionError('symlink followed')
    assert (BASE / 'host-canary.txt').read_text() == 'SYNTHETIC-OUTSIDE-ROOT-CANARY\n'
    assert ADAPTER.read(ReadRequest('docs/canary.txt', 0, 128)) == b'synthetic-read-only-reference\n'
    return {'rejected_operations': rejected, 'canaries_unchanged': True, 'supervisor': meta}


def descendant_teardown(exit_parent=False):
    name = ('exit' if exit_parent else 'timeout') + '-heartbeat-' + TOKEN
    heartbeat = BASE / 'writable' / 'scratch' / name
    source = '''import os,time
if os.fork() == 0:
 os.setsid()
 with open('/workspace/scratch/''' + name + '''','ab',buffering=0) as f:
  while True:f.write(b'x');time.sleep(.025)
else:
 time.sleep(''' + ('.3' if exit_parent else '8') + ''')
'''
    reply, meta = execute(source, wall=1)
    assert reply.status == ('succeeded' if exit_parent else 'timeout'), (reply, meta)
    assert heartbeat.exists() and heartbeat.stat().st_size > 0
    size = heartbeat.stat().st_size
    time.sleep(.2)
    assert heartbeat.stat().st_size == size, 'setsid descendant kept running'
    assert meta['elapsed_seconds'] < 2
    return {'status': reply.status, 'heartbeat_bytes': size,
            'heartbeat_stable_after_return_seconds': .2, 'supervisor': meta}


def output_limit():
    reply, meta = execute('import os;os.write(1,b"x"*100000)', cap=2048)
    assert reply.status == 'failed' and meta['stop_reason'] == 'output_limit', (reply, meta)
    assert len(reply.stdout) + len(reply.stderr) <= 2048
    return meta


def closed_stream_timeout():
    reply, meta = execute('import os,time;os.close(0);os.close(1);os.close(2);time.sleep(8)', wall=1)
    assert reply.status == 'timeout' and meta['elapsed_seconds'] < 1.5, (reply, meta)
    return meta


def selector_setup_failure_cleanup():
    captured = []
    original_popen = subprocess.Popen
    def popen(*args, **kwargs):
        process = original_popen(*args, **kwargs)
        captured.append(process)
        return process
    with patch('probe_adapter.subprocess.Popen', popen), patch(
            'probe_adapter.selectors.DefaultSelector', side_effect=RuntimeError('synthetic_selector_failure')):
        try:
            execute('import time;time.sleep(2)')
        except RuntimeError as error:
            assert str(error) == 'synthetic_selector_failure'
        else:
            raise AssertionError('setup failure was not injected')
    assert len(captured) == 1
    process = captured[0]
    assert process.poll() is not None, 'synthetic child survived setup failure'
    assert all(stream.closed for stream in (process.stdin, process.stdout, process.stderr))
    return {'setup_failure': 'DefaultSelector constructor', 'child_reaped': True,
            'all_three_pipes_closed': True, 'exit_code': process.returncode}


def outer_controller_death_cleanup():
    name = 'outer-death-' + TOKEN
    heartbeat = BASE / 'writable' / 'scratch' / name
    candidate = '''import os,time
if os.fork()==0:
 os.setsid()
 end=time.monotonic()+3
 with open('/workspace/scratch/''' + name + '''','ab',buffering=0) as f:
  while time.monotonic()<end:f.write(b'x');time.sleep(.025)
else:time.sleep(3)
'''
    controller = 'from probe_adapter import ProbeSandboxAdapter,PYTHON;from services.controller import ExecRequest;'
    controller += 'ProbeSandboxAdapter().exec(ExecRequest((PYTHON,"-I","-B","-c",' + repr(candidate)
    controller += '),".",5,268435456,16384))'
    process = subprocess.Popen([sys.executable, '-B', '-c', controller], cwd=BASE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    try:
        deadline = time.monotonic()+1.5
        while not heartbeat.exists() and time.monotonic()<deadline:
            time.sleep(.025)
        assert heartbeat.exists(), 'bounded synthetic candidate did not start'
        process.kill()  # only this fresh dedicated synthetic controller
        process.wait(timeout=2)
        time.sleep(.15)
        size = heartbeat.stat().st_size
        time.sleep(.25)
        assert heartbeat.stat().st_size == size, 'candidate survived outer-controller death'
        assert size < 40, 'heartbeat reached too much of natural 3 second duration'
        return {'outer_controller_exit_code': process.returncode,
            'setsid_descendant_heartbeat_bytes': size,
            'heartbeat_stable_seconds': .25, 'candidate_natural_duration_seconds': 3}
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=2)
        process.stdout.close()
        process.stderr.close()


def candidate_cannot_disable_teardown(outer_death=False):
    name = ('outer' if outer_death else 'timeout') + '-hostile-death-link-' + TOKEN
    heartbeat = BASE / 'writable' / 'scratch' / name
    candidate = '''import ctypes,os,time
assert os.getpid()!=1
os.setsid()
assert ctypes.CDLL(None,use_errno=True).prctl(1,0,0,0,0)==0
os.close(0);os.close(1);os.close(2)
end=time.monotonic()+3
with open('/workspace/scratch/''' + name + '''','ab',buffering=0) as f:
 while time.monotonic()<end:f.write(b'x');time.sleep(.025)
'''
    if outer_death:
        controller = 'from probe_adapter import ProbeSandboxAdapter,PYTHON;from services.controller import ExecRequest;'
        controller += 'ProbeSandboxAdapter().exec(ExecRequest((PYTHON,"-I","-B","-c",' + repr(candidate)
        controller += '),".",5,268435456,16384))'
        process = subprocess.Popen([sys.executable, '-B', '-c', controller], cwd=BASE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        try:
            deadline = time.monotonic()+1.5
            while not heartbeat.exists() and time.monotonic()<deadline:
                time.sleep(.025)
            assert heartbeat.exists(), 'bounded synthetic candidate did not start'
            process.kill()
            process.wait(timeout=2)
            meta = {'outer_controller_exit_code': process.returncode}
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=2)
            process.stdout.close()
            process.stderr.close()
    else:
        reply, meta = execute(candidate, wall=1)
        assert reply.status == 'timeout' and meta['elapsed_seconds'] < 1.5, (reply, meta)
    assert heartbeat.exists() and heartbeat.stat().st_size > 0
    time.sleep(.15)
    size = heartbeat.stat().st_size
    time.sleep(.25)
    assert heartbeat.stat().st_size == size, 'detached PDEATHSIG-clear candidate survived'
    assert size < 50, 'candidate reached too much of its natural 3 second duration'
    return {'candidate_actions': ['setsid', 'clear own PDEATHSIG', 'close 0/1/2'],
            'natural_duration_seconds': 3, 'heartbeat_bytes': size,
            'heartbeat_stable_seconds': .25, 'supervisor': meta}


def trusted_init_protection():
    value, meta = data('''import ctypes,json,os
libc=ctypes.CDLL(None,use_errno=True)
result={'candidate_pid':os.getpid(),'parent_pid':os.getppid()}
for name in ('/proc/1/mem','/proc/1/fd/0'):
 try:
  fd=os.open(name,os.O_RDONLY);os.close(fd);result[name]='opened'
 except OSError as e:result[name]=e.errno
rc=libc.ptrace(16,1,None,None)
result['ptrace_attach']={'rc':rc,'errno':ctypes.get_errno()}
print(json.dumps(result))
''')
    assert value['candidate_pid'] == 2 and value['parent_pid'] == 1
    assert value['/proc/1/mem'] == value['/proc/1/fd/0'] == 13, value
    assert value['ptrace_attach'] == {'rc': -1, 'errno': 1}, value
    return {'candidate': value, 'supervisor': meta}


def memory_limit():
    value, meta = data('''import json
try:
 value=bytearray(80*1024*1024)
 print(json.dumps({'allocated':len(value)}))
except MemoryError:
 print(json.dumps({'memory_error':True}))
''', memory=67108864)
    assert value == {'memory_error': True}, value
    return {'candidate': value, 'per_process_only': True, 'supervisor': meta}


def file_limit():
    value, meta = data('''import json,os
p='/workspace/scratch/file-limit-''' + TOKEN + ''''
try:
 with open(p,'wb',buffering=0) as f:
  for unused in range(8):f.write(b'x'*262144)
 result={'write':'succeeded'}
except OSError as e:result={'errno':e.errno}
result['size']=os.stat(p).st_size
print(json.dumps(result))
''')
    assert value == {'errno': 27, 'size': 1048576}, value
    return {'candidate': value, 'per_file_only': True, 'supervisor': meta}


def controller_integration():
    name = 'src/controller-' + TOKEN + '.txt'
    calls = [
        ToolCall('w', 'workspace_write', json.dumps({'path': name, 'content': 'controller actual sandbox'})),
        ToolCall('r', 'workspace_read', json.dumps({'path': name, 'offset': 0, 'limit': 128})),
        ToolCall('e', 'workspace_exec', json.dumps({'argv': [PYTHON, '-I', '-B', '-c',
            'print(open(' + repr('/workspace/' + name) + ').read())'], 'cwd': '.', 'timeout_seconds': 2}))]
    class SyntheticTransport:
        def next_turn(self, request):
            assert request.context.system == b'synthetic controller-only system'
            assert request.context.task == b'synthetic controller-only task'
            return TurnReply(calls=tuple(calls)) if request.turn == 1 else TurnReply(final_text='probe complete')
    class UnusedScrimmage:
        def __getattr__(self, name):
            raise AssertionError('scrimmage unexpectedly used')
    report = run_synthetic(FrozenContext(b'synthetic controller-only system', b'synthetic controller-only task'),
        SyntheticTransport(), ADAPTER, UnusedScrimmage(), limits=ControllerLimits(max_turns=2))
    outputs = [json.loads(item) for item in report.transcript[1:]]
    assert report.status == 'complete' and report.tool_calls == 3 and report.turns == 2
    assert [item['result']['status'] for item in outputs] == ['complete', 'complete', 'succeeded'], outputs
    assert outputs[1]['result']['text'] == 'controller actual sandbox'
    assert outputs[2]['result']['stdout'] == 'controller actual sandbox\n'
    return {'status': report.status, 'tool_calls': report.tool_calls,
            'initial_sha256': report.initial_sha256, 'outputs': outputs,
            'transport': 'synthetic fixed replies; no model invocation'}


def controller_host_io_rejection():
    host = str(BASE / 'host-canary.txt')
    calls = (
        ToolCall('host_read', 'workspace_read', json.dumps({'path': host, 'offset': 0, 'limit': 128})),
        ToolCall('host_write', 'workspace_write', json.dumps({'path': host, 'content': 'synthetic replacement'})),
        ToolCall('native_exec', 'exec_command', json.dumps({'cmd': 'true'})),
        ToolCall('isolated_exec', 'workspace_exec', json.dumps({'argv': [PYTHON, '-I', '-B', '-c',
            'import os;print(os.path.exists(' + repr(host) + '))'], 'cwd': '.', 'timeout_seconds': 2})),
    )
    class SyntheticTransport:
        def next_turn(self, request):
            assert request.tool_names == ('workspace_read', 'workspace_write', 'workspace_exec',
                'scrimmage_submit', 'scrimmage_result', 'scrimmage_replay')
            return TurnReply(calls=calls) if request.turn == 1 else TurnReply(final_text='probe complete')
    report = run_synthetic(FrozenContext(b'synthetic system', b'synthetic task'),
        SyntheticTransport(), ADAPTER, object(), limits=ControllerLimits(max_turns=2))
    outputs = [json.loads(item) for item in report.transcript[1:]]
    assert report.status == 'complete' and report.tool_calls == 4
    assert [r['result'].get('reason') for r in outputs[:3]] == [
        'invalid_arguments', 'invalid_arguments', 'unknown_tool'], outputs
    assert outputs[3]['result']['status'] == 'succeeded' and outputs[3]['result']['stdout'] == 'False\n'
    assert (BASE / 'host-canary.txt').read_text() == 'SYNTHETIC-OUTSIDE-ROOT-CANARY\n'
    return {'status': report.status, 'tool_calls': report.tool_calls,
            'outputs': outputs, 'outside_canary_unchanged': True,
            'transport': 'synthetic fixed replies; no model invocation'}


if __name__ == '__main__':
    for name, test in [
        ('outside_root_confidentiality', filesystem_confidentiality),
        ('immutable_reference_runtime_helper', immutable_inputs),
        ('dropped_capabilities_no_new_privileges', capabilities),
        ('clean_descriptors_and_environment', descriptor_environment),
        ('private_process_namespace', process_boundary),
        ('host_loopback_unreachable', network_boundary),
        ('same_root_read_write_exec', unified_io),
        ('symlink_io_rejection', symlink_io),
        ('timeout_kills_setsid_descendant', descendant_teardown),
        ('init_exit_kills_setsid_descendant', lambda: descendant_teardown(True)),
        ('bounded_combined_output', output_limit),
        ('closed_streams_cannot_evade_deadline', closed_stream_timeout),
        ('selector_setup_failure_cleans_process_and_pipes', selector_setup_failure_cleanup),
        ('outer_controller_death_kills_setsid_descendant', outer_controller_death_cleanup),
        ('hostile_candidate_cannot_disable_timeout_teardown', candidate_cannot_disable_teardown),
        ('hostile_candidate_cannot_disable_outer_death_teardown', lambda: candidate_cannot_disable_teardown(True)),
        ('trusted_namespace_init_protected_from_candidate', trusted_init_protection),
        ('per_process_address_space_limit', memory_limit),
        ('per_file_size_limit', file_limit),
        ('synthetic_controller_actual_adapter', controller_integration),
        ('six_tool_controller_host_io_rejection', controller_host_io_rejection)]:
        check(name, test)
    document = {'schema': 'bcenv.unshare-boundary-probe.v1',
        'scope': 'fresh synthetic fixture, no model invocation', 'tests': RESULTS,
        'passed': sum(r['status'] == 'passed' for r in RESULTS),
        'failed': sum(r['status'] == 'failed' for r in RESULTS),
        'aggregate_resource_enforcement': 'not implemented or accepted',
        'complete_isolation_claim': 'not accepted'}
    (BASE / 'unshare-results.json').write_text(json.dumps(document, indent=2) + '\n')
    print(json.dumps({'passed': document['passed'], 'failed': document['failed']}))
    raise SystemExit(bool(document['failed']))
