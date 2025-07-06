import os
from typing import Dict
import requests
from agents import Agent, function_tool

def safe_save_html(html_content: str, subject: str) -> str:
    """Safely save HTML content to a file, with fallback if it fails"""
    print(f"🔧 DEBUG: safe_save_html called with subject: '{subject}'")
    print(f"🔧 DEBUG: HTML content length: {len(html_content)}")
    
    try:
        import datetime
        import re

        # Create safe filename from subject
        safe_subject = re.sub(r'[^a-zA-Z0-9\s\-_]', '', subject)
        safe_subject = safe_subject.replace(' ', '_')[:50]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{safe_subject}_{timestamp}.html"
        print(f"🔧 DEBUG: Generated filename: {filename}")

        # Create output directory if it doesn't exist
        output_dir = "output"
        print(f"🔧 DEBUG: Checking output directory: {output_dir}")
        
        if not os.path.exists(output_dir):
            print(f"🔧 DEBUG: Creating output directory...")
            os.makedirs(output_dir)
            print(f"🔧 DEBUG: Output directory created")
        else:
            print(f"🔧 DEBUG: Output directory already exists")

        # Save HTML file
        filepath = os.path.join(output_dir, filename)
        print(f"🔧 DEBUG: Full filepath: {filepath}")
        
        print(f"🔧 DEBUG: Attempting to write file...")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"🔧 DEBUG: File written successfully")

        print(f"✅ HTML saved as {filepath}")
        return filepath

    except Exception as e:
        print(f"❌ safe_save_html failed: {e}")
        print(f"🔧 DEBUG: Exception type: {type(e)}")
        import traceback
        print(f"🔧 DEBUG: Traceback: {traceback.format_exc()}")
        
        # Fallback: try simple filename
        try:
            print(f"🔧 DEBUG: Attempting fallback save...")
            # Ensure output directory exists for fallback too
            if not os.path.exists("output"):
                os.makedirs("output")
            
            fallback_path = "output/report_latest.html"
            print(f"🔧 DEBUG: Fallback path: {fallback_path}")
            
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Fallback HTML saved as {fallback_path}")
            return fallback_path
        except Exception as e2:
            print(f"❌ Fallback attempt also failed: {e2}")
            print(f"🔧 DEBUG: Fallback exception type: {type(e2)}")
            return None


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send out an email with the given subject and HTML body 
    to all sales prospects using Resend
    """
    print(f"🔧 DEBUG: send_email called with subject: '{subject}'")
    print(f"🔧 DEBUG: HTML body length: {len(html_body)}")
    
    # Get email addresses from environment variables
    from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
    to_email = os.getenv("TO_EMAIL", "alexjustdata@gmail.com")
    
    # Get the Resend API key from environment variable
    api_key = os.getenv("RESEND_API_KEY")
    
    # Validate that RESEND_API_KEY is available
    if not api_key:
        print("❌ RESEND_API_KEY not found in environment variables")
        return {"status": "failure", 
                "message": "RESEND_API_KEY not found in environment variables"}
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Directly use the provided HTML body (no extra formatting or conversion)
    formatted_html = html_body
    
    payload = {
        "from": f"Alex <{from_email}>",
        "to": [to_email],
        "subject": subject,
        "html": formatted_html
    }
    
    try:
        print(f"🔧 DEBUG: About to send email...")
        response = requests.post(
            "https://api.resend.com/emails", 
            json=payload, 
            headers=headers
        )
        
        # Add debugging information
        print(f"📧 EMAIL SENT:")
        print(f"  - Subject: {subject}")
        print(f"  - To: {payload['to']}")
        print(f"  - HTML content length: {len(formatted_html)} chars")
        print(f"  - Response status: {response.status_code}")
        
        # Try to save HTML locally (safely)
        print(f"📧 EMAIL PREVIEW:")
        print(f"  - Subject: {subject}")
        print(f"  - HTML length: {len(formatted_html)} characters")
        print(f"  - HTML preview (first 200 chars): {formatted_html[:200]}...")
        
        print(f"🔧 DEBUG: About to call safe_save_html...")
        saved_path = safe_save_html(formatted_html, subject)
        print(f"🔧 DEBUG: safe_save_html returned: {saved_path}")
        
        if saved_path:
            print(f"💾 HTML report saved: {saved_path}")
        else:
            print(f"⚠️ Failed to generate HTML for saving")
        
        if response.status_code == 200 or response.status_code == 202:
            return {"status": "success", 
                    "message": "HTML email sent successfully", 
                    "response": response.text}
        else:
            print(f"❌ Email failed with status {response.status_code}: {response.text}")
            return {"status": "failure", 
                    "message": response.text, 
                    "status_code": response.status_code}
            
    except Exception as e:
        print(f"❌ Email exception: {str(e)}")
        return {"status": "error", 
                "message": f"Exception occurred: {str(e)}"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line.

Always create a compelling subject line that captures the essence of the report.
Format the HTML with proper structure, headers, and styling for professional presentation.
Ensure all markdown links are converted to clickable HTML links in the email.
Preserve all references and citations in a readable format."""

email_agent = Agent(
    name="EmailAgent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
