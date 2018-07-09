# 🐨 flimsy 🐨

flimsy is a cross-platform text expander for lazy programmers.
it intentionally reveal whats behind your aliases so that you know whats going on.

## supports

* windows
* mac
* linux

## features

* easy json configuration file
* enhance your aliases with placeholders
* works in every environment (even on remote ssh sessions)

## installation

install the awesome [keyboard](https://github.com/boppreh/keyboard) package with:
```bash
pip install keyboard
```

fetch **flimsy.py**:
```bash
wget https://raw.githubusercontent.com/vielhuber/flimsy/master/flimsy.py
```

create **aliases.json** (put this e.g. inside your dropbox):
```json
{
    "trigger": "space",
    "autoenter": false,
    "timeout": 60,
    "data": {
        "lorem": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "docroot": "$_SERVER['DOCUMENT_ROOT']",
        "quote": "&bdquo;&ldquo; „“",
        "anim": "transition: all 0.25s ease-in-out;",
        "ndash": "–",
        "plus": "⁺",
        "iconr": "®",
        "iconc": "©",
        "cfix": "clear:both;\ndisplay:table;\ncontent:\"\"",
        "gitr $a": "git add -A . && git commit -m \"$a\" && git push origin master",
        "gitr $a $b": "git add -A . && git commit -m \"$a\" && git push origin master && git tag -a \"$b\" -m \"$a\" && git push --tags",
        "npm $a $b": "npm --no-git-tag-version version \"$b\" && npm publish && git add -A . && git commit -m \"$a\" && git push origin master && git tag -a \"$b\" -m \"$a\" && git push --tags"
    }
}

```

and throw this inside your autostart:
```bash
python ~/path/to/flimsy.py ~/path/to/aliases.json &
```

now get the party started:

![demo](https://media.giphy.com/media/qPa9vUYCUrx6w/giphy.gif)