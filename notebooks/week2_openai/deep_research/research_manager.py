from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
import asyncio

class ResearchManager:

    async def run(self, query: str):
        """Run the deep research process, yielding status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield f"🔍 View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            yield "🚀 Starting research..."
            search_plan = await self.plan_searches(query)
            yield "📋 Searches planned, starting to search..."     
            search_results = await self.perform_searches(search_plan)
            yield "✅ Searches complete, writing report..."
            report = await self.write_report(query, search_results)
            yield "📝 Report written, sending email..."
            await self.send_email(report)
            yield "📧 Email sent successfully!"
            
            # Format the final report for better display in Gradio
            print(f"DEBUG: Preparing final report for query: {query}")
            print(f"DEBUG: Report summary length: {len(report.short_summary)}")
            print(f"DEBUG: Report content length: {len(report.markdown_report)}")
            
            final_report = f"""## Final Research Report

**Query:** {query}

**Executive Summary:** {report.short_summary}

---

{report.markdown_report}

---

### 🔍 Recommended Follow-up Research Topics:
"""
            
            for i, question in enumerate(report.follow_up_questions, 1):
                final_report += f"{i}. {question}\n"
            
            print(f"DEBUG: Final report prepared, length: {len(final_report)}")
            print(f"DEBUG: Final report starts with: {final_report[:100]}...")
            
            yield final_report
        

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the searches to perform for the query"""
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Perform the searches for the query"""
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform a single search for the given search item"""
        input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input_text,
            )
            return str(result.final_output)
        except Exception as e:
            print(f"DEBUG: Search failed for {item.query}: {e}")
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the comprehensive report based on search results"""
        print("📝 Thinking about report...")
        input_text = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input_text,
        )

        print("✅ Finished writing report")
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        """Send the report via email"""
        print("📧 Sending email...")
        try:
            result = await Runner.run(
                email_agent,
                report.markdown_report,
            )
            print("✅ Email sent successfully")
        except Exception as e:
            print(f"DEBUG: Email sending failed: {e}")
            print("⚠️ Email sending failed, but continuing with report generation")