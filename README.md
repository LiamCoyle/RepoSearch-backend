# GitHub Repository Search - Backend API

A Flask REST API that serves as a proxy to the GitHub API, providing endpoints for searching repositories and retrieving repository analytics.

## Features

- 🔍 **Repository Search**: Search GitHub repositories using GitHub's search API
- 📊 **Repository Details**: Get detailed information about repositories by ID or owner/repo
- 📝 **Commit History**: Retrieve commit history (last 100 commits)
- 👥 **Contributor Management**: Fetch repository contributors with pagination support
- 🏥 **Health Check**: Health monitoring endpoint
- 🔒 **CORS Support**: Configured for frontend integration


## Tech Stack

- **Framework**: Flask 3.1.2
- **Language**: Python 3


## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Create a virtual environment (recommended):

```bash
python -m venv venv
```

2. Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the backend directory (optional):

```env
PORT=5000
FLASK_DEBUG=false
FRONTEND_URL=http://localhost:3000
```

### Running the Server

**Development:**
```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

## API Endpoints

### Health Check

**GET** `/health`

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "Wiremind Technical Test API"
}
```

### Search Repositories

**GET** `/github/search?query={search_query}`

Search for GitHub repositories.

**Parameters:**
- `query` (required): Search query string

**Response:**
```json
{
  "total_count": 1000,
  "items": [...]
}
```

### Get Repository Details

**GET** `/github/get_repository_details?owner={owner}&repo={repo}`

Get repository details by owner and repository name.

**Parameters:**
- `owner` (required): Repository owner (username or organization)
- `repo` (required): Repository name

**GET** `/github/get_repository_by_id?id={id}`

Get repository details by repository ID.

**Parameters:**
- `id` (required): Repository ID

### Get Repository Commits

**GET** `/github/get_repository_commits?owner={owner}&repo={repo}&per_page={per_page}`

Get repository commits.

**Parameters:**
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `per_page` (optional): Number of commits per page (default: 100, max: 100)

**Response:**
Array of commit objects with author, committer, and commit information.

### Get Repository Contributors

**GET** `/github/get_repository_contributors?owner={owner}&repo={repo}&per_page={per_page}&page={page}`

Get repository contributors with pagination support.

**Parameters:**
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `per_page` (optional): Number of contributors per page (default: 100, max: 100)
- `page` (optional): Page number (default: 1)

**Response:**
Array of contributor objects sorted by total contributions (descending).

**Note:** GitHub API only links the first 500 author email addresses to GitHub users. The rest appear as anonymous contributors.

## Project Structure

```
backend/
├── app.py                 # Flask application entry point
├── routes/                # API route handlers
│   ├── github.py         # GitHub-related endpoints
│   └── health.py         # Health check endpoint
├── services/              # Business logic
│   └── github.py         # GitHub API service
├── utils/                 # Utility functions
│   └── logger.py         # Logging configuration
├── logs/                  # Application logs
├── requirements.txt       # Python dependencies
└── .env                  # Environment variables (optional)
```

## GitHub API Integration

The backend acts as a proxy to the GitHub API, using the following endpoints:

- `GET /search/repositories` - Search repositories
- `GET /repos/{owner}/{repo}` - Get repository details
- `GET /repositories/{id}` - Get repository by ID
- `GET /repos/{owner}/{repo}/commits` - Get repository commits
- `GET /repos/{owner}/{repo}/contributors` - Get repository contributors

All requests use the GitHub API v3 and include proper headers for authentication and rate limiting.

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (missing required parameters)
- `500` - Internal Server Error

Error responses include a JSON object with an `error` field:

```json
{
  "error": "Error message here"
}
```


## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `5000` |
| `FLASK_DEBUG` | Enable debug mode | `false` |
| `FRONTEND_URL` | Allowed CORS origins | `http://localhost:3000` |

## Development

### Running in Debug Mode

Set `FLASK_DEBUG=true` in your `.env` file or environment variables to enable Flask's debug mode.

### Testing Endpoints

You can test the API using curl or any HTTP client:

```bash
# Health check
curl http://localhost:5000/health

# Search repositories
curl "http://localhost:5000/github/search?query=react"

# Get repository details
curl "http://localhost:5000/github/get_repository_details?owner=facebook&repo=react"
```

## Rate Limiting

The GitHub API has rate limits:
- **Unauthenticated**: 60 requests per hour per IP
- **Authenticated**: 5,000 requests per hour




