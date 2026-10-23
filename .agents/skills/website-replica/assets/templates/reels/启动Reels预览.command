#!/bin/zsh
cd -- "${0:A:h}"
if curl --fail --silent --output /dev/null http://127.0.0.1:4175/index.html; then
  print '4175 端口已有页面运行，请打开：http://127.0.0.1:4175/'
  print '如果不是 Reels 页面，请关闭占用该端口的服务后重试。'
  read '?按回车关闭此窗口。'
else
  print 'Reels 本地学习预览：http://127.0.0.1:4175/'
  print '保留此窗口以保持预览运行，结束时按 Control+C。'
  python3 -m http.server 4175 --bind 127.0.0.1 --directory .
fi
