import os
import sys
import requests
import json

def generate_web_page(markdown_content, api_key, secret_key):
    """
    Uses Baidu ERNIE to convert Markdown content into a single-file HTML web page.
    """
    
    # 1. Get Access Token
    token_url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key
    }
    
    print("Retrieving access token...")
    response = requests.post(token_url, params=params)
    if response.status_code != 200:
        print(f"Error getting token: {response.text}")
        return None
        
    access_token = response.json().get("access_token")
    if not access_token:
        print("No access token found in response.")
        return None

    # 2. Call ERNIE Bot (using ERNIE-4.0-8K or similar endpoint)
    # Endpoint for ERNIE-Bot-4
    ernie_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token={access_token}"
    
    prompt = f"""
    You are an expert web developer. I have the following content in Markdown format extracted from a PDF. 
    Your task is to convert this content into a stunning, modern, responsive single-page HTML website.
    
    Requirements:
    1. Use internal CSS for styling. Make it look professional (e.g., Google Fonts, nice color palette, responsive layout).
    2. Use semantic HTML5 tags.
    3. The content is provided below. Structure it logically.
    4. Return ONLY the HTML code, starting with <!DOCTYPE html> and ending with </html>. Do not include markdown code blocks (```html ... ```) in the output, just the raw HTML code.
    
    Markdown Content:
    {markdown_content}
    """
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "top_p": 0.8,
        "penalty_score": 1,
        "disable_search": False,
        "enable_citation": False
    })
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    print("Generating web page with ERNIE...")
    response = requests.post(ernie_url, headers=headers, data=payload)
    
    if response.status_code != 200:
        print(f"Error calling ERNIE: {response.text}")
        return None
        
    result = response.json()
    
    if "result" not in result:
        print(f"Error in ERNIE response: {result}")
        return None
        
    html_content = result["result"]
    
    # Cleanup: Remove markdown code fences if ERNIE included them despite instructions
    if html_content.startswith("```html"):
        html_content = html_content[7:]
    if html_content.endswith("```"):
        html_content = html_content[:-3]
        
    return html_content.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_web.py <path_to_markdown_file>")
        print("Please set ERNIE_API_KEY and ERNIE_SECRET_KEY environment variables.")
        sys.exit(1)
        
    md_file = sys.argv[1]
    
    api_key = os.environ.get("ERNIE_API_KEY")
    secret_key = os.environ.get("ERNIE_SECRET_KEY")
    
    if not api_key or not secret_key:
        print("Error: ERNIE_API_KEY and ERNIE_SECRET_KEY environment variables must be set.")
        sys.exit(1)
        
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    html_output = generate_web_page(content, api_key, secret_key)
    
    if html_output:
        output_path = md_file.replace(".pdf.md", ".html").replace(".md", ".html")
        if output_path == md_file:
            output_path += ".html"
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"Web page saved to {output_path}")
