def get_google_login_url():
    # Mock OAuth URL
    return "https://accounts.google.com/o/oauth2/auth?client_id=mock..."

def get_github_login_url():
    # Mock OAuth URL
    return "https://github.com/login/oauth/authorize?client_id=mock..."

def handle_oauth_callback(provider: str, code: str):
    # Exchange code for token (mocked)
    return {
        "email": f"mock_user@{provider}.com",
        "name": "Mock User"
    }
