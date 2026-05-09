# 如何贡献

## 分支规范

| 分支 | 用途 |
|------|------|
| `main` | 正式环境，任何时候可部署 |
| `feat/<name>` | 新功能开发 |
| `fix/<name>` | Bug 修复 |
| `hotfix/<name>` | 紧急热修 |

## 添加新案例

### Step 1：创建案例单页

```html
<!-- 案例N_标题.html -->
<!-- 参考案例1_任姓族谱深度研究.html 的结构 -->
```

命名规范：`案例{N}_{简短标题}.html`

### Step 2：注册到案例入口页

在 `Jarvis案例.html` 的 `<div class="cases-grid">` 中添加：

```html
<div class="case-card">
  <a href="案例N_标题.html">
    <h3>案例标题</h3>
    <p>简短描述...</p>
    <div class="tags">
      <span class="tag">分类</span>
    </div>
  </a>
</div>
```

### Step 3：注册到案例集

在 `案例集.html` 的 `<div class="timeline">` 中添加时间线条目。

### Step 4：提交 PR

```bash
git checkout -b feat/案例N标题
git add .
git commit -m "Add 案例N: 标题"
git push origin feat/案例N标题
# 然后在 GitHub 上创建 PR
```

## 提交信息规范

格式：`<type>: <description>`

| type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 格式/样式调整（不影响功能） |
| `refactor` | 重构 |
| `chore` | 杂项（构建脚本、CI等）|

示例：
```
feat: 添加任姓族谱深度研究案例
fix: 修复首页导航栏缺失案例入口
docs: 更新 README 添加本地预览说明
```
