from flask import Blueprint, jsonify, request
from services.github import GithubService
from utils import get_logger

github_bp = Blueprint('github', __name__)
logger = get_logger()

github_service = GithubService()

@github_bp.route('/github/search', methods=['GET'])
def search_repositories():
    try:
        query = request.args.get('query')
        if not query:
            logger.warning('Search request missing query parameter')
            return jsonify({'error': 'Query parameter is required'}), 400
        logger.info(f'Searching repositories with query: {query}')
        repositories = github_service.search_repositories(query)
        logger.debug(f'Found {len(repositories.get("items", []))} repositories')
        return jsonify(repositories)
    except Exception as e:
        logger.error(f'Error searching repositories: {str(e)}')
        return jsonify({'error': str(e)}), 500

@github_bp.route('/github/get_repository_details', methods=['GET'])
def get_repository_details():
    try:
        owner = request.args.get('owner')
        if not owner:
            return jsonify({'error': 'Owner parameter is required'}), 400
        repo = request.args.get('repo')
        if not repo:
            return jsonify({'error': 'Repository parameter is required'}), 400
        repository = github_service.get_repository_details(owner, repo)
        return jsonify(repository)
    except Exception as e:
        logger.error(f'Error getting repository details: {str(e)}')
        return jsonify({'error': str(e)}), 500

@github_bp.route('/github/get_repository_contributors', methods=['GET'])
def get_repository_contributors():
    try:
        owner = request.args.get('owner')
        if not owner:
            return jsonify({'error': 'Owner parameter is required'}), 400
        repo = request.args.get('repo')
        if not repo:
            return jsonify({'error': 'Repository parameter is required'}), 400
        
        per_page = request.args.get('per_page', 100, type=int)
        page = request.args.get('page', 1, type=int)
        contributors = github_service.get_repository_contributors(owner, repo, per_page, page)
        logger.info(f'Found {len(contributors)} contributors')
        return jsonify(contributors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@github_bp.route('/github/get_repository_issues', methods=['GET'])
def get_repository_issues():
    try:
        owner = request.args.get('owner')
        if not owner:
            return jsonify({'error': 'Owner parameter is required'}), 400
        repo = request.args.get('repo')
        if not repo:    
            return jsonify({'error': 'Repository parameter is required'}), 400
        issues = github_service.get_repository_issues(owner, repo)
        return jsonify(issues)
    except Exception as e:
        logger.error(f'Error getting repository issues: {str(e)}')
        return jsonify({'error': str(e)}), 500

@github_bp.route('/github/get_repository_commits', methods=['GET'])
def get_repository_commits():
    try:
        owner = request.args.get('owner')
        if not owner:
            return jsonify({'error': 'Owner parameter is required'}), 400
        repo = request.args.get('repo')
        if not repo:
            return jsonify({'error': 'Repository parameter is required'}), 400
        per_page = request.args.get('per_page', 100, type=int)
        commits = github_service.get_repository_commits(owner, repo, per_page)
        return jsonify(commits)
    except Exception as e:
        logger.error(f'Error getting repository commits: {str(e)}')
        return jsonify({'error': str(e)}), 500

@github_bp.route('/github/get_repository_by_id', methods=['GET'])
def get_repository_by_id():
    try:
        repo_id = request.args.get('id')
        if not repo_id:
            return jsonify({'error': 'Repository ID parameter is required'}), 400
        repository = github_service.get_repository_by_id(int(repo_id))
        return jsonify(repository)
    except Exception as e:
        logger.error(f'Error getting repository by ID: {str(e)}')
        return jsonify({'error': str(e)}), 500