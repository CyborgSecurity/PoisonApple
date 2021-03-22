#!/usr/bin/env bash

echo "Triggered @ $(date) " >> /Users/$(stat -f "%Su" /dev/console)/Desktop/PoisonApple-$1