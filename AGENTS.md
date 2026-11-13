# Repository Guidelines

## 项目结构与模块组织

- `index.html` 内嵌样式、脚本、GLSL 着色器和笔画数据，包含时间表、距离场、WebGL2 渲染及 SVG 降级逻辑。
- 优先在 `CFG` 中调整节奏、材质和布局，在 `THEMES` 中调整配色。
- `probe/question_std.js` 生成标准问号的 `QDATA`；`probe/extract_glyph.py` 提取字体笔画中心线。
- 没有独立的源码、素材或测试目录。`probe/` 被忽略，但上述两个脚本已跟踪；实验文件保留在该目录。

## 构建、测试与开发命令

从仓库根目录运行：

```sh
python3 -m http.server 8000 --bind 127.0.0.1
node probe/question_std.js
node --check probe/question_std.js
git diff --check
```

命令依次用于本地预览、输出问号 JSON、检查生成脚本语法、检查差异中的空白问题。预览地址：`http://127.0.0.1:8000/`。

页面无需安装依赖或构建。字体提取另需 `fontTools` 和未附带的字体；运行前检查脚本的 `FONT` 路径。Node.js 仅用于辅助脚本。

## 编码风格与命名约定

JavaScript、CSS、GLSL 使用两空格缩进，Python 使用四空格。JavaScript 保留分号，优先使用 `const`；函数与一般变量使用 `camelCase`，配置常量使用 `UPPER_SNAKE_CASE`，Python 函数使用 `snake_case`。

未配置格式化或 lint 工具。保持改动局部；注释说明坐标系和单位。修改问号生成逻辑后，同步更新内嵌 `QDATA`。

## 测试指南

暂无测试框架、覆盖率门槛或测试命名约定。提交前在浏览器验证：

- 完整播放问号、玻璃珠与正文，检查控制台错误及阶段衔接。
- 使用 `/?at=3` 定格加载后第 3 秒，`/?t=0.5` 检查正文书写 50%，`/?th=50` 检查写完 50 秒后的配色。
- 使用 `/?gl=0` 验证 SVG/CSS 降级；检查桌面、窄屏、窗口缩放及 `prefers-reduced-motion` 模式。

## 提交与 Pull Request 指南

历史提交使用简短中文描述效果，如“问号改为标准写法；书写时不再显示笔尖形状”，无固定类型前缀。每次提交聚焦一个改动，正文解释原因。

PR 说明目的、影响和验证结果，有相关 issue 时附链接。视觉改动附相同视口、定格参数的前后截图；动画改动附录屏。报告 WebGL2、降级及减少动态效果模式的检查结果。
