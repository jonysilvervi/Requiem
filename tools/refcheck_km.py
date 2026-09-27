"""Citation checker for REQUIEM_KNOWLEDGE_MODEL.md.

Checks that every "DOCUMENT.md, section N" reference points to a heading that
exists, that bare "section N" references resolve inside the Knowledge Model,
and that every FD-Bx reference exists in REQUIEM_FOUNDATION_DECISIONS.md.

Usage (from the repository root):
    python tools/refcheck_km.py memory-core/context

Expected result: "problems: 0".
"""
import re,sys,os
ctx=sys.argv[1]; km=open(os.path.join(ctx,'REQUIEM_KNOWLEDGE_MODEL.md'),encoding='utf-8').read()
def heads(path):
    hs=set()
    for l in open(path,encoding='utf-8'):
        m=re.match(r'^#{1,3} (\d+(?:\.\d+)?)[.\s]',l)
        if m: hs.add(m.group(1))
    return hs
bad=0; n=0
for m in re.finditer(r'(REQUIEM_[A-Z_]+\.md),? sections? (\d+(?:\.\d+)?)',km):
    doc,sec=m.group(1),m.group(2); n+=1
    p=os.path.join(ctx,doc)
    if not os.path.exists(p): print('MISSING DOC',doc,sec); bad+=1; continue
    if sec not in heads(p): print('NO SECTION',doc,sec); bad+=1
local=heads(os.path.join(ctx,'REQUIEM_KNOWLEDGE_MODEL.md'))
for m in re.finditer(r'(?<!\.md, )(?<!\.md )\bsection (\d+(?:\.\d+)?)',km):
    s=km[max(0,m.start()-4):m.start()]
    n+=1
    if m.group(1) not in local: print('LOCAL NO SECTION',m.group(1),repr(km[m.start()-60:m.end()])); bad+=1
fd=open(os.path.join(ctx,'REQUIEM_FOUNDATION_DECISIONS.md'),encoding='utf-8').read()
for b in sorted(set(re.findall(r'FD-B\d',km))):
    n+=1
    if not re.search(r'^# \d+\. '+b+r' ',fd,re.M): print('NO FD',b); bad+=1
print('checked',n,'refs; problems:',bad)
