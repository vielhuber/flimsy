import keyboard

class _State(object): pass

def addAbbreviation(word, target):

    replacement = '\b'*(len(word)+1) + target
    callback = lambda: keyboard.write(replacement)

    triggers=['space']
    match_suffix=True,
    timeout=60

    state = _State()
    state.current = ''
    state.time = -1

    def handler(event):

        name = event.name

        if event.event_type == keyboard.KEY_UP or name in keyboard.all_modifiers:
            return

        if timeout and event.time - state.time > timeout:
            state.current = ''

        state.time = event.time

        print(state.current);

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
    '@@': 'ficken'
}

for data__key,data__value in data.items():

    addAbbreviation(data__key,data__value)

keyboard.wait()