import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class GitVersionTest(unittest.TestCase):
    def test_version_exceeds_all_tags_and_the_package_version(self):
        readme = (Path(__file__).parents[1] / 'README.md').read_text()
        snippets = [json.loads('{' + line.strip().rstrip(',') + '}') for line in readme.splitlines()
                    if line.strip().startswith(('"gitut":', '"gitut $a":'))]
        self.assertEqual(2, len(snippets))
        for snippet in snippets:
            name, command = next(iter(snippet.items()))
            calculation = command.split('version=$(', 1)[1].split(') && if [ -f package.json ]', 1)[0]
            for tags, reachable, package, expected in (
                ('1.1.3\n1.1.4', '1.1.3', '1.1.4', '1.1.5'),
                ('1.1.3', '1.1.3', '1.1.4', '1.1.5'),
                ('1.2.0\n1.1.3', '1.1.3', '1.1.4', '1.2.1'),
                ('v1.2.3', 'v1.2.3', '1.1.4', '1.2.4'),
                ('1.1.9', '1.1.9', '1.1.9', '1.2.0'),
                ('1.9.9', '1.9.9', '1.9.9', '2.0.0'),
                ('', '', '1.0.9', '1.1.0'),
                ('', '', None, '1.0.0'),
            ):
                with self.subTest(snippet=name, tags=tags, package=package), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    binary = root / 'bin'
                    binary.mkdir()
                    git = binary / 'git'
                    git.write_text('#!/bin/sh\nif [ "$1" = tag ]; then printf "%s\\n" "$TEST_TAGS"; else printf "%s\\n" "$TEST_REACHABLE"; fi\n')
                    git.chmod(0o755)
                    if package is not None:
                        (root / 'package.json').write_text(json.dumps({'version': package}))
                    environment = dict(os.environ, PATH=f'{binary}:/usr/bin:/bin',
                                       TEST_TAGS=tags, TEST_REACHABLE=reachable)
                    result = subprocess.run(['bash', '-c', calculation], cwd=root, env=environment,
                                            capture_output=True, text=True, timeout=5)
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertEqual(expected, result.stdout.strip())


if __name__ == '__main__':
    unittest.main()
