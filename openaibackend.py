import spacy
from jinja2 import Template
import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Load spaCy model for text parsing
nlp = spacy.load("en_core_web_sm")

# UI Component Definitions
UI_COMPONENTS = {
    "navigation bar": "<nav class='navbar'><ul><li><a href='#'>Home</a></li><li><a href='#'>About</a></li><li><a href='#'>Contact</a></li></ul></nav>",
    "hero section": "<div class='hero-section'><h1>Welcome</h1><p>Your tagline here</p></div>",
    "button": "<button class='button'>Click Me</button>",
    "text input": "<input type='text' class='text-input' placeholder='Enter text'>",
    "email input": "<input type='email' class='email-input' placeholder='Enter email'>",
    "password input": "<input type='password' class='password-input' placeholder='Enter password'>",
    "footer": "<footer class='footer'>Footer Content</footer>",
    "card": "<div class='card'><h3>Card Title</h3><p>Card content here.</p></div>",
    "chart": "<div class='chart'>Chart Placeholder</div>",
    "image placeholder": "<div class='image-placeholder'>Image Here</div>",
}

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated UI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
        .navbar ul { list-style-type: none; padding: 0; display: flex; gap: 10px; }
        .navbar li { display: inline; }
        .button { background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; }
        .text-input, .email-input, .password-input { padding: 10px; margin: 10px 0; width: 300px; border: 1px solid #ccc; border-radius: 5px; }
        .hero-section { padding: 20px; text-align: center; background: #ddd; }
        .card { padding: 20px; background: white; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .footer { background-color: #333; color: white; padding: 10px; text-align: center; }
        .image-placeholder { width: 300px; height: 200px; background-color: #ccc; display: flex; align-items: center; justify-content: center; margin: 20px 0; }
    </style>
</head>
<body>
    {% for component in components %}
        {{ component|safe }}
    {% endfor %}
</body>
</html>
"""

# Text Parsing Function
def parse_description(description):
    doc = nlp(description.lower())
    components = []

    if "login" in description or "sign in" in description:
        components.extend([UI_COMPONENTS["email input"], UI_COMPONENTS["password input"], UI_COMPONENTS["button"]])
    if "dashboard" in description:
        components.extend([UI_COMPONENTS["navigation bar"], UI_COMPONENTS["card"], UI_COMPONENTS["chart"]])
    if "image" in description:
        components.append(UI_COMPONENTS["image placeholder"])
    if "form" in description:
        components.extend([UI_COMPONENTS["text input"], UI_COMPONENTS["email input"], UI_COMPONENTS["button"]])
    if "footer" in description:
        components.append(UI_COMPONENTS["footer"])
    if "homepage" in description or "landing page" in description:
        components.insert(0, UI_COMPONENTS["hero section"])

    return components

# Generate HTML from components
def generate_html(components):
    template = Template(HTML_TEMPLATE)
    return template.render(components=components)

# Function to save a screenshot of the webpage
def save_screenshot(html_code, output_path="screenshot.png"):
    """Render the HTML code in a headless browser and save a screenshot."""
    temp_file = "temp_ui.html"
    with open(temp_file, "w") as f:
        f.write(html_code)

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("file://" + os.path.abspath(temp_file))
        time.sleep(2)  # Allow time for the page to load
        driver.save_screenshot(output_path)
    finally:
        driver.quit()
        os.remove(temp_file)  # Clean up temporary file

    return output_path

# Function to export the generated UI to Figma
def export_to_figma(html_code, figma_api_token):
    """Export the generated design to Figma using their API."""
    headers = {"X-Figma-Token": figma_api_token}
    data = {
        "name": "Generated_UI_Design",
        "description": "UI generated from user input.",
        "html_content": html_code,  # Assuming Figma API supports raw HTML input.
    }
    
    # Figma API endpoint (customize if required based on their documentation)
    figma_endpoint = "https://api.figma.com/v1/files"

    try:
        response = requests.post(figma_endpoint, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for HTTP issues
        return response.json()  # Return the API response
    except requests.exceptions.RequestException as e:
        print(f"Figma Export Error: {e}")
        return {"error": str(e)}
def generate_ui_from_description(description, figma_token=None):
    """Generate UI design based on user input and export to Figma if token provided."""
    components = parse_description(description)
    html_code = generate_html(components)
    
    # Save the screenshot locally
    screenshot_path = save_screenshot(html_code)

    # If a Figma token is provided, export the HTML to Figma
    figma_response = None
    if figma_token:
        figma_response = export_to_figma(html_code, figma_token)
        if "error" not in figma_response:
            print("Successfully exported to Figma.")
        else:
            print("Figma Export Failed:", figma_response.get("error"))

    return {"screenshot": screenshot_path, "figma_response": figma_response}

