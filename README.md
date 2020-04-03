# 🐨 flimsy 🐨

> know what's behind your aliases.™

flimsy is a cross-platform text expander for lazy programmers written in python.  
it intentionally reveals whats behind your aliases so that you know whats going on.

## supports

-   windows
-   mac
-   linux

## features

-   easy json configuration file
-   enhance your aliases with placeholders
-   works in every environment (even on remote ssh sessions)
-   also supports defining hotkeys (including suppression) to open programs and scripts

## installation

install the awesome [keyboard](https://github.com/boppreh/keyboard), [pyperclip](https://github.com/asweigart/pyperclip) and [subprocess.run](https://pypi.org/project/subprocess.run/) packages with:

```bash
pip install keyboard pyperclip subprocess.run
```

fetch **flimsy.py**:

```bash
wget https://raw.githubusercontent.com/vielhuber/flimsy/master/flimsy.py
```

create **flimsy.json** (put this e.g. inside your dropbox):

```json
{
    "trigger": "ctrl",
    "timeout": 60,
    "data": {
        "..1": "cd ../../\r",
        "..2": "cd ../../\r",
        "..3": "cd ../../../\r",
        "..4": "cd ../../../../\r",
        "..5": "cd ../../../../../\r",
        "anim": "transition: all 0.25s ease-in-out;",
        "cfix": "clear:both;\ndisplay:table;\ncontent:\"\"",
        "curling": "curl -sD - -o /dev/null https://www.",
        "docroot": "$_SERVER['DOCUMENT_ROOT']",
        "composer": "require_once(__DIR__ . '/vendor/autoload.php');",
        "find $a": "find . -type f -name \"$a\" 2>/dev/null\r",
        "gitu $a $b": "git add -A . && git commit -m \"$a\" && git push origin HEAD && git tag -a \"$b\" -m \"$a\" && git push --tags\r",
        "gitu $a": "git add -A . && git commit -m \"$a\" && git push origin HEAD\r",
        "gitu": "git add -A . && git commit -m \".\" && git push origin HEAD\r",
        "gitut $a": "git add -A . && git commit -m \"$a\" && git push origin HEAD && git tag -a $(v=`git describe --abbrev=0 --tags 2>/dev/null`;n=(${v//./ });n1=${n[0]};n2=${n[1]};n3=${n[2]};if [ -z \"$n1\" ] && [ -z \"$n2\" ] && [ -z \"$n3\" ]; then n1=1; n2=0; n3=0;else n3=$((n3+1)); fi;if [ \"$n3\" == \"10\" ]; then n3=0; n2=$((n2+1)); fi;if [ \"$n2\" == \"10\" ]; then n2=0; n1=$((n1+1)); fi;echo \"$n1.$n2.$n3\") -m \"$a\" && git push --tags\r",
        "gitrm $a": "git rm -rf --cached \"$a\"",
        "gitt": "git describe --tags\r",
        "gits": "git status -sbu\r",
        "git statusall": "find . -type d -name '.git' | while read dir ; do sh -c \"if [ -z \\\"$(cd $dir/../ && git status --porcelain)\\\" ]; then tput setaf 2 && echo \\\"${dir//\\.git/} clean\\\"; else tput setaf 1 && echo \\\"${dir//\\.git/} modified\\\"; fi\" ; done\r",
        "wp updateall": "curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && php wp-cli.phar --allow-root cli cache clear && php wp-cli.phar --allow-root core update && php wp-cli.phar --allow-root core update-db && php wp-cli.phar --allow-root plugin update --all && php wp-cli.phar --allow-root theme update --all && php wp-cli.phar --allow-root language core update && php wp-cli.phar --allow-root language plugin update --all && php wp-cli.phar --allow-root language theme update --all && rm -f wp-cli.phar",
        "nah": "git reset --hard; git clean -df;",
        "gitl": "git log --graph --abbrev-commit --decorate --format=format:\"%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)\" --all\r",
        "gscript": "clasp push --watch\r",
        "lorem": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        "42": "____________/\\\\\\_______/\\\\\\\\\\\\\\\\\\_____________\n___________/\\\\\\\\\\_____/\\\\\\///////\\\\\\__________\n__________/\\\\\\/\\\\\\____\\///______\\//\\\\\\________\n_________/\\\\\\/\\/\\\\\\______________/\\\\\\/________\n________/\\\\\\/__\\/\\\\\\___________/\\\\\\//_________\n_______/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_____/\\\\\\//___________\n_______\\///////////\\\\\\//____/\\\\\\/_____________\n__________________\\/\\\\\\_____/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\__\n___________________\\///_____\\///////////////__",
        "nvm": "nvm use node --lts\r",
        "call": "089215400142",
        "unicorn": "🦄",
        "heart": "❤️",
        "infty": "∞",
        "smile": "😊",
        "thumbs": "👍",
        "ls -h": "ls -haltr --color=auto\r",
        "mkdir $a": "mkdir -p \"$a\" && cd \"$a\"\r",
        "myip": "curl http://ipecho.net/plain; echo\r",
        "ndash": "–",
        "npmu $a $b": "npm --no-git-tag-version version \"$b\" && npm publish && git add -A . && git commit -m \"$a\" && git push origin HEAD && git tag -a \"$b\" -m \"$a\" && git push --tags\r",
        "npmut $a": "npm --no-git-tag-version version $(v=`git describe --abbrev=0 --tags 2>/dev/null`;n=(${v//./ });n1=${n[0]};n2=${n[1]};n3=${n[2]};if [ -z \"$n1\" ] && [ -z \"$n2\" ] && [ -z \"$n3\" ]; then n1=1; n2=0; n3=0;else n3=$((n3+1)); fi;if [ \"$n3\" == \"10\" ]; then n3=0; n2=$((n2+1)); fi;if [ \"$n2\" == \"10\" ]; then n2=0; n1=$((n1+1)); fi;echo \"$n1.$n2.$n3\") && npm publish && git add -A . && git commit -m \"$a\" && git push origin HEAD && git tag -a $(v=`git describe --abbrev=0 --tags 2>/dev/null`;n=(${v//./ });n1=${n[0]};n2=${n[1]};n3=${n[2]};if [ -z \"$n1\" ] && [ -z \"$n2\" ] && [ -z \"$n3\" ]; then n1=1; n2=0; n3=0;else n3=$((n3+1)); fi;if [ \"$n3\" == \"10\" ]; then n3=0; n2=$((n2+1)); fi;if [ \"$n2\" == \"10\" ]; then n2=0; n1=$((n1+1)); fi;echo \"$n1.$n2.$n3\") -m \"$a\" && git push --tags\r",
        "please": "sudo !!\r",
        "gfy": "Thanks for your valuable feedback.",
        "plus": "⁺",
        "quote": "&bdquo;&ldquo; „“",
        "dotdotdot": "&hellip; …",
        "unzip": "unzip file.zip -d .; rm -f file.zip",
        "zip": "zip -r file.zip .",
        "kill $a": "killall -KILL $a",
        "ssh customer-xy": "ssh -o TCPKeepAlive=yes -o StrictHostKeyChecking=no -p 22 -l username -i ~/.ssh/id_rsa host -t \"echo 'rm /tmp/initfile; source ~/.bashrc; cd folder; git status' > /tmp/initfile; bash --init-file /tmp/initfile\"\r",
        "id_rsa": "ssh-rsa AAAAB3NzaC1y...........................................................................................................................................................................................................................................................................................................................................................................................",
        "iconc": "©",
        "iconr": "®",
        "tm": "™",
        "e": "exit\r"
    },
    "hotkeys": {
        "windows": {
            "ctrl+alt+s": "C:\\Users\\David\\AppData\\Roaming\\Spotify\\Spotify.exe",
            "ctrl+alt+c": "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            "win+d": ["script", "-argument1 -argument2"]
        }
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

now add `sudo /usr/bin/flimsy-startup.sh` in your startup programs of your desktop environment.

### windows

add `pythonw C:\path\to\flimsy.py C:\path\to\flimsy.json` to your windows task scheduler.

### mac

```bash
echo "/Library/Frameworks/Python.framework/Versions/3.7/bin/python3 /path/to/flimsy.py /path/to/flimsy.json &" | sudo tee -a /usr/bin/flimsy-startup.sh
sudo chmod +x /usr/bin/flimsy-startup.sh
echo "ALL ALL = (root) NOPASSWD: /usr/bin/flimsy-startup.sh" | sudo tee -a /etc/sudoers
```

now run `sleep 10s; sudo /usr/bin/flimsy-startup.sh &>/dev/null &` via [Automator](https://stackoverflow.com/a/6445525/2068362) on every startup.

### demo

let's get the party started:

![demo](https://raw.githubusercontent.com/vielhuber/flimsy/master/flimsy.gif)
