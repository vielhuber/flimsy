import keyboard
import pyperclip
from time import sleep
import platform
import sys

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
    "gitp": "git add -A . && git commit -m \".\" && git push origin HEAD",
    "gitp $a": "git add -A . && git commit -m \"$a\" && git push origin HEAD",
    "gitt $a $b": "git add -A . && git commit -m \"$a\" && git push origin HEAD && git tag -a \"$b\" -m \"$a\" && git push --tags",
    "iconc": "©",
    "iconr": "®",
    "lorem": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
    "ls": "ls -haltr --color=auto",
    "mkdir $a": "mkdir -p \"$a\" && cd \"$a\"",
    "myip": "curl http://ipecho.net/plain",
    "ndash": "–",
    "npm $a $b": "npm --no-git-tag-version version \"$b\" && npm publish && git add -A . && git commit -m \"$a\" && git push origin HEAD && git tag -a \"$b\" -m \"$a\" && git push --tags",
    "please": "sudo !!",
    "plus": "⁺",
    "quote": "&bdquo;&ldquo; „“",
    "ssh customer-xy": "ssh -o TCPKeepAlive=yes -o StrictHostKeyChecking=no -p 22 -l username -i ~/.ssh/id_rsa host -t \"echo 'rm /tmp/initfile; source ~/.bashrc; cd folder; git status' > /tmp/initfile; bash --init-file /tmp/initfile\""
}

def replaceNow(source, target):
    #print((len(source)+1))
    sleep(0.5)
    for x in range(len(source)):       
        keyboard.send('backspace')
        sleep(0.01)
    pyperclip.copy(target)
    sleep(0.5)
    #print(platform.system())
    if platform.system() == 'Windows':
        keyboard.send('ctrl+v')
    if platform.system() == 'Darwin':
        keyboard.send('command+v')
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
   
    command = ''.join(list(keyboard.get_typed_strings(data.events)))

    if event.event_type != keyboard.KEY_UP or name not in data.triggers:
        return

    for data__key,data__value in data.replacements.items():

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
        if len(source) != len(target) and len(source) == 2 and source[1] == '$a':
            new_target = []
            new_target.append(target[0])
            del target[0]
            new_target.append(' '.join(target))
            target = new_target

        if len(source) != len(target):        
            continue

        for source__key,source__value in enumerate(source):
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

        for placeholder__key,placeholder__value in placeholder.items():        
            final_command = final_command.replace(placeholder__key, placeholder__value);

        replaceNow(search_command,final_command)
        data.events = []
        #print('clearing events')
        break;

keyboard.hook(handler)

keyboard.wait()
