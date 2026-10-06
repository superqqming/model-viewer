#!/usr/bin/env python3
"""掃描 models/，產生 models/list.json（老師設定頁的模型清單）。由「發布模型.command」呼叫。"""
from __future__ import annotations

import json
import os
import sys
import time
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(ROOT, 'models')
EXTS = {'.obj', '.stl', '.glb'}
WARN_MB = 50    # GitHub 對超過 50 MB 的檔案會警告
LIMIT_MB = 95   # 超過 100 MB 會被 GitHub 拒收


def main() -> int:
    items, notes, too_big = [], [], []
    for dirpath, dirnames, filenames in os.walk(MODELS):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith('.'))
        for fn in sorted(filenames):
            if fn.startswith('.') or fn == 'list.json':
                continue
            path = os.path.join(dirpath, fn)
            rel = unicodedata.normalize('NFC', os.path.relpath(path, MODELS).replace(os.sep, '/'))
            ext = os.path.splitext(fn)[1].lower()
            if ext == '.gltf':
                notes.append(f'{rel}：.gltf 需要另外的 .bin 檔，請改匯出成 .glb')
            if ext not in EXTS:
                continue
            size = os.path.getsize(path)
            mb = size / 1024 / 1024
            if mb > LIMIT_MB:
                too_big.append(f'{rel}（{mb:.0f} MB）')
                continue
            if mb > WARN_MB:
                notes.append(f'{rel} 有 {mb:.0f} MB，同學載入會很慢，建議在 SketchUp 簡化後再匯出')
            items.append({
                'file': rel,
                'bytes': size,
                'modified': time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(path))),
            })
    if too_big:
        print('以下檔案超過 GitHub 的大小上限（100 MB），請先在 SketchUp 簡化模型或移出 models/：')
        for t in too_big:
            print('  ·', t)
        return 1
    with open(os.path.join(MODELS, 'list.json'), 'w', encoding='utf-8') as f:
        json.dump({'models': items}, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'models/ 裡有 {len(items)} 個模型：')
    for it in items:
        print('  ·', it['file'])
    for n in notes:
        print('注意：', n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
