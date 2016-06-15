#!/bin/bash
brew cleanup -s
rm -fr $(brew --cache)
