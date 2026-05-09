#!/usr/bin/env python3
"""
local_preview.py - 启动本地静态服务器预览网站
用法: python3 scripts/local_preview.py [端口]
"""

import http.server
import socketserver
import os
import sys
import shutil
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

class TailoredHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义 Handler，支持中文文件名"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # 添加缓存控制，避免浏览器缓存旧版本
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # 彩色化日志输出
        print(f"\033[92m  → \033[0m {args[0]}")


def find_free_port(start_port):
    """找到第一个可用端口"""
    import socket
    port = start_port
    while port < start_port + 10:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            port += 1
    return None


if __name__ == '__main__':
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    port = find_free_port(PORT)
    if port is None:
        print("❌ 无法找到可用端口")
        sys.exit(1)
    
    print(f"""
╔══════════════════════════════════════════════╗
║       Jarvis Pages - 本地预览服务器           ║
╠══════════════════════════════════════════════╣
║  目录: {project_root}
║  端口: http://localhost:{port}
║  按 Ctrl+C 停止服务器
╚══════════════════════════════════════════════╝
    """)
    
    with socketserver.TCPServer(("", port), TailoredHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ 服务器已停止")
