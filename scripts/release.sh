#!/usr/bin/env bash
# release.sh - 本地发布脚本
# 用法: bash scripts/release.sh [patch|minor|major]
# 推荐用 GitHub Actions 的 Release workflow 触发正式发布（自动更新 CHANGELOG + 打标签）

set -e

VERSION_TYPE=${1:-patch}

# 检查 git 状态
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ 有未提交的更改，请先 commit"
  exit 1
fi

# 获取当前版本
CURRENT=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "当前版本: $CURRENT"

# 解析版本号
MAJOR=$(echo $CURRENT | sed 's/v//' | cut -d. -f1)
MINOR=$(echo $CURRENT | sed 's/v//' | cut -d. -f2)
PATCH=$(echo $CURRENT | sed 's/v//' | cut -d. -f3)

if [ "$VERSION_TYPE" = "major" ]; then
  MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0
elif [ "$VERSION_TYPE" = "minor" ]; then
  MINOR=$((MINOR + 1)); PATCH=0
else
  PATCH=$((PATCH + 1))
fi

NEW="v${MAJOR}.${MINOR}.${PATCH}"
echo "新版本: $NEW"
echo ""
echo "请确认发布 $NEW？ [y/N]"
read -r confirm
if [ "$confirm" != "y" ]; then
  echo "已取消"
  exit 0
fi

# 创建标签
git tag -a "$NEW" -m "Release $NEW"
echo "✅ 已创建标签 $NEW"
echo ""
echo "推送到 GitHub 触发流水线:"
echo "  git push origin main && git push origin $NEW"
echo ""
echo "或通过 GitHub Actions 触发正式 Release workflow（自动更新 CHANGELOG）"
