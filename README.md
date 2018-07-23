# 🐨 flimsy 🐨

flimsy is a cross-platform text expander for lazy programmers written in python.

it intentionally reveals whats behind your aliases so that you know whats going on.

lets get the party started:

![demo](https://media.giphy.com/media/qPa9vUYCUrx6w/giphy.gif)

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
        "find $a": "find . -type f -name \"$a\" 2>/dev/null",
        "gitp": "git add -A . && git commit -m \".\" && git push origin HEAD",
        "gitp $a": "git add -A . && git commit -m \"$a\" && git push origin HEAD",
        "gitt": "git describe --tags",
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
}
```

## autostart

### linux

```bash
echo "python /path/to/flimsy.py /path/to/flimsy.json &" | sudo tee -a /usr/bin/flimsy-startup.sh
sudo chmod +x /usr/bin/flimsy-startup.sh
echo "ALL ALL = (root) NOPASSWD: /usr/bin/flimsy-startup.sh" | sudo tee -a /etc/sudoers
```

now add ```sudo /usr/bin/flimsy-startup.sh``` in your startup programs of your desktop environment.

### windows

add ```pythonw C:\path\to\flimsy.py C:\path\to\flimsy.json``` to your windows task scheduler.

### mac

```bash
echo "/Library/Frameworks/Python.framework/Versions/3.7/bin/python3 /path/to/flimsy.py /path/to/flimsy.json &" | sudo tee -a /usr/bin/flimsy-startup.sh
sudo chmod +x /usr/bin/flimsy-startup.sh
echo "ALL ALL = (root) NOPASSWD: /usr/bin/flimsy-startup.sh" | sudo tee -a /etc/sudoers
```

now run ```sleep 10; sudo /usr/bin/flimsy-startup.sh``` via [Automator](https://stackoverflow.com/a/6445525/2068362) on every startup.