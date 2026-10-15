import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class KeyboardHealthTest(unittest.TestCase):
    def test_device_changes_restart_linux_without_restarting_healthy_listeners(self):
        for platform, connected, expected in (
            ('linux', ['event1'], 0),
            ('linux', ['event1', 'event2'], 1),
            ('linux', [], 1),
            ('darwin', ['event1', 'event2'], 0),
        ):
            with self.subTest(platform=platform, connected=connected), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / 'flimsy.py'
                shutil.copyfile(Path(__file__).parents[1] / 'flimsy.py', source)
                configuration = root / 'flimsy.json'
                configuration.write_text(json.dumps({'trigger': 'ctrl', 'timeout': 5, 'data': {}}))
                script = '''
import queue, runpy, sys, time, types
source, configuration, platform, connected = sys.argv[1:]
import json
connected = json.loads(connected)
keyboard = types.ModuleType('keyboard')
thread = types.SimpleNamespace(is_alive=lambda: True)
keyboard._listener = types.SimpleNamespace(listening=True, listening_thread=thread,
                                         processing_thread=thread, queue=queue.Queue())
keyboard._os_keyboard = types.SimpleNamespace(device=types.SimpleNamespace(
    devices=[types.SimpleNamespace(path='event1')]))
keyboard._nixcommon = types.SimpleNamespace(list_devices_from_proc=lambda name:
    [types.SimpleNamespace(path=path) for path in connected])
keyboard.hook = lambda callback: None
sys.modules['keyboard'] = keyboard
sys.modules['pyperclip'] = types.ModuleType('pyperclip')
iterations = iter([None])
def sleep(seconds):
    if next(iterations, True):
        sys.exit(0)
time.sleep = sleep
sys.platform = platform
sys.argv = [source, configuration]
runpy.run_path(source, run_name='__main__')
'''
                result = subprocess.run([sys.executable, '-c', script, str(source), str(configuration),
                                         platform, json.dumps(connected)], capture_output=True, text=True, timeout=5)
                self.assertEqual(expected, result.returncode, result.stderr)
                log = (root / 'flimsy.log').read_text()
                self.assertEqual(expected == 1, 'reason=keyboard devices changed' in log)


if __name__ == '__main__':
    unittest.main()
