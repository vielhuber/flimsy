import keyboard
import pyperclip
from time import sleep
import platform
import sys
import json
from pprint import pprint
import os.path
import subprocess
import shlex

class Data(object):
    pass

if len(sys.argv) != 2:
    print('filename missing')
    sys.exit()

if not os.path.isfile(sys.argv[1]):
    print('file missing')
    sys.exit()

with open(sys.argv[1], encoding='utf-8') as config_file:
    config = json.load(config_file)

data = Data()
data.events = []
data.timeout = config['timeout']
data.timer = None

if config['trigger'] == 'ctrl':
    data.triggers = ['right ctrl', 'ctrl', 'command', 'strg-rechts']
else:
    print('no support for that trigger')
    sys.exit()

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
    if target.rfind('\r') == len(target)-1:
        target = target.replace('\r', '', target.rfind('\r'))
        autoenter = True

    curClipboard = pyperclip.paste()
    pyperclip.copy(target)
    sleep(0.5*data.delay)
    # print(platform.system())
    if platform.system() == 'Windows':
        keyboard.send('ctrl+v')
    if platform.system() == 'Darwin':
        keyboard.send('command+v')
    if platform.system() == 'Linux':
        keyboard.send('ctrl+shift+v')
    if(autoenter == True):
        sleep(0.5*data.delay)
        keyboard.send('enter')
    sleep(1)
    pyperclip.copy(curClipboard)


def handler(event):

    global data

    name = event.name

    if name is None:
        return;

    if data.timer and event.time-data.timer > data.timeout:
        data.events = []
        # print('clearing events')
    data.timer = event.time

    data.events.append(event)

    if event.event_type == keyboard.KEY_UP and name not in data.triggers:
        return

    command = ''.join(list(keyboard.get_typed_strings(data.events)))

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

        if replace == False:
            continue

        for placeholder__key, placeholder__value in placeholder.items():
            final_command = final_command.replace(
                placeholder__key, placeholder__value)

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
    subprocess.call(args)
    # bugfix (https://github.com/boppreh/keyboard/issues/301)
    keyboard.stash_state()

if data.hotkeys != None:
    for hotkeys__key, hotkeys__value in data.hotkeys.items():
        # fix name for windows hot key
        if( 'win+' in hotkeys__key ):
            keyboard.add_hotkey('linke windows', lambda: None, suppress=True) # suppress windows key in general
            hotkeys__key = hotkeys__key.replace('win+','linke windows+')
        keyboard.add_hotkey(hotkeys__key, openProgram, args=[hotkeys__key, hotkeys__value], timeout=2, suppress=True, trigger_on_release=True)

keyboard.wait()
