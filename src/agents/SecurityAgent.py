from langchain.agents import create_agent
from agents.constants import LLM_MODEL
from agents.models import AgentFindings

class SecurityAgent:
    def __init__(self, tools) -> None:
        self.system_prompt = """You are a senior tech lead doing PR triage.
        Pick a small set of focus files (max 5) that are most important/risky to review deeply.
        Only use information in the PR header and patches provided.
        """
        self.agent = create_agent(LLM_MODEL, tools, system_prompt=self.system_prompt, response_format=AgentFindings)

    async def generate_review(self, pr_url):
        user_prompt = f"Review the PR at {pr_url}. Return JSON matching this schema: {AgentFindings.model_json_schema()}"
        response = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": user_prompt}]}
        )
        return response["structured_response"]
