from fastmcp import FastMCP
from github_fetcher.github_api_connector import GithubAPIConnector

mcp = FastMCP(
    "SentinelReview MCP Server",
    instructions="This MCP server provides tools for fetching GitHub PR details and files.",
    version="1.0.0"
)

@mcp.tool
def fetch_github_pr(pr_url: str) -> dict:
    """Fetches GitHub PR details for the given PR URL."""
    connector = GithubAPIConnector()
    pr_details = connector.fetch_pr_details(pr_url)

    return {
        "pr_details": pr_details.model_dump(),
    }

@mcp.tool
def fetch_github_pr_files(pr_url: str) -> dict:
    """Fetches GitHub PR files details given a PR URL."""
    connector = GithubAPIConnector()
    pr_files = connector.fetch_pr_files(pr_url)

    return {
        "pr_files": [file.model_dump() for file in pr_files],
    }

@mcp.tool
def fetch_raw_github_pr_files(raw_url: str) -> dict:
    """Fetches GitHub PR files content given a raw_url or original_file_raw_url from fetch_github_pr_files tool."""
    connector = GithubAPIConnector()
    raw_file_content = connector.fetch_raw_file_content(raw_url)

    return {
        "raw_file_content": raw_file_content,
    }

if __name__ == "__main__":
    mcp.run(transport="http", port=8080)