from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StreamableHttpConnection

from agents.SummarizerAgent import SummarizerAgent
from agents.TriageAgent import TriageAgent
from agents.SecurityAgent import SecurityAgent
from agents.CorrectnessAgent import CorrectnessAgent

class PRReviewer:

    async def _get_mcp_tools(self):
        mcp_client = MultiServerMCPClient(
            {
                "pr_review_helpers": StreamableHttpConnection(
                    transport="streamable_http", url="http://localhost:8080/mcp"
                )
            }
        )
        tools = await mcp_client.get_tools()
        return tools

    async def generate_pr_review(self, pr_url):
        tools = await self._get_mcp_tools()
        triage_agent = TriageAgent(tools)
        correctness_agent = CorrectnessAgent(tools)
        security_agent = SecurityAgent(tools)
        summarizer_agent = SummarizerAgent(tools)

        triage_response = await triage_agent.generate_review(pr_url)
        correctness_response = await correctness_agent.generate_review(pr_url)
        security_response = await security_agent.generate_review(pr_url)
        summarizer_response = await summarizer_agent.generate_review(
            pr_url=pr_url,
            triage_response=triage_response,
            correctness_response=correctness_response,
            security_response=security_response,
        )
        return summarizer_response
        