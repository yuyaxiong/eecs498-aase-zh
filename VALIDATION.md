# 验证记录

核对日期：2026-10-21（Asia/Shanghai）。

## 已通过

- Python标准库构建：6个HTML页面、15周、28讲、13次实验、25个FAQ、7期播客。
- 本地目标与锚点：80项通过；所有页面有zh-Hans、h1、非官方声明。
- 原站功能性外链：从4个公开主页面提取后与成品逐一比对，未丢失。原始RSS、7个音频、7个逐字稿及日历均保留。
- JavaScript语法检查通过。
- 本地首页HTTP 200。
- 浏览器默认桌面宽度：首页视觉已检查，导航、非官方提示、主CTA与内容布局正常。
- 浏览器390×844：主体宽度390px，无横向溢出；菜单展开aria-expanded=true；Escape关闭为false。
- FAQ：不存在的关键词显示0/25及无结果反馈；清空恢复25/25；首条原生折叠可展开。
- 播客：Deep Dive筛选显示2/7。
- 浏览器日志：上述交互无warning/error。
- 404页使用已知GitHub Pages地址为base，嵌套失效URL仍能恢复到项目首页与资产。

## 未执行或受限

- 未逐个确认所有第三方服务的最终可访问性；链接存在不等于外站免登录可用。
- 未制作中文音频或翻译逐字稿、课件全文。
- 无JavaScript、打印及屏幕阅读器的完整人工验证尚未执行；正文直接存在HTML中，FAQ原生details，打印有专用样式。
- GitHub连接确认yuyaxiong/eecs498-aase-zh为公开仓库，具有admin/push权限；当前连接不提供Pages管理接口，本机GitHub登录无效。
- 浏览器进入GitHub设置时超时。GitHub Pages启用和线上部署不计为已完成。

## 最后发布步骤

在仓库 Settings → Pages 设置 Source=Deploy from a branch，Branch=main，Folder=/docs，Save。等待部署成功，再验证线上各页面。

预计地址（不是部署成功证明）：https://yuyaxiong.github.io/eecs498-aase-zh/
