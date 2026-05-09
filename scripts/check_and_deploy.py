#!/usr/bin/env python3
"""
check_and_deploy.py - 发布前检查 + 推送到 GitHub 触发部署
用法: python3 scripts/check_and_deploy.py
"""

import subprocess
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent


def run_cmd(cmd, cwd=None):
    """执行命令并返回结果"""
    print(f"  $ {cmd}")
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or SCRIPT_DIR,
        capture_output=True, text=True
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr and result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode == 0


def step(name):
    print(f"\n🔄 {name}")


def main():
    os.chdir(SCRIPT_DIR)
    
    print("=" * 50)
    print("Jarvis Pages - 发布前检查")
    print("=" * 50)
    
    # Step 1: 检查 git 状态
    step("检查 Git 状态")
    if not run_cmd("git status --porcelain"):
        print("  ⚠️  有未提交的更改")
        resp = input("  继续发布？[y/N]: ")
        if resp.lower() != 'y':
            print("已取消")
            return
    
    # Step 2: 运行链接检查
    step("检查内部链接")
    link_checker = SCRIPT_DIR / "scripts" / "link_checker.py"
    if link_checker.exists():
        ok = run_cmd(f"python3 {link_checker}")
        if not ok:
            print("  ⚠️  链接检查有错误（见上文）")
            resp = input("  继续发布？[y/N]: ")
            if resp.lower() != 'y':
                print("已取消")
                return
    else:
        print("  ⏭️  跳过（link_checker.py 不存在）")
    
    # Step 3: push 到 GitHub
    step("推送到 GitHub（触发自动部署）")
    ok = run_cmd("git push origin main")
    if not ok:
        print("  ❌ 推送失败，请检查网络和 GitHub 认证")
        sys.exit(1)
    
    print(f"""
✅ 发布成功！

   约 1 分钟后访问: https://nktdrenzy-commits.github.io/jarvis-pages/
   查看 CI 状态:     https://github.com/nktdrenzy-commits/jarvis-pages/actions
    """)


if __name__ == '__main__':
    main()
