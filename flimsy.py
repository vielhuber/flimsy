#!/usr/bin/env python3
import keyboard
import pyperclip
from time import sleep
import platform
import sys
import json
import os
import subprocess
import shlex
import logging
import traceback

# log everything next to flimsy.py so the user always finds it in the repo
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flimsy.log')
try:
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
except Exception:
    # if we cannot open the log file (permissions etc.), keep going silently
    pass

def log_exception(where):
    # write a full traceback so silent hook-thread deaths become visible
    logging.error('exception in %s: %s', where, traceback.format_exc())

class Data:
    pass

if len(sys.argv) != 2:
    print('filename missing')
    logging.error('startup aborted: filename missing')
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print('file missing')
    logging.error('startup aborted: config file %s not found', sys.argv[1])
    sys.exit(1)

with open(sys.argv[1], encoding='utf-8') as config_file:
    config = json.load(config_file)

logging.info('flimsy starting on %s with config %s', platform.system(), sys.argv[1])

data = Data()
data.events = []
data.timeout = config['timeout']
data.timer = None

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
    try:
        _handler_impl(event)
    except Exception:
        log_exception('handler')

def _handler_impl(event):
    name = event.name

    if name is None:
        return

    if data.timer and event.time-data.timer > data.timeout:
        data.events = []
        # print('clearing events')
    data.timer = event.time

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

# remember which hotkey combos are currently in "fired" state so we only
# trigger once per press instead of on every event while keys stay held
data.hotkeys_fired = set()

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

keyboard.wait()
