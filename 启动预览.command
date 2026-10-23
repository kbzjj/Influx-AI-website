#!/bin/zsh
cd -- "${0:A:h}"
if curl --fail --silent --output /dev/null http://127.0.0.1:4174/; then
  print '方案二预览已在运行，请打开：http://127.0.0.1:4174/'
  read '?按回车关闭此窗口。'
else
  print '请打开：http://127.0.0.1:4174/'
  print '保留此窗口以保持预览运行，结束时按 Control+C。'
  python3 -m http.server 4174 --bind 127.0.0.1 --directory .
fi
