#!/usr/bin/env python3


import sys
sys.path.insert(0, '/home/shiva/Downloads/VIBE')

from time_scraper import fetch_html, extract_stories
import json

print(" Testing Time.com Story Scraper...")
print("=" * 60)

# Fetch HTML
print("\n1️ Fetching HTML from Time.com...")
html = fetch_html('https://time.com')

if html:
    print(f" Successfully fetched {len(html)} characters of HTML")
    
    # Extract stories
    print("\n2️ Extracting latest 6 stories...")
    stories = extract_stories(html)
    
    print(f" Found {len(stories)} stories\n")
    
    # Display results
    print("=" * 60)
    print(" LATEST STORIES FROM TIME.COM")
    print("=" * 60)
    print(json.dumps(stories, indent=2, ensure_ascii=False))
    print("=" * 60)
    
    # Verify format
    print("\n3️ Verifying JSON format...")
    if len(stories) > 0:
        if all('title' in s and 'link' in s for s in stories):
            print(" All stories have 'title' and 'link' fields")
        else:
            print(" Some stories missing required fields")
            
        if len(stories) == 6:
            print(" Exactly 6 stories returned")
        else:
            print(f"  {len(stories)} stories returned (expected 6)")
    else:
        print(" No stories found")
else:
    print(" Failed to fetch HTML")

print("\n" + "=" * 60)
print(" To run the API server, execute:")
print("   python3 time_scraper.py")
print("\n   Then access: http://localhost:8080/getTimeStories")
print("=" * 60)
