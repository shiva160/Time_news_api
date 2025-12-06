# Time.com Stories Scraper API

A lightweight Python web service that scrapes the latest 6 stories from Time.com and serves them via a REST API.

## ✨ Features

- ✅ **Zero Dependencies** - Uses only Python standard library
- ✅ **No Regex** - Pure string parsing with basic operations
- ✅ **Simple API** - Single GET endpoint
- ✅ **Clean JSON** - Returns `[{"title": "...", "link": "..."}]`
- ✅ **Easy to Deploy** - Just run one Python file

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- Internet connection

### Installation

1. Clone the repository:
```bash
git clone https://github.com/shiva160/Time_news_api/
cd time-scraper-api
```

2. Run the server:
```bash
python3 time_scraper.py
```

The server will start on `http://localhost:8080`

### Usage

#### Start the Server
```bash
python3 time_scraper.py
```

#### Make API Request
```bash
curl http://localhost:8080/getTimeStories
```

#### Response Format
```json
[
  {
    "title": "Story Title Here",
    "link": "https://time.com/article-path/"
  },
  ...
]
```

## 📡 API Documentation

### Endpoint
```
GET /getTimeStories
```

### Response
- **Status Code**: 200 OK
- **Content-Type**: application/json
- **Body**: Array of 6 story objects

### Example Response
```json
[
  {
    "title": "Hegseth Says U.S. 'Just Sunk Another Narco Boat'",
    "link": "https://time.com/7338857/hegseth-confirms-another-boat-strike-controversy-war-crime-debate/"
  },
  {
    "title": "How Hong Kong Is Stamping Out Discontent Over Fire",
    "link": "https://time.com/7338838/hong-kong-fire-arrests-national-security/"
  }
]
```

## 🧪 Testing

Run the test script to verify functionality:

```bash
python3 test_scraper.py
```

Run the full verification:

```bash
./final_verification.sh
```

## 🛠️ Technical Details

### Technology Stack
- **Language**: Python 3
- **HTTP Server**: `http.server` (standard library)
- **HTML Fetching**: `urllib.request` (standard library)
- **Parsing**: Pure string operations (find, slice, loops)
- **JSON**: `json` module (standard library)

### No External Dependencies
```bash
$ grep "^import\|^from" time_scraper.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json
```

All imports are from Python standard library! ✅

### Parsing Strategy
- Uses `str.find()` and `str.rfind()` to locate patterns
- Manual string slicing to extract data
- Character-by-character parsing with while loops
- No regex patterns - pure string operations only

