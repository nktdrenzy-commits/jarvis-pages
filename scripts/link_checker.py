#!/usr/bin/env python3
"""
link_checker.py - 检查所有 HTML 文件中的内部链接是否有效
用法: python3 scripts/link_checker.py [html目录]
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

def extract_links(html_content, base_url):
    """从 HTML 内容中提取所有 href 和 src 链接"""
    links = set()
    
    # 提取 href 链接
    href_pattern = re.compile(r'href=["\']([^"\']+)["\']')
    for match in href_pattern.finditer(html_content):
        links.add(match.group(1))
    
    # 提取 src 链接
    src_pattern = re.compile(r'src=["\']([^"\']+)["\']')
    for match in src_pattern.finditer(html_content):
        links.add(match.group(1))
    
    return links

def is_internal_link(link, base_url):
    """判断是否为内部链接"""
    parsed = urlparse(link)
    
    # 绝对 URL
    if parsed.scheme:
        return parsed.netloc == urlparse(base_url).netloc
    
    # 锚点链接
    if link.startswith('#'):
        return True
    
    # JavaScript 链接
    if link.startswith('javascript:'):
        return True
    
    # 外部链接（跳过）
    if parsed.netloc:
        return False
    
    return True

def normalize_path(link, current_file):
    """将相对链接转换为绝对文件路径"""
    if link.startswith('#') or link.startswith('javascript:'):
        return None
    
    base_dir = os.path.dirname(current_file)
    target = os.path.normpath(os.path.join(base_dir, link))
    return target

def check_links(html_dir):
    """检查目录下所有 HTML 文件的内部链接"""
    html_dir = Path(html_dir)
    results = []
    
    for html_file in html_dir.rglob('*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        base_url = f"file://{html_file}"
        links = extract_links(content, base_url)
        
        for link in links:
            if not is_internal_link(link, base_url):
                continue
            
            # 跳过外部链接和锚点
            if link.startswith('#') or link.startswith('javascript:'):
                continue
            
            target_path = normalize_path(link, html_file)
            if target_path is None:
                continue
            
            # 检查文件是否存在
            if not os.path.exists(target_path):
                rel_file = os.path.relpath(html_file, html_dir)
                rel_link = os.path.relpath(target_path, html_dir)
                results.append((rel_file, link, rel_link, "❌ 文件不存在"))
            else:
                results.append((os.path.relpath(html_file, html_dir), link, "", "✅ 正常"))
    
    return results

if __name__ == '__main__':
    html_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"🔍 检查目录: {html_dir}\n")
    results = check_links(html_dir)
    
    errors = [r for r in results if r[3].startswith('❌')]
    ok = [r for r in results if r[3].startswith('✅')]
    
    if errors:
        print(f"⚠️  发现 {len(errors)} 个失效链接:\n")
        for file, link, target, status in errors:
            print(f"  {file}")
            print(f"    链接: {link}")
            print(f"    目标: {target}")
            print(f"    状态: {status}\n")
    
    print(f"✅ 共检查 {len(results)} 个链接，{len(ok)} 正常，{len(errors)} 失效")
    
    sys.exit(1 if errors else 0)
