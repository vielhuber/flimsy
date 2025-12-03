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
        "cd $a": "{ cd /var/www/$a/wp-content/themes/$a; } || { cd /var/www/$a/wp-content/themes && ls; } || { cd /var/www/$a && ls; }\r",
        "anim": "transition: all 0.25s ease-in-out;",
        "audit": "for d in ./*/; do n=$(basename \"$d\"); [ \"$n\" = \"_archive\" ] && continue; npm_ok=0; comp_ok=0; if [ -f \"$d/package.json\" ]; then (cd \"$d\" && npm audit >/dev/null 2>&1) || npm_ok=1; elif [ -f \"$d/wp-content/themes/$n/package.json\" ]; then (cd \"$d/wp-content/themes/$n\" && npm audit >/dev/null 2>&1) || npm_ok=1; fi; if [ -f \"$d/composer.json\" ]; then (cd \"$d\" && composer audit >/dev/null 2>&1) || comp_ok=1; elif [ -f \"$d/wp-content/themes/$n/composer.json\" ]; then (cd \"$d/wp-content/themes/$n\" && composer audit >/dev/null 2>&1) || comp_ok=1; fi; if [ \"$npm_ok\" -eq 0 ] && [ \"$comp_ok\" -eq 0 ]; then echo \"✅ $n\"; else echo \"⛔ $n\"; fi; done\r",
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
        "gitt $a": "git tag -a \"$a\" -m \"\" && git push --tags",
        "gitt": "git describe --tags\r",
        "gits": "git status -sbu\r",
        "gitb $a": "git checkout -b $a && git push --set-upstream origin $a",
        "git stash": "git stash -u; git stash pop",
        "git squash $a": "git merge \"$a\" && git push origin HEAD && git reset --soft \"$a\" && git add -A . && git commit -m \"squash\" && git pull --no-ff && git push origin HEAD",
        "git statusall": "{ printf '\n🟢: clean\n🟡: behind/ahead\n🔴: modified\n\n----------------------------------\n\n'; find . -path './_archive' -prune -o -type d -name .git -print0 | sort -z | while IFS= read -r -d '' d; do r=${d%/.git}; r=${r#./}; s=$(git -C \"$r\" status --porcelain); a=0; b=0; if git -C \"$r\" rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then timeout 10s git -C \"$r\" fetch --all --prune >/dev/null 2>&1 || true; a=$(git -C \"$r\" rev-list --count --left-only HEAD...@{u}); b=$(git -C \"$r\" rev-list --count --right-only HEAD...@{u}); fi; if [ -n \"$s\" ]; then emoji=\"🔴\"; elif [ \"$a\" -gt 0 ] || [ \"$b\" -gt 0 ]; then emoji=\"🟡\"; else emoji=\"🟢\"; fi; printf '%s %s\n' \"$emoji\" \"$r\"; done; }\r",
        "git clean": "git clean -df;\r",
        "wp updateall": "curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && php wp-cli.phar --allow-root cli cache clear && php wp-cli.phar --allow-root core update && php wp-cli.phar --allow-root core update-db && php wp-cli.phar --allow-root plugin update --all && php wp-cli.phar --allow-root theme update --all && php wp-cli.phar --allow-root language core update && php wp-cli.phar --allow-root language plugin update --all && php wp-cli.phar --allow-root language theme update --all && rm -f wp-cli.phar",
        "nah": "git reset --hard; git clean -df;",
        "gitl": "git log --graph --abbrev-commit --decorate --format=format:\"%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)\" --all\r",
        "gscript": "clasp push --watch\r",
        "lorem": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.",
        "lorem2": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.\nAenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante.",
        "lorem3": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.\nAenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante.\nEtiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu.",
        "lorem4": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.\nAenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante.\nEtiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu.\nDuis arcu tortor, suscipit eget, imperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestibulum volutpat pretium libero. Cras id dui. Aenean ut eros et nisl sagittis vestibulum. Nullam nulla eros, ultricies sit amet, nonummy id, imperdiet feugiat, pede. Sed lectus. Donec mollis hendrerit risus. Phasellus nec sem in justo pellentesque facilisis. Etiam imperdiet imperdiet orci. Nunc nec neque.",
        "lorem5": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.\nAenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante.\nEtiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu.\nDuis arcu tortor, suscipit eget, imperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestibulum volutpat pretium libero. Cras id dui. Aenean ut eros et nisl sagittis vestibulum. Nullam nulla eros, ultricies sit amet, nonummy id, imperdiet feugiat, pede. Sed lectus. Donec mollis hendrerit risus. Phasellus nec sem in justo pellentesque facilisis. Etiam imperdiet imperdiet orci. Nunc nec neque.\nPhasellus leo dolor, tempus non, auctor et, hendrerit quis, nisi. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo. Maecenas malesuada. Praesent congue erat at massa. Sed cursus turpis vitae tortor. Donec posuere vulputate arcu. Phasellus accumsan cursus velit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Sed aliquam, nisi quis porttitor congue, elit erat euismod orci, ac placerat dolor lectus quis orci. Phasellus consectetuer vestibulum elit. Aenean tellus metus, bibendum sed, posuere ac, mattis non, nunc.",
        "loremg": "Es gibt im Moment in diese Mannschaft, oh, einige Spieler vergessen ihnen Profi was sie sind. Ich lese nicht sehr viele Zeitungen, aber ich habe gehört viele Situationen. Erstens: wir haben nicht offensiv gespielt. Es gibt keine deutsche Mannschaft spielt offensiv und die Name offensiv wie Bayern. Letzte Spiel hatten wir in Platz drei Spitzen: Elber, Jancka und dann Zickler. Wir müssen nicht vergessen Zickler. Zickler ist eine Spitzen mehr, Mehmet eh mehr Basler. Ist klar diese Wörter, ist möglich verstehen, was ich hab gesagt? Danke.",
        "loremg2": "Es gibt im Moment in diese Mannschaft, oh, einige Spieler vergessen ihnen Profi was sie sind. Ich lese nicht sehr viele Zeitungen, aber ich habe gehört viele Situationen. Erstens: wir haben nicht offensiv gespielt. Es gibt keine deutsche Mannschaft spielt offensiv und die Name offensiv wie Bayern. Letzte Spiel hatten wir in Platz drei Spitzen: Elber, Jancka und dann Zickler. Wir müssen nicht vergessen Zickler. Zickler ist eine Spitzen mehr, Mehmet eh mehr Basler. Ist klar diese Wörter, ist möglich verstehen, was ich hab gesagt? Danke.\nOffensiv, offensiv ist wie machen wir in Platz. Zweitens: ich habe erklärt mit diese zwei Spieler: nach Dortmund brauchen vielleicht Halbzeit Pause. Ich habe auch andere Mannschaften gesehen in Europa nach diese Mittwoch. Ich habe gesehen auch zwei Tage die Training. Ein Trainer ist nicht ein Idiot! Ein Trainer sei sehen was passieren in Platz. In diese Spiel es waren zwei, drei diese Spieler waren schwach wie eine Flasche leer! Haben Sie gesehen Mittwoch, welche Mannschaft hat gespielt Mittwoch?",
        "loremg3": "Es gibt im Moment in diese Mannschaft, oh, einige Spieler vergessen ihnen Profi was sie sind. Ich lese nicht sehr viele Zeitungen, aber ich habe gehört viele Situationen. Erstens: wir haben nicht offensiv gespielt. Es gibt keine deutsche Mannschaft spielt offensiv und die Name offensiv wie Bayern. Letzte Spiel hatten wir in Platz drei Spitzen: Elber, Jancka und dann Zickler. Wir müssen nicht vergessen Zickler. Zickler ist eine Spitzen mehr, Mehmet eh mehr Basler. Ist klar diese Wörter, ist möglich verstehen, was ich hab gesagt? Danke.\nOffensiv, offensiv ist wie machen wir in Platz. Zweitens: ich habe erklärt mit diese zwei Spieler: nach Dortmund brauchen vielleicht Halbzeit Pause. Ich habe auch andere Mannschaften gesehen in Europa nach diese Mittwoch. Ich habe gesehen auch zwei Tage die Training. Ein Trainer ist nicht ein Idiot! Ein Trainer sei sehen was passieren in Platz. In diese Spiel es waren zwei, drei diese Spieler waren schwach wie eine Flasche leer! Haben Sie gesehen Mittwoch, welche Mannschaft hat gespielt Mittwoch?\nHat gespielt Mehmet oder gespielt Basler oder hat gespielt Trapattoni? Diese Spieler beklagen mehr als sie spielen! Wissen Sie, warum die Italienmannschaften kaufen nicht diese Spieler? Weil wir haben gesehen viele Male solche Spiel! Haben gesagt sind nicht Spieler für die italienisch Meisters! Strunz! Strunz ist zwei Jahre hier, hat gespielt 10 Spiele, ist immer verletzt! Was erlauben Strunz? Letzte Jahre Meister Geworden mit Hamann, eh, Nerlinger. Diese Spieler waren Spieler! Waren Meister geworden! Ist immer verletzt!",
        "loremg4": "Es gibt im Moment in diese Mannschaft, oh, einige Spieler vergessen ihnen Profi was sie sind. Ich lese nicht sehr viele Zeitungen, aber ich habe gehört viele Situationen. Erstens: wir haben nicht offensiv gespielt. Es gibt keine deutsche Mannschaft spielt offensiv und die Name offensiv wie Bayern. Letzte Spiel hatten wir in Platz drei Spitzen: Elber, Jancka und dann Zickler. Wir müssen nicht vergessen Zickler. Zickler ist eine Spitzen mehr, Mehmet eh mehr Basler. Ist klar diese Wörter, ist möglich verstehen, was ich hab gesagt? Danke.\nOffensiv, offensiv ist wie machen wir in Platz. Zweitens: ich habe erklärt mit diese zwei Spieler: nach Dortmund brauchen vielleicht Halbzeit Pause. Ich habe auch andere Mannschaften gesehen in Europa nach diese Mittwoch. Ich habe gesehen auch zwei Tage die Training. Ein Trainer ist nicht ein Idiot! Ein Trainer sei sehen was passieren in Platz. In diese Spiel es waren zwei, drei diese Spieler waren schwach wie eine Flasche leer! Haben Sie gesehen Mittwoch, welche Mannschaft hat gespielt Mittwoch?\nHat gespielt Mehmet oder gespielt Basler oder hat gespielt Trapattoni? Diese Spieler beklagen mehr als sie spielen! Wissen Sie, warum die Italienmannschaften kaufen nicht diese Spieler? Weil wir haben gesehen viele Male solche Spiel! Haben gesagt sind nicht Spieler für die italienisch Meisters! Strunz! Strunz ist zwei Jahre hier, hat gespielt 10 Spiele, ist immer verletzt! Was erlauben Strunz? Letzte Jahre Meister Geworden mit Hamann, eh, Nerlinger. Diese Spieler waren Spieler! Waren Meister geworden! Ist immer verletzt!\nHat gespielt 25 Spiele in diese Mannschaft in diese Verein. Muß respektieren die andere Kollegen! haben viel nette kollegen! Stellen Sie die Kollegen die Frage! Haben keine Mut an Worten, aber ich weiß, was denken über diese Spieler. Mussen zeigen jetzt, ich will, Samstag, diese Spieler müssen zeigen mich, seine Fans, müssen alleine die Spiel gewinnen. Muß allein die Spiel gewinnen! Ich bin müde jetzt Vater diese Spieler, eh der Verteidiger diese Spieler. Ich habe immer die Schuld über diese Spieler. Einer ist Mario, einer andere ist Mehmet!",
        "loremg5": "Es gibt im Moment in diese Mannschaft, oh, einige Spieler vergessen ihnen Profi was sie sind. Ich lese nicht sehr viele Zeitungen, aber ich habe gehört viele Situationen. Erstens: wir haben nicht offensiv gespielt. Es gibt keine deutsche Mannschaft spielt offensiv und die Name offensiv wie Bayern. Letzte Spiel hatten wir in Platz drei Spitzen: Elber, Jancka und dann Zickler. Wir müssen nicht vergessen Zickler. Zickler ist eine Spitzen mehr, Mehmet eh mehr Basler. Ist klar diese Wörter, ist möglich verstehen, was ich hab gesagt? Danke.\nOffensiv, offensiv ist wie machen wir in Platz. Zweitens: ich habe erklärt mit diese zwei Spieler: nach Dortmund brauchen vielleicht Halbzeit Pause. Ich habe auch andere Mannschaften gesehen in Europa nach diese Mittwoch. Ich habe gesehen auch zwei Tage die Training. Ein Trainer ist nicht ein Idiot! Ein Trainer sei sehen was passieren in Platz. In diese Spiel es waren zwei, drei diese Spieler waren schwach wie eine Flasche leer! Haben Sie gesehen Mittwoch, welche Mannschaft hat gespielt Mittwoch?\nHat gespielt Mehmet oder gespielt Basler oder hat gespielt Trapattoni? Diese Spieler beklagen mehr als sie spielen! Wissen Sie, warum die Italienmannschaften kaufen nicht diese Spieler? Weil wir haben gesehen viele Male solche Spiel! Haben gesagt sind nicht Spieler für die italienisch Meisters! Strunz! Strunz ist zwei Jahre hier, hat gespielt 10 Spiele, ist immer verletzt! Was erlauben Strunz? Letzte Jahre Meister Geworden mit Hamann, eh, Nerlinger. Diese Spieler waren Spieler! Waren Meister geworden! Ist immer verletzt!\nHat gespielt 25 Spiele in diese Mannschaft in diese Verein. Muß respektieren die andere Kollegen! haben viel nette kollegen! Stellen Sie die Kollegen die Frage! Haben keine Mut an Worten, aber ich weiß, was denken über diese Spieler. Mussen zeigen jetzt, ich will, Samstag, diese Spieler müssen zeigen mich, seine Fans, müssen alleine die Spiel gewinnen. Muß allein die Spiel gewinnen! Ich bin müde jetzt Vater diese Spieler, eh der Verteidiger diese Spieler. Ich habe immer die Schuld über diese Spieler. Einer ist Mario, einer andere ist Mehmet!\nStrunz ich spreche nicht, hat gespielt nur 25 Prozent der Spiel. Ich habe fertig! Es gibt im Moment in diese Mannschaft, oh, einige Spieler vergessen ihnen Profi was sie sind. Ich lese nicht sehr viele Zeitungen, aber ich habe gehört viele Situationen. Erstens: wir haben nicht offensiv gespielt. Es gibt keine deutsche Mannschaft spielt offensiv und die Name offensiv wie Bayern. Letzte Spiel hatten wir in Platz drei Spitzen: Elber, Jancka und dann Zickler. Wir müssen nicht vergessen Zickler. Zickler ist eine Spitzen mehr, Mehmet eh mehr Basler.",
        "check": "✅",
        "warn": "⚠️",
        "work": "⚠️",
        "stop": "⛔",
        "what": "❓",
        "100": "💯",
        "plz": "🙏🏻",
        "green": "🟢",
        "yellow": "🟡",
        "red": "🔴",
        "boilerplate": "<!DOCTYPE html>\n<html lang=\"de\">\n<head>\n    <meta charset=\"utf-8\" />\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=5, minimum-scale=1\" />\n    <title>.</title>\n    <link rel=\"stylesheet\" href=\"style.css\" />\n    <script src=\"script.js\"></script> \n    <script>\n    \n    </script>\n    <style>\n    *\n    {\n        box-sizing: border-box;\n        margin: 0;\n        padding: 0;\n    }\n    </style>\n</head>\n<body>\n\n</body>\n</html>",
        "42": "____________/\\\\\\_______/\\\\\\\\\\\\\\\\\\_____________\n___________/\\\\\\\\\\_____/\\\\\\///////\\\\\\__________\n__________/\\\\\\/\\\\\\____\\///______\\//\\\\\\________\n_________/\\\\\\/\\/\\\\\\______________/\\\\\\/________\n________/\\\\\\/__\\/\\\\\\___________/\\\\\\//_________\n_______/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_____/\\\\\\//___________\n_______\\///////////\\\\\\//____/\\\\\\/_____________\n__________________\\/\\\\\\_____/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\__\n___________________\\///_____\\///////////////__",
        "nvm": "nvm use node --lts\r",
        "call": "099123456789",
        "ustid": "DE 000 000 000",
        "cls": "cd /var/www && clear\r",
        "unicorn": "🦄",
        "heart": "❤️",
        "alert": "❗",
        "wait": "⏳",
        "sun": "☀️",
        "star": "⭐",
        "infty": "∞",
        "info": "ℹ️",
        "smile": "😊",
        "rocket": "🚀",
        "thumbs": "👍",
        "luck": "🍀",
        "coffee": "☕",
        "nbsp": " ",
        "ls -h": "ls -haltr --color=auto\r",
        "cp $a $b": "rsync -ah --progress $a $b",
        "mkdir $a": "mkdir -p \"$a\" && cd \"$a\"\r",
        "myip": "curl http://ipecho.net/plain; echo\r",
        "speedtest $a": "curl -s -w 'Testing Website Response Time for :%{url_effective}\\n\\nLookup Time:\\t\\t%{time_namelookup}\\nConnect Time:\\t\\t%{time_connect}\\nAppCon Time:\\t\\t%{time_appconnect}\\nRedirect Time:\\t\\t%{time_redirect}\\nPre-transfer Time:\\t%{time_pretransfer}\\nStart-transfer Time:\\t%{time_starttransfer}\\n\\nTotal Time:\\t\\t%{time_total}\\n' -o /dev/null $a\r",
        "sitemap": "curl -N -s https://tld.com/sitemap_index.xml | grep -oP '<loc>\\K[^<]*' | xargs -n1 curl -N -s | grep -oP '<loc>\\K[^<]*' > urls.txt",
        "ndash": "–",
        "comment": "\/**\n  * This\n  * is a multiline\n  * comment.\n  *\/\n",
        "npmu $a $b": "npm --no-git-tag-version version \"$b\" && npm publish && git add -A . && git commit -m \"$a\" && git push origin HEAD && git tag -a \"$b\" -m \"$a\" && git push --tags\r",
        "npmut $a": "if grep -q \"prod\" package.json; then npm run prod; fi; npm --no-git-tag-version version $(v=`git describe --abbrev=0 --tags 2>/dev/null`;n=(${v//./ });n1=${n[0]};n2=${n[1]};n3=${n[2]};if [ -z \"$n1\" ] && [ -z \"$n2\" ] && [ -z \"$n3\" ]; then n1=1; n2=0; n3=0;else n3=$((n3+1)); fi;if [ \"$n3\" == \"10\" ]; then n3=0; n2=$((n2+1)); fi;if [ \"$n2\" == \"10\" ]; then n2=0; n1=$((n1+1)); fi;echo \"$n1.$n2.$n3\") && npm publish && git add -A . && git commit -m \"$a\" && git push origin HEAD; if grep -q \"update-changelog\" package.json; then npm run update-changelog && git add -A . && git commit -m \"Update changelog.\" && git push origin HEAD; fi; git tag -a $(v=`git describe --abbrev=0 --tags 2>/dev/null`;n=(${v//./ });n1=${n[0]};n2=${n[1]};n3=${n[2]};if [ -z \"$n1\" ] && [ -z \"$n2\" ] && [ -z \"$n3\" ]; then n1=1; n2=0; n3=0;else n3=$((n3+1)); fi;if [ \"$n3\" == \"10\" ]; then n3=0; n2=$((n2+1)); fi;if [ \"$n2\" == \"10\" ]; then n2=0; n1=$((n1+1)); fi;echo \"$n1.$n2.$n3\") -m \"$a\" && git push --tags\r",
        "phpv $a": "sudo update-alternatives --set php /usr/bin/php$a\r",
        "migr": "php artisan migrate --path=/database/migrations/post/20XX-XX-XX/",
        "migrate": "php artisan migrate:fresh --seed\r",
        "please": "sudo !!\r",
        "gfy": "Thanks for your valuable feedback.",
        "plus": "⁺",
        "quote": "&bdquo;&ldquo; „“",
        "dotdotdot": "&hellip; …",
        "unzip": "unzip file.zip -d .; rm -f file.zip",
        "zip": "zip -r file.zip .",
        "df": "du -d 1 -xh . 2>/dev/null | sort -h -r | head -10\r",
        "kill $a": "killall -KILL $a",
        "wpscan": "wpscan --random-user-agent --disable-tls-checks --api-token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --ignore-main-redirect --url https://www.domain.tld | grep '[!]'",
        "ssh host.tld": "ssh -o UserKnownHostsFile=/dev/null -o TCPKeepAlive=yes -o StrictHostKeyChecking=no -p 22 -l username -i ~/.ssh/id_rsa host.tld -t \"echo 'rm /tmp/initfile; source ~/.bashrc; cd folder; git status' > /tmp/initfile; bash --init-file /tmp/initfile\"\r",
        "ssh host-that-does-not-support-public-keys.tld": "sshpass -p 'XXXXXXXXXXXX' ssh -o UserKnownHostsFile=/dev/null -o TCPKeepAlive=yes -o StrictHostKeyChecking=no -p 22 -l username -i ~/.ssh/id_rsa host.tld -t \"echo 'rm /tmp/initfile; source ~/.bashrc; cd folder; git status' > /tmp/initfile; bash --init-file /tmp/initfile\"\r",
        "sql host.tld": "ssh -o -UserKnownHostsFile=/dev/null -o TCPKeepAlive=yes -o StrictHostKeyChecking=no -TNL 5001:/var/lib/mysql/mysql.sock username@host.tld\r",
        "id_rsa": "ssh-rsa AAAAB3NzaC1y...........................................................................................................................................................................................................................................................................................................................................................................................",
        "sshcopy": "cat ~/.ssh/id_rsa.pub | xclip\r",
        "iconc": "©",
        "iconr": "®",
        "tm": "™",
        "e": "exit\r"
    },
    "hotkeys": {
        "windows": {
            "ctrl+shift+s": "C:\\Users\\David\\AppData\\Roaming\\Spotify\\Spotify.exe",
            "ctrl+shift+c": "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            "f1": ["script", "-argument1 -argument2"],
            "win+d": ["script", "-argument1 -argument2"]
        }
    }
}
```

## update

fetch **flimsy.py**:

```bash
wget -O flimsy.py https://raw.githubusercontent.com/vielhuber/flimsy/master/flimsy.py
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
