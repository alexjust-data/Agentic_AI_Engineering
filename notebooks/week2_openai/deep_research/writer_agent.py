from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words.\n"
    "IMPORTANT: Include a 'References' section at the end with all the source URLs from the research. "
    "Maintain the clickable markdown format for all links. Group sources by topic if relevant. "
    "Cite sources within the text using superscript numbers like [1], [2], etc. and match them "
    "to numbered references at the end."
)


class ReportData(BaseModel):
    # A brief summary of the findings (2-3 sentences), useful for quickly presenting the main conclusion
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    # The complete final report in Markdown format (can include tables, lists, charts, etc.)
    markdown_report: str = Field(description="The final comprehensive report with proper citations and references")

    # A list of suggested follow-up topics or questions for further research (helpful for iteration or deeper analysis)
    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)