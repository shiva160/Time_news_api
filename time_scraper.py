#!/usr/bin/env python3


from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json


def fetch_html(url):
   
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None


def extract_stories(html):
    """
    Extract the latest 6 stories from Time.com HTML
    Uses basic string parsing - no external libraries, no regex
    """
    stories = []
    
    if not html:
        return stories
    
    # Find articles by searching for the pattern in the HTML
    # Pattern: \"id\":123,\"postType\":\"article\",\"title\":\"...\"...\"path\":\"...\"
    search_marker = ',\\"postType\\":\\"article\\",'
    seen_urls = set()
    
    # Start searching from the beginning
    pos = 0
    while len(stories) < 6:
        # Find next article marker
        pos = html.find(search_marker, pos)
        if pos == -1:
            break
        
        # Extract title - find the title field after the article marker
        title_marker = '\\"title\\":\\"'
        title_start = html.find(title_marker, pos, pos + 300)
        
        if title_start != -1:
            title_start += len(title_marker)
            # Find the closing quote for title
            title_end = title_start
            while title_end < len(html):
                if html[title_end] == '\\' and title_end + 1 < len(html) and html[title_end + 1] == '"':
                    break
                title_end += 1
            
            if title_end < len(html):
                title = html[title_start:title_end]
                
                # Extract path - find path field after title
                path_marker = '\\"path\\":\\"'
                path_start = html.find(path_marker, title_end, pos + 2000)
                
                if path_start != -1:
                    path_start += len(path_marker)
                    # Find the closing quote for path
                    path_end = path_start
                    while path_end < len(html):
                        if html[path_end] == '\\' and path_end + 1 < len(html) and html[path_end + 1] == '"':
                            break
                        path_end += 1
                    
                    if path_end < len(html):
                        path = html[path_start:path_end]
                        
                        # Clean up the path - remove ALL backslash escapes (may be double-escaped)
                        # First pass: remove one layer of escaping
                        clean_path = []
                        i = 0
                        while i < len(path):
                            if path[i] == '\\':
                                if i + 1 < len(path):
                                    clean_path.append(path[i + 1])
                                    i += 2
                                else:
                                    i += 1
                            else:
                                clean_path.append(path[i])
                                i += 1
                        
                        # Second pass: clean again if still has backslashes
                        first_clean = ''.join(clean_path)
                        final_path = []
                        i = 0
                        while i < len(first_clean):
                            if first_clean[i] == '\\':
                                if i + 1 < len(first_clean):
                                    final_path.append(first_clean[i + 1])
                                    i += 2
                                else:
                                    i += 1
                            else:
                                final_path.append(first_clean[i])
                                i += 1
                        path = ''.join(final_path)
                        
                        # Decode unicode escapes and HTML entities for title
                        title = decode_unicode_escapes(title)
                        title = decode_html_entities(title)
                        
                        # Build full URL
                        full_url = f"https://time.com{path}"
                        
                        # Avoid duplicates and filter out section titles
                        if full_url not in seen_urls and len(path) > 5 and path.count('/') > 1:
                            seen_urls.add(full_url)
                            stories.append({
                                "title": title,
                                "link": full_url
                            })
        
        # Move to next position
        pos += len(search_marker)
    
    return stories[:6]


def decode_unicode_escapes(text):
    """Decode unicode escape sequences like \\u0026"""
    result = []
    i = 0
    while i < len(text):
        if i + 5 < len(text) and text[i:i+2] == '\\u':
            # Found a unicode escape sequence
            hex_code = text[i+2:i+6]
            try:
                char = chr(int(hex_code, 16))
                result.append(char)
                i += 6
                continue
            except:
                pass
        result.append(text[i])
        i += 1
    return ''.join(result)


def decode_html_entities(text):
    """Decode common HTML entities"""
    entities = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&apos;': "'",
        '&#x27;': "'",
        '&mdash;': '—',
        '&ndash;': '–',
        '&rsquo;': ''',
        '&lsquo;': ''',
        '&rdquo;': '"',
        '&ldquo;': '"',
    }
    
    for entity, char in entities.items():
        text = text.replace(entity, char)
    
    return text


class TimeStoriesHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the Time Stories API"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/getTimeStories':
            try:
                # Fetch and parse stories
                print("Fetching Time.com...")
                html = fetch_html('https://time.com')
                print(f"HTML fetched: {len(html) if html else 0} characters")
                
                stories = extract_stories(html)
                print(f"Extracted {len(stories)} stories")
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Write JSON response
                response = json.dumps(stories, indent=2, ensure_ascii=False)
                self.wfile.write(response.encode('utf-8'))
                
            except Exception as e:
                # Error response
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = json.dumps({
                    "error": str(e)
                })
                self.wfile.write(error_response.encode('utf-8'))
        else:
            # 404 for other paths
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found. Use /getTimeStories endpoint.')
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8080):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TimeStoriesHandler)
    print(f"✅ Time Stories API Server running on http://localhost:{port}")
    print(f"📡 Access the API at: http://localhost:{port}/getTimeStories")
    print(f"Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped.")
        httpd.server_close()


if __name__ == '__main__':
    run_server()
