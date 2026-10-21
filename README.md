# EECS 498 AASE 非官方中文课程资料

独立中文整理，非密歇根大学或原课程团队网站。原站：<https://eecs498-aase.github.io/>。核对：2026-10-21。

## 内容与边界

6个HTML页面：课程概览、教学大纲、FAQ、播客、来源与译注、404。包含15周/28讲课表、13次实验、评分政策、25个问题、7期播客入口。

没有发现整站开放许可，所以正文使用独立中文事实整理，而非逐字全文翻译。原音频、逐字稿、课件、日历、课程平台和个人仓库仍由原站提供；课程规则以官方为准。Python版本、FAQ联络TBD与大纲、黑客松待公布日期等差异在来源页注明。

原课程内容版权标示：© 2026 University of Michigan · EECS 498-016。代码MIT许可不覆盖课程材料、商标或第三方资源。

## 本地使用

无需安装依赖，Python 3.10+用于构建和预览，浏览器运行不需要Python：

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8080 --directory docs
```

打开 http://localhost:8080/ 。docs内已包含构建成品。

## GitHub Pages 发布（免费公开仓库）

1. 仓库 Settings → Pages。
2. Build and deployment → Source 选择 **Deploy from a branch**。
3. Branch 选择 **main**，目录选择 **/docs**，点击 **Save**。
4. 等待 Pages build and deployment 成功，再打开：
   https://yuyaxiong.github.io/eecs498-aase-zh/

上面的URL是预计地址，只有部署成功且实际访问通过才算发布完成。连接工具没有Pages管理接口；上传文件本身不会启用Pages。

后续修改 scripts/build.py（页面内容）、docs/assets/style.css（样式）、docs/assets/app.js（交互），重新构建并提交。所有站内资源使用相对路径，兼容项目子路径。

## 验证与维护

- scripts/check.py 检查本地链接、锚点、语言标记、页面数量、课表、节目与FAQ数量。
- source-links.json 记录原站发现的功能性外链；校验要求保留。
- 不接入第三方追踪或分析。无账号、数据库、表单提交及服务端API。
- 资料不会自动同步。维护者应核对原站后修改内容与日期并重新发布。
- 外部资源是否可访问、是否需要学校登录，由原服务决定。
