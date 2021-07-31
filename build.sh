#!/bin/bash
python3 -m build
git add -A
git commit -m "Modifica"
git push origin master
