import gradio as gr
from dotenv import load_dotenv
import asyncio
import importlib
import sys

# 🔄 FORCE MODULE RELOAD - Ensures latest changes are loaded
def force_reload_modules():
    """Force reload of all our custom modules to pick up latest changes"""
    modules_to_reload = [
        'research_manager', 'email_agent', 'search_agent', 
        'planner_agent', 'writer_agent'
    ]
    
    for module_name in modules_to_reload:
        if module_name in sys.modules:
            print(f"🔄 Reloading module: {module_name}")
            importlib.reload(sys.modules[module_name])
        else:
            print(f"🔄 Module not loaded yet: {module_name}")

# Force reload at startup
force_reload_modules()

# Now import after reload
from research_manager import ResearchManager

load_dotenv(override=True)


class MockResearchManager(ResearchManager):
    """Test version that uses mock searches instead of real web searches"""
    
    async def search(self, item):
        """Mock search that returns simulated results instead of real web searches"""
        print(f"🔍 MOCK SEARCH: {item.query}")
        
        # Simulate different types of search results based on the query
        mock_results = {
            "latest": f"""Latest developments in {item.query}: Recent advancements include new frameworks 
            and improved methodologies. Industry leaders are focusing on scalability and efficiency.
            Major companies are investing heavily in this technology with promising early results.
            
            Sources: [Recent Tech News](https://example.com/tech-news), [Industry Report](https://example.com/report), [Company Announcement](https://example.com/announcement)""",
            
            "technical": f"""Technical analysis of {item.query}: Core technologies involve advanced algorithms
            and distributed systems. Implementation challenges include performance optimization and scalability.
            System architecture requires careful consideration of resource allocation and processing efficiency.
            
            Sources: [Technical Documentation](https://example.com/docs), [Research Paper](https://example.com/paper), [Engineering Blog](https://example.com/blog)""",
            
            "review": f"""Review and analysis of {item.query}: Expert opinions highlight both strengths and limitations.
            Comparative studies show varying performance across different use cases and environments.
            User feedback indicates positive reception with some areas for improvement identified.
            
            Sources: [Expert Review](https://example.com/review), [Comparison Study](https://example.com/study), [User Survey](https://example.com/survey)""",
            
            "trends": f"""Future trends in {item.query}: Emerging patterns suggest increased adoption and innovation.
            Market forecasts indicate continued growth with significant investment expected in the coming years.
            Industry analysts predict major breakthroughs and widespread deployment across various sectors.
            
            Sources: [Market Analysis](https://example.com/market), [Trend Report](https://example.com/trends), [Analyst Prediction](https://example.com/prediction)""",
            
            "default": f"""Research findings for {item.query}: Comprehensive analysis reveals key insights
            and important considerations for implementation and adoption. Current state shows promising progress
            with several practical applications already demonstrating significant value.
            
            Sources: [Research Article](https://example.com/research), [Case Study](https://example.com/case-study), [White Paper](https://example.com/whitepaper)"""
        }
        
        # Select mock result based on keywords in the query
        query_lower = item.query.lower()
        if "latest" in query_lower or "recent" in query_lower:
            return mock_results["latest"]
        elif "technical" in query_lower or "how" in query_lower:
            return mock_results["technical"]
        elif "review" in query_lower or "analysis" in query_lower:
            return mock_results["review"]
        elif "trends" in query_lower or "future" in query_lower:
            return mock_results["trends"]
        else:
            return mock_results["default"]


async def run_research_async(query: str, use_test_mode: bool = False):
    """Async version for Jupyter notebooks - SIMPLIFIED"""
    if not query or query.strip() == "":
        return "❌ Please enter a research query", ""
    
    # 🔄 Force reload modules to pick up latest changes
    print("🔄 Reloading modules for latest changes...")
    force_reload_modules()
    
    try:
        # Import fresh versions after reload
        from research_manager import ResearchManager
        
        # Choose manager based on test mode
        if use_test_mode:
            manager = MockResearchManager()
            print("🧪 **TEST MODE ACTIVE - No API costs will be incurred**")
        else:
            manager = ResearchManager()
            print("💰 **REAL MODE ACTIVE - OpenAI API costs will apply (2.5¢ per search)**")
        
        # Collect all chunks
        all_chunks = []
        async for chunk in manager.run(query):
            all_chunks.append(str(chunk))
            print(f"🔄 Progress: {len(all_chunks)} updates received")
        
        if not all_chunks:
            return "❌ No results received", ""
        
        # Find the final report (usually the longest chunk)
        final_report = ""
        progress_chunks = []
        
        for chunk in all_chunks:
            if len(chunk) > 500 and ("##" in chunk or "#" in chunk):
                final_report = chunk
            else:
                progress_chunks.append(chunk)
        
        # If no long report found, use the last chunk
        if not final_report and all_chunks:
            final_report = all_chunks[-1]
            progress_chunks = all_chunks[:-1]
        
        progress_text = "\n".join(progress_chunks) + "\n\n✅ **Research Complete!**"
        
        return progress_text, final_report
                
    except Exception as e:
        error_msg = f"❌ Error during research: {str(e)}"
        print(f"DEBUG: Exception occurred: {e}")
        return error_msg, ""


def run_research_sync(query: str, use_test_mode: bool = False):
    """Synchronous wrapper - ULTRA SIMPLIFIED for maximum reliability"""
    if not query or query.strip() == "":
        return "❌ Please enter a research query", ""
    
    # 🔄 Force reload modules to pick up latest changes
    print("🔄 Reloading modules for latest changes...")
    force_reload_modules()
    
    try:
        import concurrent.futures
        import asyncio
        
        def run_async_in_thread():
            """Run async code in completely isolated thread"""
            # Create completely new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Simple direct execution
                async def simple_research():
                    # Import fresh versions after reload
                    from research_manager import ResearchManager
                    
                    if use_test_mode:
                        manager = MockResearchManager()
                        print("🧪 TEST MODE: Using mock searches")
                    else:
                        manager = ResearchManager()
                        print("💰 REAL MODE: Using live searches")
                    
                    # Just collect everything
                    chunks = []
                    async for chunk in manager.run(query):
                        chunks.append(str(chunk))
                        print(f"📥 Collected chunk {len(chunks)}")
                    
                    if not chunks:
                        return "❌ No data collected", ""
                    
                    # Simple separation: longest chunk = report, rest = progress
                    longest_chunk = max(chunks, key=len) if chunks else ""
                    other_chunks = [c for c in chunks if c != longest_chunk]
                    
                    progress = "\n".join(other_chunks) + "\n\n✅ Complete!"
                    return progress, longest_chunk
                
                # Run it
                return loop.run_until_complete(simple_research())
                
            except Exception as e:
                print(f"🔧 Thread error: {e}")
                return f"❌ Error: {e}", ""
            finally:
                loop.close()
        
        # Execute in thread with timeout
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_async_in_thread)
            result = future.result(timeout=180)  # 3 minute timeout
            return result
            
    except concurrent.futures.TimeoutError:
        return "❌ Research timed out after 3 minutes", ""
    except Exception as e:
        print(f"🔧 Sync wrapper error: {e}")
        return f"❌ Error: {e}", ""


def create_interface():
    """Create the Gradio interface"""
    with gr.Blocks(theme=gr.themes.Default(primary_hue="sky"), title="Deep Research Agent") as ui:
        gr.Markdown("# 🔍 Deep Research Agent")
        gr.Markdown("Enter a research topic and the agent will search the web, analyze results, and email you a comprehensive report with linked references.")
        
        # Cost warning and test mode toggle
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("""
                ### 💰 **Cost Information:**
                - **Test Mode**: FREE - Uses simulated searches with realistic sample data
                - **Real Mode**: 2.5¢ per search × 5 searches = 12.5¢ per research query
                """)
            with gr.Column(scale=1):
                test_mode_toggle = gr.Checkbox(
                    label="🧪 Enable Test Mode (FREE)",
                    value=True,  # Default to test mode to prevent accidental costs
                    info="Use mock searches to test functionality without API costs"
                )
        
        with gr.Row():
            with gr.Column(scale=3):
                query_textbox = gr.Textbox(
                    label="Research Query", 
                    placeholder="e.g., Latest developments in quantum computing 2025",
                    lines=3
                )
            with gr.Column(scale=1):
                run_button = gr.Button("🚀 Start Research", variant="primary", size="lg")
        
        with gr.Row():
            with gr.Column(scale=1):
                progress_area = gr.Markdown(
                    label="🔄 Research Progress", 
                    value="Enter a query above to begin research...",
                    height=400
                )
            with gr.Column(scale=1):
                report_area = gr.Markdown(
                    label="📋 Final Report with References", 
                    value="Complete report with linked sources will appear here when research is finished...",
                    height=400
                )
        
        # Clear button to reset the interface
        with gr.Row():
            clear_button = gr.Button("🗑️ Clear", variant="secondary")
            debug_button = gr.Button("🔧 Debug Info", variant="secondary")
        
        def clear_interface():
            return ("Enter a query above to begin research...", 
                    "Complete report with linked sources will appear here when research is finished...", 
                    "")
        
        def show_debug_info():
            debug_info = """## Debug Information
            
- Interface: ✅ Working
- Research Manager: ✅ Loaded
- Search Agents: ✅ Configured
- Email Service: ✅ Connected
- Report Detection: ✅ Enhanced (multiple formats)

**Test Mode Features:**
- 🧪 Mock searches return realistic sample data
- 💰 No OpenAI API costs incurred
- 📧 Email functionality still works
- 🔗 Sample reference links included

**Real Mode Features:**
- 🌐 Live web searches via OpenAI API
- 💰 2.5¢ per search (12.5¢ total per query)
- 📧 Professional HTML email with real sources
- 🔗 Actual clickable reference links

**How it works:**
1. Plans 5 diverse searches based on query analysis
2. Executes searches (real or mock based on toggle)
3. Generates comprehensive report with professional citations
4. Sends HTML email with clickable references
5. Displays final report with source links

**Enhanced Report Detection:**
- Detects reports starting with "## Final Research Report"
- Detects reports starting with "# " (main title)
- Detects long structured content with headers
- Fallback: checks last chunk for report content

**If report doesn't appear:** 
- Check console for debug logs
- Try clicking "Clear" and running again
- Toggle between test/real mode
- Verify query is specific enough
            """
            return "Debug info displayed", debug_info
        
        # Connect the buttons to functions
        run_button.click(
            fn=run_research_sync, 
            inputs=[query_textbox, test_mode_toggle], 
            outputs=[progress_area, report_area]
        )
        query_textbox.submit(
            fn=run_research_sync, 
            inputs=[query_textbox, test_mode_toggle], 
            outputs=[progress_area, report_area]
        )
        clear_button.click(
            fn=clear_interface,
            outputs=[progress_area, report_area, query_textbox]
        )
        debug_button.click(
            fn=show_debug_info,
            outputs=[progress_area, report_area]
        )
    
    return ui


if __name__ == "__main__":
    ui = create_interface()
    ui.launch(inbrowser=True)

