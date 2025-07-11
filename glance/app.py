#!/usr/bin/env python3
import os
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import socketserver
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class MergeFreezeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/health':
                self.send_health_response()
                return

            # Repository configurations
            repositories = [
                {"name": "app", "url": "https://www.mergefreeze.com/api/branches/PlayerData/app/master/"},
                {"name": "api", "url": "https://www.mergefreeze.com/api/branches/PlayerData/api/master/"},
                {"name": "web", "url": "https://www.mergefreeze.com/api/branches/PlayerData/web/master/"},
                {"name": "analysis-services", "url": "https://www.mergefreeze.com/api/branches/PlayerData/analysis-services/master/"},
                {"name": "actions", "url": "https://www.mergefreeze.com/api/branches/PlayerData/actions/main/"},
            ]

            # Get access token from environment
            access_token = os.getenv('MERGE_APP_KEY')
            if not access_token:
                self.send_error_response("MERGE_APP_KEY environment variable not set")
                return

            # Fetch status for all repositories concurrently
            repo_statuses = self.fetch_all_repos_concurrent(repositories, access_token)

            # Generate HTML content
            html_content = self.generate_html(repo_statuses)

            # Send response with Glance extension headers
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Widget-Title', 'Merge Freeze Status')
            self.send_header('Widget-Content-Type', 'html')
            self.end_headers()

            self.wfile.write(html_content.encode('utf-8'))

        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_error_response(f"Server error: {str(e)[:50]}")

    def fetch_repo_status(self, repo, access_token):
        """Fetch status for a single repository"""
        try:
            response = requests.get(f"{repo['url']}?access_token={access_token}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "name": repo["name"],
                    "frozen": data.get("frozen", False),
                    "frozen_by": data.get("frozen_by", ""),
                    "status": "success"
                }
            else:
                return {
                    "name": repo["name"],
                    "frozen": None,
                    "frozen_by": "",
                    "status": "error",
                    "error": f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                "name": repo["name"],
                "frozen": None,
                "frozen_by": "",
                "status": "error",
                "error": str(e)[:50]  # Truncate long error messages
            }

    def fetch_all_repos_concurrent(self, repositories, access_token):
        """Fetch all repository statuses concurrently"""
        repo_statuses = []

        # Use ThreadPoolExecutor to make concurrent requests
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all requests
            future_to_repo = {
                executor.submit(self.fetch_repo_status, repo, access_token): repo
                for repo in repositories
            }

            # Collect results as they complete (with timeout)
            for future in as_completed(future_to_repo, timeout=15):
                try:
                    result = future.result()
                    repo_statuses.append(result)
                except Exception as e:
                    repo = future_to_repo[future]
                    repo_statuses.append({
                        "name": repo["name"],
                        "frozen": None,
                        "frozen_by": "",
                        "status": "error",
                        "error": f"Timeout: {str(e)[:30]}"
                    })

        return repo_statuses

    def generate_html(self, repo_statuses):
        # Count frozen/unfrozen repositories
        frozen_count = sum(1 for repo in repo_statuses if repo["frozen"] is True)
        total_count = len([repo for repo in repo_statuses if repo["status"] == "success"])
        error_count = len([repo for repo in repo_statuses if repo["status"] == "error"])

        # Generate summary
        if error_count > 0:
            summary_color = "color-negative"
            summary_text = f"{error_count} error(s)"
        elif frozen_count > 0:
            summary_color = "color-primary"
            summary_text = f"{frozen_count}/{total_count} frozen"
        else:
            summary_color = "color-positive"
            summary_text = f"All {total_count} unfrozen"

        html = f'''<div>
<div class="margin-bottom-10">
<span class="size-h3 {summary_color}">🔒 {summary_text}</span>
</div>
<hr class="margin-block-10">
<ul class="list list-gap-8">'''

        # Sort repositories: errors first, then frozen, then unfrozen
        def sort_key(repo):
            if repo["status"] == "error":
                return (0, repo["name"])  # Errors first
            elif repo["frozen"]:
                return (1, repo["name"])  # Frozen second
            else:
                return (2, repo["name"])  # Unfrozen last

        sorted_repos = sorted(repo_statuses, key=sort_key)

        for repo in sorted_repos:
            if repo["status"] == "error":
                html += f'''<li class="list-item">
<div class="flex justify-between items-center">
<span class="size-h4">{repo["name"]}</span>
<span class="color-negative">❌ Error</span>
</div>
<div class="size-h6 color-subdue">{repo["error"]}</div>
</li>'''
            elif repo["frozen"]:
                html += f'''<li class="list-item">
<div class="flex justify-between items-center">
<span class="size-h4">{repo["name"]}</span>
<span class="color-primary">❄️ Frozen</span>
</div>
<div class="size-h6 color-subdue">by {repo["frozen_by"]}</div>
</li>'''
            else:
                html += f'''<li class="list-item">
<div class="flex justify-between items-center">
<span class="size-h4">{repo["name"]}</span>
<span class="color-positive">✅ Unfrozen</span>
</div>
</li>'''

        html += f'''</ul>
<hr class="margin-block-10">
<div class="size-h6 color-subdue">
Last updated: {datetime.now().strftime('%H:%M:%S')}
</div>
</div>'''

        return html

    def send_error_response(self, error_message):
        try:
            html_content = f'''<div>
<div class="size-h3 color-negative">Configuration Error</div>
<div class="size-h5 color-subdue margin-top-5">{error_message}</div>
</div>'''

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Widget-Title', 'Merge Freeze Status')
            self.send_header('Widget-Content-Type', 'html')
            self.end_headers()

            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            print(f"Error sending error response: {e}")

    def send_health_response(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"healthy"}')
        except Exception as e:
            print(f"Error sending health response: {e}")

    def log_message(self, format, *args):
        # Enable logging for debugging
        print(f"{datetime.now()}: {format % args}")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in separate threads."""
    daemon_threads = True

if __name__ == '__main__':
    # Bind to 0.0.0.0 for Docker container compatibility
    server_address = ('0.0.0.0', 8081)
    httpd = ThreadedHTTPServer(server_address, MergeFreezeHandler)
    print(f"Merge Freeze Extension server running on http://{server_address[0]}:{server_address[1]}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down extension server...")
        httpd.shutdown()
