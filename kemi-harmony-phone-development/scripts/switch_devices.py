#!/usr/bin/env python3
"""Authorized peer-switch QA; no remote text, power or lock input is injected."""
import argparse, hashlib, json, re, time
from pathlib import Path
from PIL import Image, ImageStat
from device_probe import run, layout, flatten

def bounds(node):
    nums = list(map(int, re.findall(r'-?\d+', node['bounds'])))
    if len(nums) != 4: raise RuntimeError('Unexpected bounds format')
    return nums

def peers(nodes, label):
    return [n for n in nodes if n.get('text', '').split('\n')[0] == label]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hdc', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--expected-model', required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--peer', action='append', required=True)
    parser.add_argument('--count', type=int, default=100)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    digest = hashlib.sha256(args.candidate.read_bytes()).hexdigest()
    if digest != args.sha256: raise RuntimeError('Candidate hash mismatch')
    if len(set(args.peer)) < 2 or args.count < 1: raise RuntimeError('At least two distinct authorized peers required')
    model = run(args.hdc, args.target, 'shell', 'param', 'get', 'const.product.model').strip()
    if model != args.expected_model: raise RuntimeError('Device model mismatch')
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out/'candidate.json').write_text(json.dumps({'sha256':digest,'target':args.target,'peers':args.peer,'count':args.count},indent=2))
    results = []
    for index in range(args.count):
        label = args.peer[index % len(args.peer)]
        nodes = flatten(layout(args.hdc, args.target))
        for attempt in range(3):
            match = peers(nodes, label)
            if match: break
            toolbar = [n for n in nodes if n.get('text', '').split('\n')[0] == '收起']
            if not toolbar: raise RuntimeError('Peer toolbar absent; restore UI before continuing')
            x1, y1, x2, y2 = bounds(toolbar[0]); y = (y1+y2)//2
            run(args.hdc, args.target, 'shell', 'uitest', 'uiInput', 'swipe', str(max(30,x1-40)), str(y), '40', str(y), '600')
            nodes = flatten(layout(args.hdc, args.target))
        if not match: raise RuntimeError('Authorized peer absent: ' + label)
        button = match[0]
        if button.get('selected') == 'true': raise RuntimeError('Test would count an already-selected peer as a switch')
        if button.get('enabled') == 'false': raise RuntimeError('Peer disabled/offline or in use elsewhere: ' + label)
        x1,y1,x2,y2 = bounds(button)
        started = time.monotonic()
        run(args.hdc, args.target, 'shell', 'uitest', 'uiInput', 'click', str((x1+x2)//2), str((y1+y2)//2))
        deadline = started + 25
        while True:
            nodes = flatten(layout(args.hdc, args.target))
            match = peers(nodes, label)
            loading = any('正在连接' in n.get('text', '') for n in nodes)
            modal = any(n.get('text') in ['当前权限无法继续', '请先登录后再继续远程会话。', '连接错误'] for n in nodes)
            if modal: raise RuntimeError('Account policy or connection error; do not bypass authorization')
            if not match and not loading:
                toolbar = [n for n in nodes if n.get('text', '').split('\n')[0] == '收起']
                if toolbar:
                    x1,y1,x2,y2 = bounds(toolbar[0]); y = (y1+y2)//2
                    run(args.hdc,args.target,'shell','uitest','uiInput','swipe',str(max(30,x1-40)),str(y),'40',str(y),'600')
                    nodes = flatten(layout(args.hdc,args.target)); match = peers(nodes,label)
            if match and match[0].get('selected') == 'true' and not loading: break
            if time.monotonic() > deadline:
                (args.out/'failure.json').write_text(json.dumps({'index':index+1,'target':label,'loading':loading,'nodes':nodes},ensure_ascii=False,indent=2))
                raise RuntimeError('Switch timeout: ' + label)
        image_path = args.out / ('%03d.jpeg' % (index+1))
        remote = '/data/local/tmp/kemi-switch-frame.jpeg'
        run(args.hdc, args.target, 'shell', 'snapshot_display', '-f', remote)
        run(args.hdc, args.target, 'file', 'recv', remote, str(image_path))
        image = Image.open(image_path).convert('RGB')
        toolbar = [n for n in nodes if n.get('text','').split('\n')[0] == '收起']
        bottom = bounds(toolbar[0])[1] if toolbar else image.height-100
        area = image.crop((int(image.width*.12), 120, int(image.width*.78), max(121,bottom-60)))
        variance = ImageStat.Stat(area).stddev
        nonblank = max(variance) > 15
        item = {'index':index+1, 'target':label, 'selected':True, 'loading':False,
                'seconds':round(time.monotonic()-started,3), 'frame_stddev':variance,
                'nonblank':nonblank, 'screenshot':str(image_path),
                'screenshot_sha256':hashlib.sha256(image_path.read_bytes()).hexdigest()}
        results.append(item)
        (args.out/'results.json').write_text(json.dumps({'candidate_sha256':digest,'scope':'peer-selection-and-nonblank-frames; visual review required','results':results},ensure_ascii=False,indent=2))
        if not nonblank: raise RuntimeError('Blank remote frame')
        if (index+1)%10 == 0: print('%d/%d switches; selected target and nonblank frame' % (index+1,args.count),flush=True)
    print('Switch assertions passed; inspect screenshots before declaring correct remote contents',flush=True)

if __name__ == '__main__': main()
