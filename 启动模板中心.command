#!/bin/zsh
cd -- "${0:A:h}"
if curl --fail --silent --output /dev/null http://127.0.0.1:4176/api/catalog; then
  print '模板中心已运行：http://127.0.0.1:4176/'
  open 'http://127.0.0.1:4176/'
else
  print '正在启动模板中心：http://127.0.0.1:4176/'
  print '保留此窗口。按 Control+C 可关闭模板中心及由它启动的预览。'
  python3 .agents/skills/website-replica/scripts/library.py --port 4176 --open
fi
