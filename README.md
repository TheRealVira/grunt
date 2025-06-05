# grunt

This repository is dedicated to brute-force password guesses for Trench Crusade ARG: https://www.trenchcrusade.com/6d6574616d6f7270686973

## Install

    pip3 install -r requirements.txt

## Run

    python3 grunt.py --help

## Example

Without password generation:

    python3 grunt.py -c YOUR_CRUMB

With password generation:

    python3 grunt.py -g -c YOUR_CRUMB -d YOUR_ID -ch YOUR_CHANNEL_ID

## Crumb

![Crumb](/assets/crumb.png)