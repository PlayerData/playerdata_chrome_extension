#!/usr/bin/env python3
import json
import os
import socketserver
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests


class IncidentTimerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/health':
                self.send_health_response()
                return

            # Get access token from environment
            access_token = os.getenv('PAGER_KEY')
            if not access_token:
                self.send_error_response("PAGER_KEY environment variable not set")
                return

            # Fetch the most recent incident
            incident_data = self.fetch_last_incident(access_token)

            if incident_data['status'] != 'success':
                self.send_error_response(incident_data.get('error', 'Unknown error'))
                return

            # Generate HTML content
            html_content = self.generate_html(incident_data)

            # Send response with Glance extension headers
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Widget-Title', 'Time Since Last Incident')
            self.send_header('Widget-Content-Type', 'html')
            self.end_headers()

            self.wfile.write(html_content.encode('utf-8'))

        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_error_response(f"Server error: {str(e)[:50]}")

    def fetch_last_incident(self, access_token):
        """Fetch the most recent open incident, or most recent resolved incident if no open ones"""
        try:
            headers = {
                'Accept': 'application/vnd.pagerduty+json;version=2',
                'Content-Type': 'application/json',
                'Authorization': f'Token token={access_token}'
            }

            # First, try to get the most recent open incident (triggered or acknowledged)
            # Sort by created_at:desc to get most recent first
            open_url = 'https://api.pagerduty.com/incidents?total=true&time_zone=UTC&limit=1&sort_by=created_at:desc&statuses%5B%5D=triggered&statuses%5B%5D=acknowledged'
            response = requests.get(open_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                incidents = data.get('incidents', [])
                total_open = data.get('total', 0)

                if incidents:
                    # Found an open incident
                    incident = incidents[0]
                    return {
                        'status': 'success',
                        'incident': incident,
                        'has_incident': True,
                        'incident_type': 'open',
                        'total_open_incidents': total_open
                    }

            # No open incidents found, look for the most recent resolved incident
            resolved_url = 'https://api.pagerduty.com/incidents?total=false&time_zone=UTC&limit=1&sort_by=created_at:desc&statuses%5B%5D=resolved'
            response = requests.get(resolved_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                incidents = data.get('incidents', [])

                if incidents:
                    # Found a resolved incident
                    incident = incidents[0]
                    return {
                        'status': 'success',
                        'incident': incident,
                        'has_incident': True,
                        'incident_type': 'resolved',
                        'total_open_incidents': 0
                    }
                else:
                    return {
                        'status': 'success',
                        'has_incident': False,
                        'total_open_incidents': 0
                    }
            else:
                return {
                    'status': 'error',
                    'error': f'HTTP {response.status_code}: {response.text[:100]}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def generate_html(self, incident_data):
        """Generate HTML content for the widget"""
        if not incident_data.get('has_incident'):
            return '''<div>
<div class="size-h4 color-subtext">No incident data available</div>
</div>'''

        incident = incident_data['incident']
        incident_type = incident_data.get('incident_type', 'unknown')
        total_open_incidents = incident_data.get('total_open_incidents', 0)

        # Get incident details
        incident_title = incident.get('title', 'Unknown incident')
        incident_url = incident.get('html_url', '')
        incident_status = incident.get('status', 'unknown')
        service_name = incident.get('service', {}).get('summary', 'Unknown service')

        # Handle active incidents vs resolved incidents
        if incident_type == 'open':
            # Active incident - show 0 time since last incident
            time_display = "0 hours"
            color_class = "color-negative"  # Red for active incidents
            time_message = "Current active incident"

            # Show count of open incidents
            if total_open_incidents > 1:
                header_text = f"🚨 Active Incidents ({total_open_incidents} total)"
                incident_context = "Most recent:"
            else:
                header_text = "🚨 Active Incident"
                incident_context = ""
        else:
            # Resolved incident - calculate time since it was created
            created_at_str = incident.get('created_at', '')
            try:
                # Parse ISO format timestamp
                created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                now = datetime.now(created_at.tzinfo)

                # Calculate time difference
                time_diff = now - created_at
                hours_since = time_diff.total_seconds() / 3600

                # Format the time display
                if hours_since < 24:
                    time_display = f"{hours_since:.0f} hours"
                else:
                    days_since = hours_since / 24
                    time_display = f"{days_since:.2f} days"

                # Color based on time since incident
                if hours_since < 24:
                    color_class = "color-positive"  # Green for recent resolution (< 24 hours)
                elif hours_since < 168:  # 1 week
                    color_class = "color-primary"   # Blue for moderate time (1-7 days)
                else:
                    color_class = "color-positive"  # Green for long time (> 1 week)

                time_message = f"Since last incident"
                header_text = "Most Recent Incident:"
                incident_context = ""

            except Exception as e:
                print(f"Error parsing timestamp: {e}")
                time_display = "Unknown"
                color_class = "color-subtext"
                time_message = "Time calculation error"
                header_text = "Most Recent Incident:"
                incident_context = ""

        # Generate HTML
        html = f'''<div>
<div class="{color_class} size-h3">
{time_display}
</div>
<div class="size-h6 color-subtext margin-top-5">
{time_message}
</div>
<hr class="margin-block-10">
<div class="margin-block-5">
<div class="size-h5 {'color-negative' if incident_type == 'open' else ''}">{header_text}</div>'''

        # Add context for multiple incidents
        if incident_context:
            html += f'''<div class="size-h6 color-subtext margin-top-2">{incident_context}</div>'''

        if incident_url:
            html += f'''<a href="{incident_url}" class="color-primary" style="text-decoration: none;">
{incident_title}
</a>'''
        else:
            html += f'''<div class="size-h6">{incident_title}</div>'''

        html += f'''
<div class="size-h6 color-subtext margin-top-2">
Service: {service_name}
</div>
<div class="size-h6 color-subtext">
Status: {incident_status.title()}
</div>
</div>
<hr class="margin-block-10">
<div class="size-h6 color-subdue">
Last updated: {datetime.now().strftime('%H:%M:%S')} UTC
</div>
</div>'''

        return html

    def send_error_response(self, error_message):
        try:
            html_content = f'''<div>
<div class="size-h4 color-negative">Error</div>
<div class="size-h6 color-subtext margin-top-5">{error_message}</div>
</div>'''

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Widget-Title', 'Time Since Last Incident')
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
    """Handle requests in a separate thread."""
    pass


if __name__ == '__main__':
    # Bind to 0.0.0.0 for Docker container compatibility
    server_address = ('0.0.0.0', 8088)
    httpd = ThreadedHTTPServer(server_address, IncidentTimerHandler)
    print(f"Incident Timer Extension server running on http://{server_address[0]}:{server_address[1]}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down incident timer server...")
        httpd.shutdown()
