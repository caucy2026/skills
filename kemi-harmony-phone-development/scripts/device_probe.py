#!/usr/bin/env python3
"""Read-only, target-scoped HDC identity and UI capture. Never resets HDC."""
import argparse, json, subprocess
from pathlib import Path

def run(hdc, target, *args):
    result = subprocess.run([hdc, '-t', target, *args], capture_output=True, text=True, timeout=20)
    if result.returncode or '[Fail]' in result.stdout:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout

def flatten(node):
    result = [node.get('attributes', {})]
    for child in node.get('children', []): result.extend(flatten(child))
    return result

def layout(hdc, target):
    remote = '/data/local/tmp/kemi-skill-layout.json'
    run(hdc, target, 'shell', 'uitest', 'dumpLayout', '-p', remote)
    return json.loads(run(hdc, target, 'shell', 'cat', remote))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hdc', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--expected-model', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    keys = ['const.product.model', 'const.product.name', 'const.ohos.apiversion',
            'const.ohos.fullname', 'const.product.cpu.abilist']
    identity = {key: run(args.hdc, args.target, 'shell', 'param', 'get', key).strip() for key in keys}
    if identity['const.product.model'] != args.expected_model:
        raise RuntimeError('Device model mismatch; no UI actions performed')
    tree = layout(args.hdc, args.target)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'device.json').write_text(json.dumps(identity, ensure_ascii=False, indent=2))
    (args.out / 'layout.json').write_text(json.dumps(tree, ensure_ascii=False, indent=2))
    print(json.dumps({'identity': identity, 'text_nodes': sum(bool(n.get('text')) for n in flatten(tree))}, ensure_ascii=False))

if __name__ == '__main__': main()
