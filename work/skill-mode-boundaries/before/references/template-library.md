# 模板库与统一入口

本技能同时保存复刻流程、模板实体和本地模板中心。所有复刻成果集中放在技能内部的 `assets/templates/<slug>/`，每个模板只保留一个实体目录。不要再将新模板默认保存到项目的 `references/` 或其他重复副本中。

## 打开模板中心

用户要求“打开/启动模板中心”时，只启动并打开入口，不询问新复刻范围，也不重新抓取任何网站：

```sh
python3 <skill-dir>/scripts/library.py --port 4176
```

先请求 `http://127.0.0.1:4176/api/catalog`，若已有正确服务就复用，不重复启动。确认首页响应成功后，用当前应用支持的浏览器工具打开 <http://127.0.0.1:4176/>。macOS 用户可双击技能目录中的 `启动模板中心.command`；项目根目录也有方便访问的启动入口。

中心只提供模板卡片、分类、搜索、封面直达预览、原站和学习指南。没有收藏、备注、重命名或删除管理。不要自行扩展为管理后台。

点击封面会通过 `/open/<slug>` 按需启动模板独立的 loopback 预览端口，并跳转到其根路径。这样 Framer 等依赖 `/features` 或 `/blog` 的客户端路由不会受到中心路径前缀影响。停止中心服务时，同时关闭由它启动的模板服务器；不关闭其他已有预览服务。

服务支持普通 HTTP Range 视频读取及 Framer CMS 的 `?range=start-end,...` 分段请求。不能把依赖这些行为的模板改用普通 `python -m http.server` 后仍假定交互等价。

## 新复刻完成后自动入库

每次仍按主技能先确认新网站的范围，再在 `assets/templates/<slug>/` 内完成复刻。保留原始运行时、路由、资源、学习文档和 QA。完成实际验证后：

1. 保存本地页面真实截图作为封面，使用相对路径；不要用 AI 示意图假装截图。
2. 写入 `template.json`，名称、页面数、技术栈、标签及状态必须来自本次实际成果。
3. 执行 `python3 <skill-dir>/scripts/library.py --check`，修复入口或封面缺失问题。
4. 通过中心封面进入该模板并验证首页及至少一条内页路线；有关键交互的也要操作核对。中心每次读取目录，因此刷新即可发现新条目，不需要手工维护第二份目录清单。

最小元数据示例：

```json
{
  "name": "Example",
  "description": "该模板的真实视觉与动效特点。",
  "category": "AI 产品",
  "stack": "Framer",
  "sourceUrl": "https://example.com/",
  "entry": "index.html",
  "cover": "qa/local-home.png",
  "guide": "STUDY_GUIDE.md",
  "tags": ["画廊", "滚动动效"],
  "pageCount": 1,
  "status": "已收录 · 本地视觉与动效预览",
  "order": 100
}
```

目录名仅使用小写字母、数字和连字符。`entry`、`cover` 和 `guide` 都是模板内部的相对路径。不能用 `template.json` 的状态文字代替实际验收；受限或未完成的成果需明确标注，不能自动宣传为完整 1:1。

旧的 `references/reels-webflow` 与 `references/veo-public` 保留为指向技能内实体的兼容链接，没有第二份模板副本。修改模板、学习文档与刷新脚本时，以技能内目录为准。原始文本快照可留在模板的 `_source/` 中作为学习和追溯资料，它不参与预览。

## 维护验证

```sh
PYTHONDONTWRITEBYTECODE=1 python3 <skill-dir>/scripts/test_library.py
```

该测试使用临时模板，验证动态目录发现、封面跳转、模板根路径路由、普通视频 Range、Framer CMS 分段数据和目录约束；不改变真实模板，也不启动第三方浏览器。
