#!/usr/bin/env bash

. "$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)/buildscript.sh"

function phase2() {
    runcmd python3 -c "import nltk; nltk.download('punkt')"
    runcmd mkdir -p /home/user/.local/share/Anki2/addons21/bookCrammingModule
}

"$@"
