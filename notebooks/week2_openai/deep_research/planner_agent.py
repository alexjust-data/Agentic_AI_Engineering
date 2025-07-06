from pydantic import BaseModel, Field
from agents import Agent

HOW_MANY_SEARCHES = 5

INSTRUCTIONS = f"""You are a helpful research assistant. Given a query, come up with a set of web searches 
to perform to best answer the query comprehensively. Output {HOW_MANY_SEARCHES} diverse search terms that will 
cover different aspects of the topic.

Consider including searches for:
- Current developments and recent news
- Technical details and explanations
- Industry analysis and expert opinions
- Comparative analysis and alternatives
- Future trends and implications

Make each search unique and complementary to build a complete picture of the topic."""


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query and what unique perspective it will provide.")
    query: str = Field(description="The specific search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of diverse web searches to perform to comprehensively answer the query.")
    
planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)