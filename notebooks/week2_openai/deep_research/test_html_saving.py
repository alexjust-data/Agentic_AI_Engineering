#!/usr/bin/env python3
"""
Test script to verify HTML saving functionality
"""

def test_html_saving():
    """Test that HTML saving works without errors"""
    print("🧪 Testing HTML saving functionality...")
    
    try:
        from email_agent import safe_save_html
        
        # Test HTML content
        test_html = """
        <html>
        <head><title>Test Report</title></head>
        <body>
        <h1>Test Report</h1>
        <p>This is a test HTML report to verify saving functionality.</p>
        <p>With some <a href="https://example.com">links</a> and formatting.</p>
        </body>
        </html>
        """
        
        # Test saving
        saved_path = safe_save_html(test_html, "Test HTML Report")
        
        if saved_path:
            print(f"✅ HTML saving works: {saved_path}")
            
            # Verify file exists and has content
            import os
            if os.path.exists(saved_path):
                file_size = os.path.getsize(saved_path)
                print(f"✅ File created successfully: {file_size} bytes")
                return True
            else:
                print(f"❌ File not found: {saved_path}")
                return False
        else:
            print("❌ HTML saving failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing HTML saving: {e}")
        return False

def main():
    print("🔧 HTML SAVING TEST")
    print("=" * 40)
    
    success = test_html_saving()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 HTML SAVING WORKS!")
        print("✅ The 'Failed to generate HTML for saving' error should be fixed")
    else:
        print("❌ HTML SAVING STILL HAS ISSUES")
        print("🔧 Check permissions and disk space")

if __name__ == "__main__":
    main() 