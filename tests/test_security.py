import subprocess

def test_flake8():
    """Run flake8 to check for syntax errors and PEP8 compliance."""
    result = subprocess.run(["flake8", "src/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Flake8 found issues:\n{result.stdout}"

def test_bandit():
    """Run bandit to check for security vulnerabilities."""
    result = subprocess.run(["bandit", "-r", "src/"], capture_output=True, text=True)
    assert "No issues identified" in result.stdout or result.returncode == 0
