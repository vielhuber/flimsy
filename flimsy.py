#!/usr/bin/env python3
import os
import sys

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Avoid slow import probes through the OneDrive reparse directory.
if (
    sys.path
    and os.path.normcase(os.path.abspath(sys.path[0]))
    == os.path.normcase(SCRIPT_DIRECTORY)
):
    sys.path.pop(0)

if sys.platform == 'win32':
    import ctypes

    NORMAL_PRIORITY_CLASS = 0x20
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    kernel32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    kernel32.SetPriorityClass.restype = ctypes.c_int
    process_priority_set = bool(kernel32.SetPriorityClass(
        kernel32.GetCurrentProcess(),
        NORMAL_PRIORITY_CLASS,
    ))
    process_priority_error = None
    if not process_priority_set:
        process_priority_error = ctypes.get_last_error()

import platform

# Python 3.8 may block indefinitely while platform.system() executes "ver".
if sys.platform == 'win32':
    platform.system = lambda: 'Windows'

import keyboard
import pyperclip
from time import sleep, monotonic
import json
import subprocess
import shlex
import logging
import traceback
import atexit
import signal
import faulthandler

LOG_DIRECTORY = SCRIPT_DIRECTORY
if sys.platform == 'win32' and os.environ.get('LOCALAPPDATA'):
    LOG_DIRECTORY = os.path.join(os.environ['LOCALAPPDATA'], 'flimsy')
    try:
        os.makedirs(LOG_DIRECTORY, exist_ok=True)
    except OSError:
        LOG_DIRECTORY = SCRIPT_DIRECTORY
LOG_PATH = os.path.join(LOG_DIRECTORY, 'flimsy.log')
try:
    logging.basicConfig(
        filename=LOG_PATH,
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
except Exception:
    # if we cannot open the log file (permissions etc.), keep going silently
    pass

if sys.platform == 'win32' and process_priority_error is not None:
    logging.warning(
        'failed to set normal process priority: winerror=%d',
        process_priority_error,
    )

shutdown_reason = 'normal shutdown'
fault_log_file = None

try:
    fault_log_file = open(LOG_PATH, 'a', encoding='utf-8')
    faulthandler.enable(file=fault_log_file, all_threads=True)
except Exception:
    fault_log_file = None

def set_shutdown_reason(reason):
    global shutdown_reason
    shutdown_reason = reason

def log_shutdown():
    logging.info('flimsy stopped: %s', shutdown_reason)
    logging.shutdown()
    if faulthandler.is_enabled():
        faulthandler.disable()
    if fault_log_file is not None:
        fault_log_file.close()

atexit.register(log_shutdown)

def log_exception(where):
    # write a full traceback so silent hook-thread deaths become visible
    logging.error('exception in %s: %s', where, traceback.format_exc())

def log_uncaught_exception(exception_type, exception, traceback_value):
    set_shutdown_reason('uncaught exception')
    logging.error(
        'uncaught exception',
        exc_info=(exception_type, exception, traceback_value)
    )
    sys.__excepthook__(exception_type, exception, traceback_value)

sys.excepthook = log_uncaught_exception

def handle_shutdown_signal(signal_number, frame):
    try:
        signal_name = signal.Signals(signal_number).name
    except ValueError:
        signal_name = str(signal_number)
    set_shutdown_reason('signal ' + signal_name)
    logging.info('flimsy received signal %s', signal_name)
    sys.exit(0)

for shutdown_signal in [signal.SIGINT, signal.SIGTERM]:
    signal.signal(shutdown_signal, handle_shutdown_signal)

if hasattr(signal, 'SIGBREAK'):
    signal.signal(signal.SIGBREAK, handle_shutdown_signal)

class Data:
    pass

if len(sys.argv) != 2:
    print('filename missing')
    set_shutdown_reason('startup aborted: filename missing')
    logging.error('startup aborted: filename missing')
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print('file missing')
    set_shutdown_reason('startup aborted: config file missing')
    logging.error('startup aborted: config file %s not found', sys.argv[1])
    sys.exit(1)

with open(sys.argv[1], encoding='utf-8') as config_file:
    config = json.load(config_file)

diagnostics_config = config.get('diagnostics', {})

logging.info(
    'flimsy starting: platform=%s pid=%d python=%s keyboard=%s pyperclip=%s config=%s log=%s',
    platform.system(),
    os.getpid(),
    platform.python_version(),
    getattr(keyboard, 'version', 'unknown'),
    getattr(pyperclip, '__version__', 'unknown'),
    sys.argv[1],
    LOG_PATH,
)

data = Data()
data.events = []
data.timeout = config['timeout']
data.timer = None
data.event_buffer_limit = max(int(diagnostics_config.get('event_buffer_limit', 2048)), 100)
data.slow_handler_seconds = max(float(diagnostics_config.get('slow_handler_seconds', 2)), 0.1)
data.self_heal = diagnostics_config.get('self_heal', True) is True
data.health_check_seconds = max(float(diagnostics_config.get('health_check_seconds', 10)), 1)
data.keyboard_queue_limit = max(int(diagnostics_config.get('keyboard_queue_limit', 512)), 10)

if config['trigger'] == 'ctrl':
    data.triggers = []
    data.triggers.append('ctrl')
    data.triggers.append('right ctrl')
    data.triggers.append('command')
    data.triggers.append('strg')
    data.triggers.append('strg-rechts')
    if platform.system() != 'Windows':
        data.triggers.append('alt gr')
else:
    print('no support for that trigger')
    set_shutdown_reason('startup aborted: unsupported trigger')
    logging.error('startup aborted: unsupported trigger %r', config['trigger'])
    sys.exit(1)

data.replacements = config['data']

if platform.system() == 'Windows':
    data.delay = 0.15
if platform.system() == 'Darwin':
    data.delay = 0.75
if platform.system() == 'Linux':
    data.delay = 1

data.hotkeys = None
data.hotkeys_fired = set()
if 'hotkeys' in config:
    if platform.system() == 'Windows' and 'windows' in config['hotkeys']:
        data.hotkeys = config['hotkeys']['windows']
    if platform.system() == 'Darwin' and 'mac' in config['hotkeys']:
        data.hotkeys = config['hotkeys']['mac']
    if platform.system() == 'Linux' and 'linux' in config['hotkeys']:
        data.hotkeys = config['hotkeys']['linux']

def replaceNow(source, target):
    # print((len(source)+1))
    sleep(0.5*data.delay)
    for x in range(len(source)):
        keyboard.send('backspace')
        sleep(0.01*data.delay)

    autoenter = False
    # only strip the trailing \r; the previous implementation passed rfind() as the
    # replace-count which could wipe \r characters in the middle of the string too
    if target.endswith('\r'):
        target = target[:-1]
        autoenter = True

    # protect the clipboard round-trip: pyperclip can raise on linux/wsl when
    # xclip/xsel is missing or the wayland clipboard is busy, and an unhandled
    # exception here kills the keyboard hook thread until restart
    curClipboard = ''
    try:
        curClipboard = pyperclip.paste()
    except Exception:
        log_exception('replaceNow:pyperclip.paste')
    try:
        pyperclip.copy(target)
    except Exception:
        log_exception('replaceNow:pyperclip.copy')
        return
    sleep(0.5*data.delay)
    # print(platform.system())
    if platform.system() == 'Windows':
        keyboard.send('ctrl+v')
    if platform.system() == 'Darwin':
        keyboard.send('command+v')
    if platform.system() == 'Linux':
        keyboard.send('ctrl+shift+v')
    if autoenter:
        sleep(0.5*data.delay)
        keyboard.send('enter')
    sleep(0.25)
    # restore clipboard
    try:
        pyperclip.copy(curClipboard)
    except Exception:
        log_exception('replaceNow:pyperclip.copy(restore)')

def handler(event):
    # outer try/except ensures a single bad event cannot kill the keyboard
    # listener thread (which made flimsy "stop working until restart")
    started_at = monotonic()
    try:
        _handler_impl(event)
    except Exception:
        log_exception('handler')
    finally:
        duration = monotonic() - started_at
        if duration >= data.slow_handler_seconds:
            logging.warning(
                'slow keyboard handler: duration=%.3fs event=%r buffer=%d',
                duration,
                getattr(event, 'name', None),
                len(data.events),
            )

def _handler_impl(event):
    name = event.name

    if name is None:
        return

    if data.timer and event.time-data.timer > data.timeout:
        data.events = []
        # print('clearing events')
    data.timer = event.time

    if len(data.events) >= data.event_buffer_limit:
        logging.warning(
            'keyboard event buffer reset: limit=%d',
            data.event_buffer_limit,
        )
        data.events = []
        data.timer = None

    data.events.append(event)

    if event.event_type == keyboard.KEY_UP and name not in data.triggers:
        return

    command = ''.join(list(keyboard.get_typed_strings(data.events)))

    if event.name == 'enter':
        data.events = []
        # print('clearing events')

    if event.event_type != keyboard.KEY_UP or name not in data.triggers:
        return

    # on macos " is considered as 2; fix this!
    if platform.system() == 'Darwin' and command.find(' 2') > -1:
        command = command.replace(' 2', ' "')
        command = command.replace('2 ', '" ')
        if command.rfind('2') == (len(command)-1):
            command = command.replace('2', '"', (len(command)-1))

    for data__key, data__value in data.replacements.items():

        identifier = data__key.split(' ')[0]
        pos = command.rfind(identifier)
        cur = pos
        source = data__key.split(' ')
        target = ['']
        inside_quotes = False
        placeholder = {}
        replace = True
        search_command = command[pos:]
        final_command = data__value

        if pos == -1:
            continue

        while(cur < len(command)):
            char = command[cur:cur+1]
            cur += 1
            if char == '"':
                inside_quotes = not inside_quotes
            if char == ' ' and inside_quotes == False:
                target.append('')
                continue
            target[len(target)-1] += char

        # special case: one is allowed to omit quotes when only one placeholder is available
        if len(source) < len(target) and len(source) == 2 and source[1] == '$a':
            new_target = []
            new_target.append(target[0])
            del target[0]
            new_target.append(' '.join(target))
            target = new_target

        if len(source) != len(target):
            continue

        for source__key, source__value in enumerate(source):
            if source__value.find('$') == 0:
                # strip first/last quote
                if target[source__key][0:1] == '"':
                    target[source__key] = target[source__key][1:]
                if target[source__key][-1:] == '"':
                    target[source__key] = target[source__key][0:-1]
                placeholder[source__value] = target[source__key]
            elif source[source__key] != target[source__key]:
                replace = False
                break

        if not replace:
            continue

        for placeholder__key, placeholder__value in placeholder.items():
            final_command = final_command.replace(
                placeholder__key, placeholder__value)

        logging.info('replace match=%r placeholders=%r', data__key, placeholder)
        replaceNow(search_command, final_command)
        data.events = []
        # print('clearing events')
        break


keyboard.hook(handler)
#keyboard.hook(print)

def openProgram(hotkey, command):
    args = []
    if isinstance(command, str):
        args.append(command)
    else:
        args.append(command[0])
        for parameters__value in shlex.split(command[1]):
            args.append(parameters__value)
    # use Popen instead of call so we don't block the keyboard hook thread
    # while the launched program runs; the previous subprocess.call froze
    # all hotkeys for as long as the spawned GUI was alive
    try:
        subprocess.Popen(args, close_fds=True)
        logging.info('launched program %r', args)
    except Exception:
        log_exception('openProgram')
    # bugfix (https://github.com/boppreh/keyboard/issues/301)
    # (not needed in our custom function)
    #keyboard.stash_state()

def customHotkey(event):
    try:
        _custom_hotkey_impl(event)
    except Exception:
        log_exception('customHotkey')

def _custom_hotkey_impl(event):
    if data.hotkeys is None:
        return
    #print(event)
    for hotkeys__key, hotkeys__value in data.hotkeys.items():
        original_key = hotkeys__key
        # fix name for windows hot key
        if 'win+' in hotkeys__key:
            hotkeys__key = hotkeys__key.replace('win+', 'linke windows+')
        pressed = True
        for split__value in hotkeys__key.split('+'):
            if not keyboard.is_pressed(split__value):
                pressed = False
                break

        if pressed:
            # edge-trigger: only fire when the combo transitions from
            # "not-all-pressed" to "all-pressed"
            if original_key in data.hotkeys_fired:
                continue
            data.hotkeys_fired.add(original_key)
            try:
                event.suppress_event = True
            except Exception:
                pass
            logging.info('hotkey fired: %s -> %r', original_key, hotkeys__value)
            print('starting program ', hotkeys__value)
            openProgram(hotkeys__key, hotkeys__value)
            return False
        else:
            data.hotkeys_fired.discard(original_key)

keyboard.hook(customHotkey)

# the following solution is endlessly buggy (we implemented our own instead)
"""
if data.hotkeys != None:
    for hotkeys__key, hotkeys__value in data.hotkeys.items():
        # fix name for windows hot key
        if( 'win+' in hotkeys__key ):
            #keyboard.add_hotkey('linke windows', lambda: None, suppress=True) # suppress windows key in general
            hotkeys__key = hotkeys__key.replace('win+','linke windows+')
        keyboard.add_hotkey(hotkeys__key, openProgram, args=[hotkeys__key, hotkeys__value], timeout=0, suppress=False, trigger_on_release=True)
"""

if data.self_heal:
    logging.info(
        'keyboard self-heal enabled: interval=%.1fs queue_limit=%d',
        data.health_check_seconds,
        data.keyboard_queue_limit,
    )
    while True:
        sleep(data.health_check_seconds)
        restart_reason = None
        queue_size = None

        try:
            listener = getattr(keyboard, '_listener', None)
            listening_thread = getattr(listener, 'listening_thread', None)
            processing_thread = getattr(listener, 'processing_thread', None)
            event_queue = getattr(listener, 'queue', None)

            if listener is None:
                restart_reason = 'keyboard listener missing'
            if listener is not None and not getattr(listener, 'listening', False):
                restart_reason = 'keyboard listener stopped'
            if restart_reason is None and (
                listening_thread is None or not listening_thread.is_alive()
            ):
                restart_reason = 'keyboard listening thread stopped'
            if restart_reason is None and (
                processing_thread is None or not processing_thread.is_alive()
            ):
                restart_reason = 'keyboard processing thread stopped'
            if event_queue is not None:
                queue_size = event_queue.qsize()
            if restart_reason is None and queue_size is None:
                restart_reason = 'keyboard event queue missing'
            if restart_reason is None and queue_size >= data.keyboard_queue_limit:
                restart_reason = 'keyboard event queue blocked'
        except Exception:
            log_exception('keyboard self-heal check')
            continue

        if restart_reason is None:
            continue

        logging.critical(
            'keyboard self-heal restarting flimsy: reason=%s queue=%r',
            restart_reason,
            queue_size,
        )
        for log_handler in logging.getLogger().handlers:
            log_handler.flush()
        if fault_log_file is not None:
            fault_log_file.flush()

        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except OSError:
            log_exception('keyboard self-heal restart')

keyboard.wait()
