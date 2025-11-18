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
        per_page = request.args.get('per_page', 10, type=int)
        page = request.args.get('page', 1, type=int)
        logger.info(f'Searching repositories with query: {query}, page: {page}, per_page: {per_page}')
        repositories = github_service.search_repositories(query, per_page, page)
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
        
        # Fetch all contributors by paginating through pages
        all_contributors = []
        page = 1
        per_page = 100
        has_more = True

        while has_more:
            contributors_page = github_service.get_repository_contributors(owner, repo, per_page, page)
            
            if not contributors_page or len(contributors_page) == 0:
                has_more = False
            else:
                all_contributors.extend(contributors_page)
                
                # If we got less than per_page, we've reached the end
                if len(contributors_page) < per_page:
                    has_more = False
                else:
                    page += 1
                    # Safety limit: stop after 10 pages (1000 contributors)
                    if page > 10:
                        has_more = False
        
        logger.info(f'Found {len(all_contributors)} total contributors')
        return jsonify(all_contributors)
    except Exception as e:
        logger.error(f'Error getting repository contributors: {str(e)}')
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

@github_bp.route('/github/get_repository_languages', methods=['GET'])
def get_repository_languages():
    try:
        owner = request.args.get('owner')
        if not owner:
            return jsonify({'error': 'Owner parameter is required'}), 400
        repo = request.args.get('repo')
        if not repo:
            return jsonify({'error': 'Repository parameter is required'}), 400
        languages = github_service.get_repository_languages(owner, repo)
        return jsonify(languages)
    except Exception as e:
        logger.error(f'Error getting repository languages: {str(e)}')
        return jsonify({'error': str(e)}), 500