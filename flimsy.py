import keyboard
import pyperclip
from time import sleep
import platform

class Data(object): pass

data = Data()
data.events = []
data.timeout = 5
data.timer = None
data.triggers = ['right ctrl','ctrl','command','strg-rechts']
data.replacements = {
    "..2": "cd ../../",
    "..3": "cd ../../../",
    "..4": "cd ../../../../",
    "..5": "cd ../../../../../",
    "anim": "transition: all 0.25s ease-in-out;",
    "cfix": "clear:both;\ndisplay:table;\ncontent:\"\"",
    "docroot": "$_SERVER['DOCUMENT_ROOT']",
    "iconc": "©",
    "iconr": "®",
    "lorem": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
    "ls": "ls -haltr --color=auto",
    "myip": "curl http://ipecho.net/plain",
    "ndash": "–",
    "please": "sudo !!",
    "plus": "⁺",
    "quote": "&bdquo;&ldquo; „“"
}

def replace(source, target):
    #print((len(source)+1))
    sleep(0.5)
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
        #print('clearing events')
    data.timer = event.time

    data.events.append(event)

    if event.event_type == keyboard.KEY_UP and name not in data.triggers:
        return
    if name in keyboard.all_modifiers:
        return
   
    string = ''.join(list(keyboard.get_typed_strings(data.events)))
    #print(list(keyboard.get_typed_strings(data.events)))
    #print(string)
    #print(name)
    #print(name)

    if event.event_type != keyboard.KEY_UP or name not in data.triggers:
        return

    for data__key,data__value in data.replacements.items():

        if string.endswith(data__key):
            replace(data__key,data__value)
            data.events = []
            #print('clearing events')

keyboard.hook(handler)

keyboard.wait()
