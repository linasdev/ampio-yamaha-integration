#!/bin/bash
python -m nuitka --follow-imports --standalone --show-progress --show-scons --remove-output ./entry.py
