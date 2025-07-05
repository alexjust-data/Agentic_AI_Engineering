from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent, preview_email_agent
import asyncio
import os
from typing import Optional, Dict, Any
from datetime import datetime

class ResearchManager:
    def __init__(self, 
                 send_email: bool = True, 
                 save_html: bool = True,
                 output_dir: str = "output"):
        """
        Initialize ResearchManager with configuration options
        
        Args:
            send_email: Whether to actually send emails (False for preview only)
            save_html: Whether to save HTML reports to files
            output_dir: Directory to save output files
        """
        self.send_email = send_email
        self.save_html = save_html
        self.output_dir = output_dir
        self.last_report: Optional[ReportData] = None
        self.last_html: Optional[str] = None
        
        # Create output directory if it doesn't exist
        if self.save_html:
            os.makedirs(self.output_dir, exist_ok=True)

    async def run(self, query: str):
        """ 
        Run the deep research process, yielding status updates
        
        Yields:
            Status updates and final result dict
        """
        trace_id = gen_trace_id()
        start_time = datetime.now()
        
        try:
            with trace("Research trace", trace_id=trace_id):
                print(f"🔍 View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
                yield f"🔍 View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
                
                print("🚀 Starting research...")
                yield "🚀 Starting research..."
                
                # Plan searches
                search_plan = await self.plan_searches(query)
                yield f"📋 Searches planned: {len(search_plan.searches)} searches to perform"
                
                # Perform searches
                search_results = await self.perform_searches(search_plan)
                yield f"🔍 Searches complete: {len(search_results)} results obtained"
                
                # Write report
                report = await self.write_report(query, search_results)
                self.last_report = report
                yield "📝 Report written successfully"
                
                # Handle email/preview
                email_result = await self.handle_email(report)
                
                # Save HTML if enabled
                html_file = None
                if self.save_html:
                    html_file = await self.save_html_report(report, query)
                    yield f"💾 HTML report saved: {html_file}"
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                result = {
                    "status": "success",
                    "query": query,
                    "report": report,
                    "email_result": email_result,
                    "searches_performed": len(search_results),
                    "duration_seconds": duration,
                    "trace_id": trace_id,
                    "html_file": html_file if self.save_html else None
                }
                
                yield f"✅ Research complete! Duration: {duration:.1f}s"
                yield report.markdown_report
                
                # Final result
                yield result
                
        except Exception as e:
            error_msg = f"❌ Error during research: {str(e)}"
            print(error_msg)
            yield error_msg
            yield {
                "status": "error",
                "query": query,
                "error": str(e),
                "trace_id": trace_id
            }

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
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
        """ Perform a search for the query """
        input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(search_agent, input_text)
            return str(result.final_output)
        except Exception as e:
            print(f"⚠️ Search failed for '{item.query}': {str(e)}")
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        print("📝 Thinking about report...")
        input_text = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input_text)
        print("✅ Finished writing report")
        return result.final_output

    async def handle_email(self, report: ReportData) -> Dict[str, Any]:
        """ Handle email sending or preview based on configuration """
        if self.send_email:
            print("📧 Sending email...")
            try:
                result = await Runner.run(email_agent, report.markdown_report)
                print("✅ Email sent successfully")
                return {"status": "sent", "result": result}
            except Exception as e:
                print(f"❌ Email sending failed: {str(e)}")
                return {"status": "failed", "error": str(e)}
        else:
            print("👁️ Generating email preview...")
            try:
                result = await Runner.run(preview_email_agent, report.markdown_report)
                # Extract HTML from preview result
                if hasattr(result, 'tool_outputs') and result.tool_outputs:
                    html_data = result.tool_outputs[-1]
                    self.last_html = html_data.get('html_content', '')
                    print("✅ Email preview generated")
                    return {"status": "preview", "html_content": self.last_html}
                else:
                    print("⚠️ No HTML content in preview result")
                    return {"status": "preview_failed", "error": "No HTML content generated"}
            except Exception as e:
                print(f"❌ Email preview failed: {str(e)}")
                return {"status": "preview_failed", "error": str(e)}

    async def save_html_report(self, report: ReportData, query: str) -> str:
        """ Save HTML report to file """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()[:50]
        filename = f"research_report_{safe_query}_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        # Generate HTML content using preview agent
        try:
            result = await Runner.run(preview_email_agent, report.markdown_report)
            if hasattr(result, 'tool_outputs') and result.tool_outputs:
                html_content = result.tool_outputs[-1].get('html_content', '')
                if html_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print(f"💾 HTML report saved: {filepath}")
                    return filepath
                else:
                    print("⚠️ No HTML content to save")
                    return ""
            else:
                print("⚠️ Failed to generate HTML for saving")
                return ""
        except Exception as e:
            print(f"❌ Failed to save HTML report: {str(e)}")
            return ""

    def get_last_html(self) -> Optional[str]:
        """ Get the last generated HTML content """
        return self.last_html

    def get_last_report(self) -> Optional[ReportData]:
        """ Get the last generated report """
        return self.last_report

    async def preview_only(self, query: str) -> Dict[str, Any]:
        """ Run research and generate HTML preview without sending email """
        original_send_email = self.send_email
        self.send_email = False
        try:
            async for result in self.run(query):
                if isinstance(result, dict):
                    return result
            return {"status": "completed"}
        finally:
            self.send_email = original_send_email

    async def conduct_research(self, query: str, send_email: bool = None, preview_html: bool = True) -> Dict[str, Any]:
        """
        Conduct research and return the final result
        
        Args:
            query: The research query
            send_email: Whether to send email (overrides instance setting if provided)
            preview_html: Whether to generate HTML preview
            
        Returns:
            Dict containing research results and metadata
        """
        # Override send_email setting if provided
        original_send_email = self.send_email
        if send_email is not None:
            self.send_email = send_email
        
        try:
            final_result = None
            async for result in self.run(query):
                if isinstance(result, dict) and "status" in result:
                    final_result = result
                    break
            
            # Add HTML content if available and requested
            if preview_html and final_result and self.last_html:
                final_result["html_content"] = self.last_html
                
            # Add summary and cost estimation
            if final_result and final_result.get("status") == "success":
                final_result["summary"] = f"Research completed on: {query}"
                final_result["cost"] = 0.0  # Placeholder for cost calculation
                final_result["time"] = final_result.get("duration_seconds", 0)
                
            return final_result or {"status": "error", "error": "No result generated"}
            
        finally:
            # Restore original setting
            self.send_email = original_send_email

# Convenience functions for common use cases
async def quick_research(query: str, send_email: bool = False) -> Dict[str, Any]:
    """ Quick research with preview only by default """
    manager = ResearchManager(send_email=send_email, save_html=True)
    async for result in manager.run(query):
        if isinstance(result, dict):
            return result
    return {"status": "completed"}

async def research_with_email(query: str) -> Dict[str, Any]:
    """ Research with email sending enabled """
    return await quick_research(query, send_email=True)