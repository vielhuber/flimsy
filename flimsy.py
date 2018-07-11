import keyboard
from time import sleep

class _State(object): pass

events = []

def addAbbreviation(word, target):

    replacement = target

    def callback():
        for x in range((len(word)+1)):       
            keyboard.send('backspace')
        keyboard.write(replacement, 0, True, True)

    triggers=['right ctrl']
    match_suffix=True,
    timeout=60

    state = _State()
    state.current = ''
    state.time = -1

    def handler(event):

        name = event.name

        events.append(event)

        if event.event_type == keyboard.KEY_UP or name in keyboard.all_modifiers:
            return

        if timeout and event.time - state.time > timeout:
            state.current = ''

        if( name == 'space' ):
            name = ' '        

        state.time = event.time

        print(list(keyboard.get_typed_strings(events)))

        matched = state.current == word or (match_suffix and state.current.endswith(word))

        if name in triggers and matched:
            callback()
            state.current = ''
        elif len(name) > 1:
            state.current = ''
        else:
            state.current += name

    hooked = keyboard.hook(handler)

data = {
    'gitu': 'git add -A .; git commit ""; git push origin master;'
}

for data__key,data__value in data.items():

    addAbbreviation(data__key,data__value)

keyboard.wait()