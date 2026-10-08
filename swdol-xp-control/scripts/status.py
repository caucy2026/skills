#!/usr/bin/env python3
"""Read-only current VM identity and optional screenshot; no foreground change."""
import argparse,json,os,subprocess,sys
from pathlib import Path
root=Path(os.environ.get('SWDOL_PROJECT_ROOT','/Users/kemi/coding/swdol2026'))
legacy=Path('/Users/kemi/coding/xyOnlie')
sys.path.insert(0,str(root/'tools/xp-original-control'))
from session import current_vm,run
p=argparse.ArgumentParser();p.add_argument('--capture',type=Path);p.add_argument('--vm-name',required=True,choices=['XP SWDOL Voodoo3','XP SWDOL Voodoo3 B']);args=p.parse_args()
pid=current_vm(args.vm_name)
line=run(['swift',legacy/'tools/legacy-dynamic-trace/find_86box_window.swift',args.vm_name+' - 86Box'],timeout=20)
parts=line.split('\t',5)
if len(parts)!=6:raise SystemExit('unexpected window identity output')
result={'vmPid':pid,'windowId':int(parts[0]),'bounds':[int(x) for x in parts[1:5]],'title':parts[5],
        'frontmost':json.loads(run([legacy/'tools/legacy-dynamic-trace/build/mac-frontmost']))}
if args.capture:
    args.capture.parent.mkdir(parents=True,exist_ok=True)
    run(['screencapture','-x','-l'+parts[0],args.capture],timeout=5)
    result['capture']=str(args.capture)
print(json.dumps(result,ensure_ascii=False,indent=2))
