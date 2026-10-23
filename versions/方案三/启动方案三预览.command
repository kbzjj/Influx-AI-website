#!/bin/zsh
cd -- "${0:A:h}/../.."
preview_url='http://127.0.0.1:4174/versions/%E6%96%B9%E6%A1%88%E4%B8%89/'
if curl --fail --silent --output /dev/null "$preview_url"; then
  open "$preview_url"
  print '方案三预览已打开。'
else
  print "请打开：$preview_url"
  print '保留此窗口以保持预览运行，结束时按 Control+C。'
  python3 -m http.server 4174 --bind 127.0.0.1 --directory .
fi
