from flask import Blueprint
from .health import health_bp
from .github import github_bp

def register_routes(app):
    """Register all route blueprints with the Flask app"""
    app.register_blueprint(health_bp)
    app.register_blueprint(github_bp)

