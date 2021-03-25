#!/usr/bin/env bash

#
# Source: https://github.com/andrewp-as-is/mac-login-items
#

{ set +x; } 2>/dev/null

usage() {
    echo "usage: $(basename $0)" 1>&2
    [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; exit
}

[[ $1 == "-h" ]] || [[ $1 == "--help" ]] && usage "$@"

[[ $# == 0 ]] && usage

while [[ $# != 0 ]]; do
    osascript <<EOF
tell application "System Events" to delete login item "$1"
EOF
    shift
done;:
