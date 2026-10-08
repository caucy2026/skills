#!/usr/bin/env python3
"""Entry to maintained project controls; no duplicated implementation."""
import os
from pathlib import Path
import sys
root=Path(os.environ.get('SWDOL_PROJECT_ROOT','/Users/kemi/coding/swdol2026'))
if len(sys.argv)<2 or sys.argv[1] not in ('prepare','relogin','magic'):
    raise SystemExit('usage: control.py prepare | relogin [args] | magic [args]')
mode=sys.argv[1]
script=root/'tools/xp-original-control'/('magic_sequence.py' if mode=='magic' else 'session.py')
if not script.is_file():raise SystemExit('maintained script missing: '+str(script))
args=sys.argv[2:] if mode=='magic' else [mode]+sys.argv[2:]
os.execv(sys.executable,[sys.executable,str(script),*args])
