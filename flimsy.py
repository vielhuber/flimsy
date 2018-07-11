import keyboard
import pyperclip
from time import sleep
import platform

class Data(object): pass

data = Data()
data.events = []
data.timeout = 5
data.timer = None
data.triggers = ['space','right ctrl','ctrl','command','strg-rechts']
data.replacements = {
    'gita': 'git add -A .; git commit ""; git push origin master;',
    'iconr': '®',
    'iconc': '©',
    'cfix': 'clear:both;\ndisplay:table;\ncontent:""'
}

def replace(source, target):
    #print((len(source)+1))
    for x in range(len(source)):       
        keyboard.send('backspace')
        sleep(0.01)
    pyperclip.copy(target)
    sleep(0.5)
    if platform.system() == 'Windows':
        keyboard.send('ctrl+v')
    if platform.system() == 'Darwin':
        keyboard.send('ctrl+v')
    if platform.system() == 'Linux':
        keyboard.send('ctrl+shift+v')

def handler(event):

    global data;

    name = event.name

    if data.timer and event.time-data.timer > data.timeout:
        data.events = []
        print('clearing events')
    data.timer = event.time

    data.events.append(event)

    if event.event_type == keyboard.KEY_UP and name not in data.triggers:
        return
    if name in keyboard.all_modifiers:
        return

    #print(list(keyboard.get_typed_strings(data.events)))
    string = ''.join(list(keyboard.get_typed_strings(data.events)))
    print(string)
    #print(name)

    if event.event_type != keyboard.KEY_UP or name not in data.triggers:
        return

    for data__key,data__value in data.replacements.items():

        if string.endswith(data__key):
            replace(data__key,data__value)
            data.events = []
            print('clearing events')

keyboard.hook(handler)

keyboard.wait()
