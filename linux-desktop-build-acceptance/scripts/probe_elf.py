#!/usr/bin/env python3
"""Read selected ELF metadata only; never load or execute the supplied files."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import unittest

ARCHES={3:'i386',40:'arm',62:'x86_64',183:'aarch64',243:'riscv'}
ALIASES={'amd64':'x86_64','x86_64':'x86_64','arm64':'aarch64','aarch64':'aarch64'}
def version(value):
    if not re.fullmatch(r'\d+(?:\.\d+){1,2}',value):raise ValueError('expected numeric ABI version, e.g.2.31')
    return tuple(map(int,value.split('.')))
def elf_header(raw):
    if len(raw)<20 or raw[:4]!=b'\x7fELF':raise ValueError('not an ELF header')
    if raw[4] not in (1,2) or raw[5] not in (1,2):raise ValueError('unsupported ELF class/byte order')
    machine=int.from_bytes(raw[18:20],'little' if raw[5]==1 else 'big')
    return {'bits':32 if raw[4]==1 else 64,'byteOrder':'little' if raw[5]==1 else 'big','machine':machine,'architecture':ARCHES.get(machine,'unknown'),'appImageOuterOnly':raw[8:11]==b'AI\x02'}
def requirements(text):
    needed=False;glibc=set();glibcxx=set();private=False;other=set()
    for line in text.splitlines():
        if line.startswith('Version needs section'):needed=True
        elif line.startswith('Version ') and ' section ' in line:needed=False
        if not needed:continue
        glibc.update(re.findall(r'Name:\s+GLIBC_(\d+(?:\.\d+)+)',line))
        glibcxx.update(re.findall(r'Name:\s+GLIBCXX_(\d+(?:\.\d+)+)',line))
        private|='Name: GLIBC_PRIVATE' in line
        other.update(x for x in re.findall(r'Name:\s+(GLIBC_[A-Za-z0-9_.]+)',line) if x!='GLIBC_PRIVATE' and not re.fullmatch(r'GLIBC_\d+(?:\.\d+)+',x))
    def maximum(values):return max(values,key=version) if values else None
    return {'requiredGlibc':maximum(glibc),'requiredGlibcxx':maximum(glibcxx),'privateGlibcAbi':private,'otherGlibcVersionRequirements':sorted(other)}
def inspect(path,readelf,target_arch=None,maximum_glibc=None):
    p=Path(path).resolve(strict=True)
    with p.open('rb') as stream:header=elf_header(stream.read(20))
    h=hashlib.sha256()
    with p.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    env=dict(os.environ,LC_ALL='C')
    info=subprocess.run([readelf,'--version-info',str(p)],capture_output=True,text=True,errors='replace',timeout=30,env=env,check=True)
    dynamic=subprocess.run([readelf,'-d',str(p)],capture_output=True,text=True,errors='replace',timeout=30,env=env,check=True)
    row={'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest(),**header,**requirements(info.stdout),'neededLibraries':re.findall(r'\(NEEDED\).*?\[([^\]]+)\]',dynamic.stdout),'runtimeLoadedOrExecuted':False}
    row['matchesConfiguredArchitecture']=None if target_arch is None else row['architecture']==ALIASES[target_arch]
    row['glibcRequirementWithinConfiguredBaseline']=None if maximum_glibc is None or row['privateGlibcAbi'] or row['otherGlibcVersionRequirements'] else row['requiredGlibc'] is None or version(row['requiredGlibc'])<=version(maximum_glibc)
    return row
class ProbeTests(unittest.TestCase):
    def test_real_architecture_fields(self):
        raw=bytearray(20);raw[:6]=b'\x7fELF\x02\x01';raw[18:20]=(183).to_bytes(2,'little');self.assertEqual(elf_header(raw)['architecture'],'aarch64')
        raw[5]=2;raw[18:20]=(62).to_bytes(2,'big');self.assertEqual(elf_header(raw)['architecture'],'x86_64')
    def test_rejects_non_elf_and_truncation(self):
        for raw in (b'notelf',b'\x7fELF\x02\x01'):
            with self.assertRaises(ValueError):elf_header(raw)
    def test_ignores_defined_versions(self):
        text="Version definition section '.gnu.version_d' contains1entry:\nName: GLIBC_2.99\nVersion needs section '.gnu.version_r' contains2entries:\nName: GLIBC_2.17\nName: GLIBC_2.34\nName: GLIBCXX_3.4.30\n"
        row=requirements(text);self.assertEqual(row['requiredGlibc'],'2.34');self.assertEqual(row['requiredGlibcxx'],'3.4.30');self.assertFalse(version(row['requiredGlibc'])<=version('2.31'));self.assertTrue(version(row['requiredGlibc'])<=version('2.35'))
    def test_numeric_order_and_private(self):
        row=requirements("Version needs section '.gnu.version_r':\nName: GLIBC_2.9\nName: GLIBC_2.31\nName: GLIBC_PRIVATE\n");self.assertEqual(row['requiredGlibc'],'2.31');self.assertTrue(row['privateGlibcAbi'])
    def test_unknown_glibc_requirement(self):
        row=requirements("Version needs section '.gnu.version_r':\nName: GLIBC_ABI_DT_RELR\n");self.assertEqual(row['otherGlibcVersionRequirements'],['GLIBC_ABI_DT_RELR']);self.assertIsNone(row['requiredGlibc'])
    def test_appimage_not_payload_audit(self):
        raw=bytearray(20);raw[:6]=b'\x7fELF\x02\x01';raw[8:11]=b'AI\x02';raw[18:20]=(62).to_bytes(2,'little');self.assertTrue(elf_header(raw)['appImageOuterOnly'])
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--elf',action='append',default=[]);parser.add_argument('--target-arch',choices=sorted(ALIASES));parser.add_argument('--max-glibc');parser.add_argument('--readelf');parser.add_argument('--report');parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    if args.self_test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProbeTests));return 0 if result.wasSuccessful() else 1
    if not args.elf:parser.error('provide at least one explicit --elf path')
    if args.max_glibc:
        try:version(args.max_glibc)
        except ValueError as e:parser.error(str(e))
    readelf=args.readelf or shutil.which('readelf')
    report={'scope':'selected ELF headers, DT_NEEDED and version-needs only; not complete compatibility or package acceptance','hostArchitecture':platform.machine(),'hostLibc':platform.libc_ver(),'configuredArchitecture':args.target_arch,'configuredMaxGlibc':args.max_glibc,'runtimeLoadedOrExecuted':False,'files':[],'errors':[]}
    if not readelf:report['errors'].append('readelf unavailable; no package installation performed')
    else:
        for path in args.elf:
            try:report['files'].append(inspect(path,readelf,args.target_arch,args.max_glibc))
            except Exception as e:report['errors'].append({'path':str(path),'error':type(e).__name__+': '+str(e)[:300]})
    report['configuredLimitsSatisfied']=not report['errors'] and all((args.target_arch is None or row['matchesConfiguredArchitecture'] is True) and (args.max_glibc is None or row['glibcRequirementWithinConfiguredBaseline'] is True) for row in report['files'])
    data=json.dumps(report,ensure_ascii=False,indent=2)
    if args.report:
        with Path(args.report).open('x',encoding='utf-8') as f:f.write(data+'\n')
    print(data);return 3 if report['errors'] or (args.max_glibc and any(row['glibcRequirementWithinConfiguredBaseline'] is None for row in report['files'])) else 0 if report['configuredLimitsSatisfied'] else 2
if __name__=='__main__':raise SystemExit(main())
