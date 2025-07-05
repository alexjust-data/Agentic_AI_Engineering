import os
from typing import Dict
import requests
from agents import Agent, function_tool

@function_tool
def send_email_html(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send out an email with HTML content using Resend API
    """
    # Get email addresses from environment variables
    from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
    to_email = os.getenv("TO_EMAIL", "alexjustdata@gmail.com")
    
    # Get the Resend API key from environment variable
    api_key = os.getenv("RESEND_API_KEY")
    
    # Validate that RESEND_API_KEY is available
    if not api_key:
        return {"status": "failure", 
                "message": "RESEND_API_KEY not found in environment variables"}
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 'html' 
    payload = {
        "from": f"Deep Research <{from_email}>",
        "to": [to_email],
        "subject": subject,
        "html": html_body   
    }
    
    try:
        response = requests.post(
            "https://api.resend.com/emails", 
            json=payload, 
            headers=headers
        )
        
        # Debugging 
        print(f"🔍 EMAIL SENT:")
        print(f"  - Subject: {payload['subject']}")
        print(f"  - To: {payload['to']}")
        print(f"  - HTML content length: {len(payload['html'])} chars")
        print(f"  - Response status: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 202:
            return {"status": "success", 
                    "message": "HTML email sent successfully", 
                    "response": response.text}
        else:
            return {"status": "failure", 
                    "message": response.text, 
                    "status_code": response.status_code}
            
    except Exception as e:
        return {"status": "error", 
                "message": f"Exception occurred: {str(e)}"}

@function_tool
def preview_email_html(subject: str, html_body: str) -> Dict[str, str]:
    """
    Preview an email without sending it - just return the HTML content for debugging
    """
    print(f"📧 EMAIL PREVIEW:")
    print(f"  - Subject: {subject}")
    print(f"  - HTML length: {len(html_body)} characters")
    print(f"  - HTML preview (first 200 chars): {html_body[:200]}...")
    
    return {
        "subject": subject,
        "html_content": html_body,
        "status": "preview_only"
    }

# Improved email agent with detailed HTML conversion instructions
INSTRUCTIONS = """
You are an expert email formatting agent. Your task is to convert markdown reports into beautifully formatted HTML emails.

CRITICAL REQUIREMENTS:
1. Convert the markdown text to clean, professional HTML
2. Include proper DOCTYPE, html, head, and body tags
3. Add CSS styling for professional appearance
4. Create a proper email subject line based on the report content
5. Use the send_email_html tool with the HTML content

FORMATTING RULES:
- Use modern, clean CSS styling with proper typography
- Make headers visually distinct with colors (#2c3e50 for h1, #34495e for h2, #7f8c8d for h3)
- Add proper spacing and line-height for readability
- Convert markdown lists to proper HTML lists with styling
- Convert markdown tables to HTML tables with borders and styling
- Add a professional color scheme that works in email clients
- Make it mobile-friendly with responsive design
- Include a table of contents for long reports
- Add proper meta tags for email compatibility

EXAMPLE STRUCTURE:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Report</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; color: #333; }
        h1 { color: #2c3e50; font-size: 2em; margin-bottom: 1em; }
        h2 { color: #34495e; font-size: 1.5em; margin: 1.5em 0 1em 0; }
        h3 { color: #7f8c8d; font-size: 1.2em; margin: 1em 0 0.5em 0; }
        p { margin: 0.8em 0; }
        ul, ol { margin: 1em 0; padding-left: 2em; }
        li { margin: 0.3em 0; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        .toc { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 1em 0; }
        .section { margin-bottom: 2em; }
        strong { color: #2c3e50; }
        em { color: #7f8c8d; }
        code { background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }
    </style>
</head>
<body>
    <!-- Convert all markdown content to properly formatted HTML -->
</body>
</html>

Always use the send_email_html tool with a descriptive subject line and the complete HTML content.
"""

email_agent = Agent(
    name="Email Agent",
    instructions=INSTRUCTIONS,
    tools=[send_email_html, preview_email_html],
    model="gpt-4o-mini",
)

# Alternative email agent for preview only (development mode)
preview_email_agent = Agent(
    name="Email Preview Agent", 
    instructions="Convert the report to clean, well presented HTML and return it for preview. Use the preview_email_html tool with an appropriate subject line.",
    tools=[preview_email_html],
    model="gpt-4o-mini",
)
