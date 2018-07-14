# 🐨 flimsy 🐨

flimsy is a cross-platform text expander for lazy programmers written in python.

it intentionally reveals whats behind your aliases so that you know whats going on.

## supports

* windows
* mac
* linux

## features

* easy json configuration file
* enhance your aliases with placeholders
* works in every environment (even on remote ssh sessions)

## installation

install the awesome [keyboard](https://github.com/boppreh/keyboard) and [pyperclip](https://github.com/asweigart/pyperclip) packages with:
```bash
pip install keyboard pyperclip
```

fetch **flimsy.py**:
```bash
wget https://raw.githubusercontent.com/vielhuber/flimsy/master/flimsy.py
```

create **flimsy.json** (put this e.g. inside your dropbox):
```json
{
    "trigger": "ctrl",
    "autoenter": false,
    "timeout": 60,
    "data": {
        "..2": "cd ../../",
        "..3": "cd ../../../",
        "..4": "cd ../../../../",
        "..5": "cd ../../../../../",
        "anim": "transition: all 0.25s ease-in-out;",
        "cfix": "clear:both;\ndisplay:table;\ncontent:\"\"",
        "docroot": "$_SERVER['DOCUMENT_ROOT']",
        "gitr $a $b": "git add -A . && git commit -m \"$a\" && git push origin master && git tag -a \"$b\" -m \"$a\" && git push --tags",
        "gitr $a": "git add -A . && git commit -m \"$a\" && git push origin master",
        "iconc": "©",
        "iconr": "®",
        "lorem": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "ls": "ls -haltr --color=auto",
        "mkdir $a": "mkdir -p \"$a\" && cd \"$a\"",
        "myip": "curl http://ipecho.net/plain",
        "ndash": "–",
        "npm $a $b": "npm --no-git-tag-version version \"$b\" && npm publish && git add -A . && git commit -m \"$a\" && git push origin master && git tag -a \"$b\" -m \"$a\" && git push --tags",
        "please": "sudo !!",
        "plus": "⁺",
        "quote": "&bdquo;&ldquo; „“",
        "ssh customer-xy": "ssh -o TCPKeepAlive=yes -o StrictHostKeyChecking=no -p 22 -l username -i ~/.ssh/id_rsa host -t \"echo 'rm /tmp/initfile; source ~/.bashrc; cd folder; git status' > /tmp/initfile; bash --init-file /tmp/initfile\""
    }
}

```

and throw this inside your autostart:
```bash
python ~/path/to/flimsy.py ~/path/to/flimsy.json &
```

now get the party started:

![demo](https://media.giphy.com/media/qPa9vUYCUrx6w/giphy.gif)