# Jarvis · AI 助手 - 官网

> Jarvis 个人 AI 助手的展示网站，基于 GitHub Pages + GitHub Actions 托管。

**线上地址**：https://nktdrenzy-commits.github.io/jarvis-pages/

## 页面结构

```
/
├── index.html                    # 首页
├── Jarvis案例.html               # 案例入口页（卡片列表）
├── 案例集.html                   # 案例集（时间线视图）
├── 案例1_任姓族谱深度研究.html   # 案例1详情
├── detail.html                   # 技术详情页（legacy）
├── index_with_fm.html            # 带功能地图的首页（legacy）
└── .github/workflows/pages.yml   # CI/CD 流水线
```

## 本地开发

```bash
# 克隆项目
git clone https://github.com/nktdrenzy-commits/jarvis-pages.git
cd jarvis-pages

# 本地预览（用任意静态服务器）
python3 -m http.server 8080
# 访问 http://localhost:8080
```

## 发布流程

**自动发布**（已有流水线）：
- push 到 `main` 分支 → 自动部署到 GitHub Pages（约 1 分钟）

**手动发布**：
```bash
git checkout main
git merge --no-ff <your-branch>  # 合并 PR 或热修
git push origin main              # 触发自动部署
```

## 添加新案例

1. 创建新案例单页（如 `案例2_xxx.html`）
2. 在 `Jarvis案例.html` 的 `.cases-grid` 中添加案例卡片
3. 在 `案例集.html` 的 `.timeline` 中添加时间线条目
4. 提交 PR → 预览确认 → 合并到 main

## 技术栈

- 纯 HTML + CSS + JS（无框架依赖）
- Google Fonts: Charter, PingFang SC, Microsoft YaHei
- 部署: GitHub Pages + GitHub Actions
