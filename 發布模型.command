#!/bin/zsh
# 雙擊執行：更新 models/ 的清單 → 上傳到 GitHub → 開啟線上的老師設定頁
cd "${0:A:h}" || exit 1
pause() { echo; echo "按 Enter 關閉視窗"; read; }

echo "【3D 模型檢視器】發布模型"
echo
/usr/bin/python3 tools/make_list.py || { echo; echo "沒有發布。"; pause; exit 1; }

remote=$(git remote get-url origin 2>/dev/null)
if [[ -z "$remote" ]]; then
  echo; echo "這個資料夾還沒連到 GitHub，請先照 README.md「第一次設定」做一次。"; pause; exit 1
fi

echo
git add -A models
if git diff --cached --quiet; then
  echo "模型沒有變動。"
else
  git commit -q -m "更新模型（$(date '+%Y-%m-%d %H:%M')）" && echo "已記錄變更。"
fi

echo "上傳中…"
if ! git push -q origin HEAD; then
  echo; echo "上傳失敗：請確認網路，或 GitHub 登入是否過期。"; pause; exit 1
fi

slug=$(echo "$remote" | sed -E 's#^(https://github\.com/|git@github\.com:)##; s#\.git$##')
owner=${slug%%/*}; repo=${slug#*/}
url="https://${owner:l}.github.io/${repo}/"
echo
echo "完成！GitHub Pages 約 1～2 分鐘後更新。"
echo "老師設定頁：${url}?teacher"
open "${url}?teacher"
pause
