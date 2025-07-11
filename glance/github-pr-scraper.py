#!/usr/bin/env python3
import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import socketserver
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote

class GitHubPRHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/health':
                self.send_health_response()
                return
            elif self.path == '/my-open-prs.xml':
                self.send_rss_response()
                return
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Not found')
                
        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_error_response(f"Server error: {str(e)[:50]}")

    def fetch_github_user(self, github_token):
        """Fetch current GitHub user"""
        try:
            headers = {
                'Authorization': f'Bearer {github_token}',
                'User-Agent': 'github-pr-scraper',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'username': data.get('login'),
                    'status': 'success'
                }
            else:
                return {
                    'username': None,
                    'status': 'error',
                    'error': f'HTTP {response.status_code}'
                }
        except Exception as e:
            return {
                'username': None,
                'status': 'error',
                'error': str(e)[:50]
            }

    def fetch_open_pull_requests(self, username, github_token):
        """Fetch user's open pull requests from PlayerData organization"""
        try:
            headers = {
                'Authorization': f'Bearer {github_token}',
                'User-Agent': 'github-pr-scraper',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            search_query = f'is:pr is:open author:{username} org:PlayerData'
            encoded_query = quote(search_query)
            
            response = requests.get(
                f'https://api.github.com/search/issues?q={encoded_query}&sort=updated&per_page=50',
                headers=headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                prs = data.get('items', [])
                
                # Process PRs to extract relevant information
                processed_prs = []
                for pr in prs:
                    repo_url_parts = pr.get('repository_url', '').split('/')
                    repo_name = repo_url_parts[-1] if repo_url_parts else 'unknown'
                    repo_owner = repo_url_parts[-2] if len(repo_url_parts) > 1 else 'unknown'
                    
                    processed_prs.append({
                        'title': pr.get('title', 'No title'),
                        'url': pr.get('html_url', ''),
                        'repo_name': repo_name,
                        'repo_owner': repo_owner,
                        'full_repo_name': f'{repo_owner}/{repo_name}',
                        'created_at': pr.get('created_at', ''),
                        'updated_at': pr.get('updated_at', ''),
                        'state': pr.get('state', 'unknown'),
                        'body': pr.get('body', ''),
                        'labels': [label.get('name', '') for label in pr.get('labels', [])]
                    })
                
                return {
                    'prs': processed_prs,
                    'total_count': data.get('total_count', 0),
                    'status': 'success'
                }
            else:
                return {
                    'prs': [],
                    'total_count': 0,
                    'status': 'error',
                    'error': f'HTTP {response.status_code}'
                }
                
        except Exception as e:
            return {
                'prs': [],
                'total_count': 0,
                'status': 'error',
                'error': str(e)[:50]
            }

    def generate_rss_feed(self, prs, username):
        """Generate RSS feed from pull requests"""
        # Create root RSS element
        rss = ET.Element('rss', version='2.0')
        channel = ET.SubElement(rss, 'channel')
        
        # Channel metadata
        ET.SubElement(channel, 'title').text = f"{username}'s Open Pull Requests"
        ET.SubElement(channel, 'description').text = f"Open pull requests authored by {username}"
        ET.SubElement(channel, 'link').text = "https://github.com/pulls"
        ET.SubElement(channel, 'lastBuildDate').text = datetime.now().isoformat()
        ET.SubElement(channel, 'generator').text = "GitHub PR Scraper"
        
        # Add items for each PR
        for pr in prs:
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = f"[{pr['full_repo_name']}] {pr['title']}"
            ET.SubElement(item, 'link').text = pr['url']
            ET.SubElement(item, 'guid').text = pr['url']
            ET.SubElement(item, 'category').text = pr['full_repo_name']
            
            # Format dates
            try:
                created_date = datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00')).strftime('%a, %d %b %Y %H:%M:%S %z')
                updated_date = datetime.fromisoformat(pr['updated_at'].replace('Z', '+00:00')).strftime('%a, %d %b %Y %H:%M:%S %z')
            except:
                created_date = pr['created_at']
                updated_date = pr['updated_at']
            
            ET.SubElement(item, 'pubDate').text = updated_date
            
            # Create description
            description = f"""
<strong>Repository:</strong> {pr['full_repo_name']}<br/>
<strong>Status:</strong> {pr['state']}<br/>
<strong>Created:</strong> {created_date}<br/>
<strong>Updated:</strong> {updated_date}<br/>
<strong>Labels:</strong> {', '.join(pr['labels']) if pr['labels'] else 'None'}<br/>
<br/>
{pr['body'] if pr['body'] else 'No description provided'}
"""
            
            # Use CDATA for description to preserve formatting
            desc_elem = ET.SubElement(item, 'description')
            desc_elem.text = description
        
        # Convert to string with XML declaration
        xml_str = ET.tostring(rss, encoding='unicode')
        return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'

    def send_rss_response(self):
        """Generate and send RSS feed response"""
        try:
            # Get GitHub credentials from environment
            github_token = os.getenv('GITHUB_KEY') or os.getenv('GITHUB_TOKEN')
            github_username = os.getenv('GITHUB_USERNAME')
            
            if not github_token:
                self.send_error_rss_response("GITHUB_KEY environment variable not set")
                return
            
            # Get username if not provided
            if not github_username:
                user_result = self.fetch_github_user(github_token)
                if user_result['status'] != 'success':
                    self.send_error_rss_response(f"Failed to get GitHub user: {user_result.get('error', 'Unknown error')}")
                    return
                github_username = user_result['username']
            
            # Fetch pull requests
            pr_result = self.fetch_open_pull_requests(github_username, github_token)
            
            if pr_result['status'] != 'success':
                self.send_error_rss_response(f"Failed to fetch PRs: {pr_result.get('error', 'Unknown error')}")
                return
            
            # Generate RSS feed
            rss_content = self.generate_rss_feed(pr_result['prs'], github_username)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/rss+xml; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(rss_content.encode('utf-8'))
            
            print(f"Generated RSS feed with {len(pr_result['prs'])} PRs for {github_username}")
            
        except Exception as e:
            print(f"Error generating RSS response: {e}")
            self.send_error_rss_response(f"Server error: {str(e)[:50]}")

    def send_error_rss_response(self, error_message):
        """Send error response in RSS format"""
        try:
            rss = ET.Element('rss', version='2.0')
            channel = ET.SubElement(rss, 'channel')
            
            ET.SubElement(channel, 'title').text = "GitHub PR Scraper Error"
            ET.SubElement(channel, 'description').text = error_message
            ET.SubElement(channel, 'link').text = "https://github.com"
            ET.SubElement(channel, 'lastBuildDate').text = datetime.now().isoformat()
            
            # Add error item
            item = ET.SubElement(channel, 'item')
            ET.SubElement(item, 'title').text = "Configuration Error"
            ET.SubElement(item, 'description').text = error_message
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            
            xml_str = ET.tostring(rss, encoding='unicode')
            rss_content = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/rss+xml; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(rss_content.encode('utf-8'))
        except Exception as e:
            print(f"Error sending error RSS response: {e}")

    def send_health_response(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"healthy","timestamp":"' + datetime.now().isoformat().encode() + b'"}')
        except Exception as e:
            print(f"Error sending health response: {e}")

    def send_error_response(self, error_message):
        try:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(error_message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending error response: {e}")

    def log_message(self, format, *args):
        # Enable logging for debugging
        print(f"{datetime.now()}: {format % args}")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in separate threads."""
    daemon_threads = True

if __name__ == '__main__':
    # Bind to 0.0.0.0 for Docker container compatibility
    server_address = ('0.0.0.0', 8086)
    httpd = ThreadedHTTPServer(server_address, GitHubPRHandler)
    print(f"GitHub PR Scraper server running on http://{server_address[0]}:{server_address[1]}")
    print(f"RSS feed available at: http://{server_address[0]}:{server_address[1]}/my-open-prs.xml")
    print(f"Health check at: http://{server_address[0]}:{server_address[1]}/health")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down GitHub PR scraper server...")
        httpd.shutdown()