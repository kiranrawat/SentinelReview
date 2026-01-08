import requests
from github_fetcher.models import PRDetails, PRFile
from urllib.parse import urlparse

class GithubAPIConnector:
    """A connector for fetching GitHub pull request details and files via the GitHub API."""
    
    def __init__(self):
        pass

    def _parse_pr_url(self, pr_url: str):
        """
        Parses the given GitHub pull request URL to extract necessary components
        for constructing API endpoint URLs.
        
        Args:
            pr_url (str): The GitHub pull request URL in the format:
                  https://github.com/{owner}/{repo}/pull/{pr_number}
        
        Attributes:
            pr_url (str): The original pull request URL.
            api_pr_url (str): The GitHub API endpoint URL for the pull request.
            file_url (str): The GitHub API endpoint URL for the pull request files.
        
        Raises:
            Exception: If the pr_url format is invalid or doesn't contain expected path components.
        """
        try:
            self.pr_url = pr_url
            parts = [part for part in urlparse(pr_url).path.split('/') if part]
            api_pr_url = f'https://api.github.com/repos/{parts[0]}/{parts[1]}/pulls/{parts[-1]}'
            file_url = f'https://api.github.com/repos/{parts[0]}/{parts[1]}/pulls/{parts[-1]}/files'
            return api_pr_url, file_url
        except IndexError:
            raise Exception("Invalid PR URL format. Expected format: https://github.com/{owner}/{repo}/pull/{pr_number}")

    def fetch_pr_details(self, pr_url:str) -> PRDetails:
        """
        Fetch pull request details from the GitHub API.
        Makes an HTTP GET request to the configured PR API endpoint and parses
        the response into a PRDetails object.
        Inputs:
            pr_url (str): The GitHub pull request URL.
        Returns:
            PRDetails: A validated PRDetails object containing the pull request information.
        Raises:
            requests.exceptions.HTTPError: If the HTTP request returns an error status code.
            requests.exceptions.RequestException: If a network error occurs during the request.
            ValidationError: If the response JSON cannot be validated against the PRDetails model.
        """
        api_pr_url, _ = self._parse_pr_url(pr_url)
        response = requests.get(api_pr_url)
        response.raise_for_status()
        return PRDetails.model_validate(response.json())

    def fetch_pr_files(self, pr_url:str) -> list[PRFile]:
        """
        Fetch the list of files modified in a pull request.
        Makes an HTTP GET request to the file URL endpoint and parses the JSON response
        into a list of PRFile objects.
        Inputs:
            pr_url (str): The GitHub pull request URL.
        Returns:
            list[PRFile]: A list of PRFile objects representing the files changed in the pull request.
        Raises:
            requests.exceptions.HTTPError: If the HTTP request returns an error status code.
            requests.exceptions.RequestException: If the HTTP request fails.
            pydantic.ValidationError: If the response data fails validation against the PRFile model.
        """
        _, file_url = self._parse_pr_url(pr_url)
        response = requests.get(file_url)
        response.raise_for_status()
        files = [PRFile.model_validate(file) for file in response.json()]

        pr_details = self.fetch_pr_details(pr_url)
        base_repo_url = pr_details.base.repo.svn_url
        base_sha = pr_details.base.sha
        for file in files:
            if file.status == 'modified':
                file.original_file_raw_url = f'{base_repo_url}/raw/{base_sha}/{file.filename}'
        return files
    
    def fetch_raw_file_content(self, raw_url: str) -> str:
        """
        Fetch the raw content of a file from a given raw URL.
        
        Args:
            raw_url (str): The raw URL of the file to fetch.
        """
        response = requests.get(raw_url)
        response.raise_for_status()
        return response.text