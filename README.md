# GitHub Repository Search - Backend API

A Flask REST API that serves as a proxy to the GitHub API, providing endpoints for searching repositories and retrieving repository analytics.

## Features

- 🔍 **Repository Search**: Search GitHub repositories using GitHub's search API with pagination support
- 📊 **Repository Details**: Get detailed information about repositories by ID
- 📝 **Commit History**: Retrieve commit history with configurable page size
- 👥 **Contributor Management**: Fetch all repository contributors (including anonymous contributors)
- 💻 **Language Analytics**: Get repository languages with byte counts
- 🐛 **Issue Tracking**: Retrieve repository issues


## Tech Stack

- **Framework**: Flask 3.1.2
- **Language**: Python 3


## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the backend directory:

```env
PORT=5000
FLASK_DEBUG=false
FRONTEND_URL=http://localhost:3000
GITHUB_ACCESS_TOKEN=your_github_personal_access_token_here
```

**Note:** The `GITHUB_ACCESS_TOKEN` is optional but highly recommended. If provided, all GitHub API requests will be authenticated using a Bearer token in the Authorization header, which increases the rate limit from 60 requests/hour (unauthenticated) to 5,000 requests/hour (authenticated).


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

**GET** `/github/search?query={search_query}&per_page={per_page}&page={page}`

Search for GitHub repositories.

**Parameters:**
- `query` (required): Search query string
- `per_page` (optional): Number of results per page (default: 10, max: 100)
- `page` (optional): Page number (default: 1)

**Response:**
```json
{
  "total_count": 1000,
  "incomplete_results": false,
  "items": [
    {
      "id": 10270250,
      "name": "react",
      "full_name": "facebook/react",
      "description": "A declarative, efficient, and flexible JavaScript library...",
      "stargazers_count": 230000,
      "forks_count": 48000,
      "language": "JavaScript",
      "updated_at": "2024-01-15T10:30:00Z",
      ...
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:5000/github/search?query=react&per_page=20&page=1"
```

### Get Repository by ID

**GET** `/github/get_repository_by_id?id={id}`

Get repository details by repository ID.

**Parameters:**
- `id` (required): Repository ID (numeric)

**Response:**
Repository object with full details including name, description, stars, forks, language, and more.

**Example:**
```bash
curl "http://localhost:5000/github/get_repository_by_id?id=10270250"
```

### Get Repository Commits

**GET** `/github/get_repository_commits?owner={owner}&repo={repo}&per_page={per_page}`

Get repository commits in reverse chronological order (newest first).

**Parameters:**
- `owner` (required): Repository owner
- `repo` (required): Repository name
- `per_page` (optional): Number of commits per page (default: 100, max: 100)

**Response:**
Array of commit objects with author, committer, and commit information. Each commit includes:
- `sha`: Commit hash
- `commit`: Commit details (message, author, committer, date)
- `author`: GitHub user object (if available)
- `committer`: GitHub user object (if available)
- `url`: API URL for the commit

**Example:**
```bash
curl "http://localhost:5000/github/get_repository_commits?owner=facebook&repo=react&per_page=50"
```

### Get Repository Issues

**GET** `/github/get_repository_issues?owner={owner}&repo={repo}`

Get repository issues in chronological order (oldest first).

**Parameters:**
- `owner` (required): Repository owner
- `repo` (required): Repository name

**Response:**
Array of issue objects with details including title, body, state, labels, assignees, and more.

**Example:**
```bash
curl "http://localhost:5000/github/get_repository_issues?owner=facebook&repo=react"
```

### Get Repository Languages

**GET** `/github/get_repository_languages?owner={owner}&repo={repo}`

Get repository languages with byte counts.

**Parameters:**
- `owner` (required): Repository owner
- `repo` (required): Repository name

**Response:**
Object where keys are language names and values are bytes of code written in that language.

```json
{
  "JavaScript": 1234567,
  "TypeScript": 987654,
  "Python": 543210
}
```

**Example:**
```bash
curl "http://localhost:5000/github/get_repository_languages?owner=facebook&repo=react"
```

### Get Repository Contributors

**GET** `/github/get_repository_contributors?owner={owner}&repo={repo}`

Get all repository contributors. The endpoint automatically paginates through all available contributors.

**Parameters:**
- `owner` (required): Repository owner
- `repo` (required): Repository name

**Response:**
Array of contributor objects sorted by total contributions (descending). Each contributor object has a standardized format:

**For regular users (type: "User"):**
```json
{
  "type": "User",
  "login": "username",
  "id": 12345,
  "avatar_url": "https://avatars.githubusercontent.com/u/12345",
  "html_url": "https://github.com/username",
  "contributions": 150,
  "email": null,
  "name": null
}
```

**For anonymous contributors (type: "Anonymous"):**
```json
{
  "type": "Anonymous",
  "email": "user@example.com",
  "name": "User Name",
  "contributions": 50,
  "login": null,
  "id": null,
  "avatar_url": null,
  "html_url": null
}
```

**Note:** The endpoint automatically fetches all contributors by paginating through the GitHub API until no more contributors are available. It includes anonymous contributors using the `anon=1` parameter.

**Important:** There may still be discrepancies between the API count and GitHub's website display due to GitHub API limitations:

- **500 Email Address Limit**: Only the first 500 unique author email addresses in a repository are linked to GitHub user accounts. Contributors beyond this limit appear as anonymous.
- **API Caching**: The API caches contributor data for performance, which can result in information that is a few hours old.
- **Default Branch Only**: The endpoint only shows contributors to the default branch, while GitHub's website may show contributors across all branches.
- **Repository Insights Changes**: For repositories with over 10,000 commits, GitHub has implemented changes that may affect how contributors are counted and displayed.

**Example:**
```bash
curl "http://localhost:5000/github/get_repository_contributors?owner=facebook&repo=react"
```



## GitHub API Integration

The backend acts as a proxy to the GitHub API, using the following endpoints:

- `GET /search/repositories` - Search repositories
- `GET /repositories/{id}` - Get repository by ID
- `GET /repos/{owner}/{repo}/commits` - Get repository commits
- `GET /repos/{owner}/{repo}/contributors` - Get repository contributors (with `anon=1` parameter)
- `GET /repos/{owner}/{repo}/issues` - Get repository issues
- `GET /repos/{owner}/{repo}/languages` - Get repository languages

All requests use the GitHub API v3 and include proper headers for authentication and rate limiting. When a `GITHUB_ACCESS_TOKEN` is provided, all requests include a Bearer token in the Authorization header.

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (missing required parameters or invalid input)
- `404` - Not Found (repository not found)
- `500` - Internal Server Error (GitHub API errors or server issues)

Error responses include a JSON object with an `error` field:

```json
{
  "error": "Error message here"
}
```

Common error scenarios:
- Missing required parameters (e.g., `query`, `owner`, `repo`, `id`)
- Invalid repository ID or repository not found
- GitHub API rate limit exceeded
- Network or GitHub API errors


## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `5000` |
| `FLASK_DEBUG` | Enable debug mode | `false` |
| `FRONTEND_URL` | Allowed CORS origins | `http://localhost:3000` |
| `GITHUB_ACCESS_TOKEN` | GitHub personal access token for authenticated API requests (optional, recommended for production) | - |

## Development

### Running in Debug Mode

Set `FLASK_DEBUG=true` in your `.env` file or environment variables to enable Flask's debug mode.

### Testing Endpoints

You can test the API using curl or any HTTP client:

```bash
# Health check
curl http://localhost:5000/health

# Search repositories
curl "http://localhost:5000/github/search?query=react&per_page=20&page=1"

# Get repository by ID
curl "http://localhost:5000/github/get_repository_by_id?id=10270250"

# Get repository commits
curl "http://localhost:5000/github/get_repository_commits?owner=facebook&repo=react&per_page=50"

# Get repository contributors (automatically fetches all pages)
curl "http://localhost:5000/github/get_repository_contributors?owner=facebook&repo=react"

# Get repository issues
curl "http://localhost:5000/github/get_repository_issues?owner=facebook&repo=react"

# Get repository languages
curl "http://localhost:5000/github/get_repository_languages?owner=facebook&repo=react"
```

## Rate Limiting

The GitHub API has rate limits:
- **Unauthenticated**: 60 requests per hour per IP
- **Authenticated**: 5,000 requests per hour (when `GITHUB_ACCESS_TOKEN` is set)

The backend automatically uses authentication if the `GITHUB_ACCESS_TOKEN` environment variable is set. All GitHub API requests will include a Bearer token in the Authorization header.






The API will be available at `http://localhost:5000`.



