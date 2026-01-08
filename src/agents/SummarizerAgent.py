from langchain.agents import create_agent
from agents.constants import LLM_MODEL

class SummarizerAgent:
    def __init__(self, tools) -> None:
        system_prompt = """You are the lead pull request reviewer. Generate a nice review summary with details like:
        **Title**
        **Author**
        **Files Changed**
        **Triage Risk**
        
        **Summary**
        **Triage Table**
        """
        self.agent = create_agent(LLM_MODEL, tools, system_prompt=system_prompt)

    async def generate_review(
        self, pr_url, triage_response, correctness_response, security_response
    ) -> str:
        user_prompt = f"""
        Review PR URL: {pr_url}.
        Below are the reviews for it by triage_agent, correctness_agent and security_agent:
        Triage Response: {triage_response}
        ---
        Correctness Response: {correctness_response}
        ---
        Security Response: {security_response}
        ---
        Use these to create a summary.
        """
        response = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": user_prompt}]}
        )
        return response["messages"][-1].content