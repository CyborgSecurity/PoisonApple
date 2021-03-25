#!/usr/bin/env bash

#
# Source: https://github.com/andrewp-as-is/mac-login-items
#

{ set +x; } 2>/dev/null

usage() {
    echo "usage: $(basename $0) path ..." 1>&2
    [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; exit
}

[[ $1 == "-h" ]] || [[ $1 == "--help" ]] && usage "$@"

hidden=false

while [[ $# != 0 ]]; do
    path="$1"
    ! [ -d "$1" ] && {
        [ -d /Applications/"$1" ] && path=/Applications/"$1"
        [ -d /Applications/"$1".app ] && path=/Applications/"$1".app
        [ -d ~/Applications/"$1" ] && path=~/Applications/"$1"
        [ -d ~/Applications/"$1".app ] && path=~/Applications/"$1".app
    }
    ! [ -e "$path" ] && echo "ERROR: $path NOT EXISTS" 1>&2 && exit 1
    osascript <<EOF
tell application "System Events" to make login item at end with properties {path:"$path", hidden:$hidden}
return
EOF
    shift
done;:
