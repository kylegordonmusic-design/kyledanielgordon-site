# Copy fetched art (repo art/*.jpg) into the image set and register keys in assets.json
import json, os, shutil
R='/home/claude/kyledanielgordon-site/art'; A=json.load(open('assets.json'))
for f in sorted(os.listdir(R)):
    k=f[:-4]; shutil.copy(os.path.join(R,f), f'/home/claude/kdg_web/{f}')
    A.setdefault(k, f'/_blob/art-{k}')
json.dump(A, open('assets.json','w'), indent=0, ensure_ascii=False); print(len(A),'images')
