import requests
import os
from utils import get_logger

logger = get_logger()
class GithubService:
    def __init__(self):
        self.api_url = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Wiremind Technical Test'
        }
        
        # Add Authorization header if GitHub access token is provided
        github_token = os.getenv('GITHUB_ACCESS_TOKEN')
        if github_token:
            self.headers['Authorization'] = f'Bearer {github_token}'
            logger.info('GitHub API requests will use authenticated access token')
        else:
            logger.info('GitHub API requests will use unauthenticated access (rate limit: 60 requests/hour)')
    
    def _get(self, url : str):
        logger.info(f'Github Endpoint: {url}')
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get data from {url}: {response.status_code} {response.text}")
        return response.json()

    def search_repositories(self, query : str, per_page : int = 10, page : int = 1):
        """
        Search GitHub repositories using GitHub API endpoint:
        GET /search/repositories
        
        Returns repositories sorted by stars (descending).
        Supports pagination with per_page (max 100) and page parameters.
        """
        url = f'{self.api_url}/search/repositories?q={query}&per_page={per_page}&page={page}&sort=stars'
        return self._get(url)

    def get_repository_details(self, owner : str, repo : str):
        url = f'{self.api_url}/repos/{owner}/{repo}'
        return self._get(url)

    def get_repository_contributors(self, owner : str, repo : str, per_page : int = 100, page : int = 1):
        """
        Get repository contributors using GitHub API endpoint:
        GET /repos/{owner}/{repo}/contributors
        
        Returns contributors sorted by number of commits (descending).
        Supports pagination with per_page (max 100) and page parameters.
        """
        url = f'{self.api_url}/repos/{owner}/{repo}/contributors?per_page={per_page}&page={page}'
        return self._get(url)

    def get_repository_issues(self, owner : str, repo : str):
        url = f'{self.api_url}/repos/{owner}/{repo}/issues'
        return self._get(url)
    
    def get_repository_commits(self, owner : str, repo : str, perPage : int = 100):
        """
        Get repository commits using GitHub API endpoint:
        GET /repos/{owner}/{repo}/commits
        
        Returns commits in reverse chronological order (newest first).
        Supports pagination with per_page parameter (max 100).
        """
        url = f'{self.api_url}/repos/{owner}/{repo}/commits?per_page={perPage}'
        return self._get(url)
    
    def get_repository_by_id(self, repo_id : int):
        url = f'{self.api_url}/repositories/{repo_id}'
        return self._get(url)
    
    def get_repository_languages(self, owner : str, repo : str):
        """
        Get repository languages using GitHub API endpoint:
        GET /repos/{owner}/{repo}/languages
        
        Returns a dictionary where keys are language names and values are bytes of code.
        """
        url = f'{self.api_url}/repos/{owner}/{repo}/languages'
        return self._get(url)