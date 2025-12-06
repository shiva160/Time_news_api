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

## 🔧 Configuration

### Change Port
Edit the last line in `time_scraper.py`:
```python
if __name__ == '__main__':
    run_server(port=3000)  # Change to your desired port
```

### Change Number of Stories
Modify the return statement in `extract_stories()`:
```python
return stories[:10]  # Change 6 to any number
```

## 📂 Project Structure

```
.
├── time_scraper.py          # Main API server (REQUIRED)
├── README.md                # This file
├── test_scraper.py          # Test script (optional)
├── demo.py                  # Demo script (optional)
├── verify_format.py         # Format validator (optional)
├── final_verification.sh    # Full test suite (optional)
└── start_server.sh          # Quick start script (optional)
```

## 🚢 Deployment

### Local
```bash
python3 time_scraper.py
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY time_scraper.py .
EXPOSE 8080
CMD ["python3", "time_scraper.py"]
```

### Cloud Platforms
Works on any platform with Python 3:
- AWS EC2
- Google Cloud Platform
- Azure
- Heroku
- DigitalOcean

## ⚠️ Limitations

- Single-threaded server (suitable for development/testing)
- No authentication
- No rate limiting
- Depends on Time.com's HTML structure

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - Free to use for any purpose.

## 🎯 Assignment Context

This project was created as a solution to scrape Time.com stories without using:
- External parsing libraries (BeautifulSoup, lxml, etc.)
- Regular expressions
- Any external dependencies

Built with only Python standard library using basic string operations.

---

**Made with ❤️ using pure Python**
