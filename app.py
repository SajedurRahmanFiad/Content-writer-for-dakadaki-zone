from flask import Flask, request, render_template_string, jsonify
from agno.agent import Agent
from agno.models.google import Gemini
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Load sample writings
sample_writings = open('sample writings.txt', encoding='utf-8').read()

agent = Agent(
    role="Professional marketing content writer",
    description=f"Writes professional bengali content for ecommerce facebook page posts. Below are the sample writings:\n\n{sample_writings}",
    instructions=[
        "You will be provided a product name and a special context (Optional). Your responsibility is to write a professional content for a facebook page post.",
        "Write the content with necessary branding of the page Dakadaki zone. Our products are bird foods, bird accessories and bird toys.",
        "Use necessary emojis to make it attractive.",
        "Use psychology and necessary informations for marketing and making people interested to buy it.",
        "Use hashtags at the end.",
        "Don't add anything else or extra texts rather than the main content",
        "IMPORTANT: THE CONTENT MUST BE IN BENGALI."
    ],
    model=Gemini(id="gemini-2.0-flash"),
    markdown=True,
)

def Generate_Content(product_name, context=None):
    return agent.run(f"Product Name: {product_name}, Context: {context}").content

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; }
        #loading { display: none; text-align: center; margin-top: 20px; }
        #response-container { margin-top: 20px; display: none; }
        #response { width: 100%; height: 200px; }
        footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f8f9fa; /* Light background for visibility */
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            color: #333;
            border-top: 1px solid #dee2e6; /* Subtle border */
            z-index: 1000; /* Ensure it stays above other content */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">AI Content writer for Dakadaki Zone</h1>
        <form id="content-form">
            <div class="mb-3">
                <label for="product_name" class="form-label">Product Name</label>
                <input type="text" class="form-control" id="product_name" name="product_name" placeholder="(Bengali)" required>
            </div>
            <div class="mb-3">
                <label for="context" class="form-label">Context (Optional)</label>
                <input type="text" class="form-control" id="context" name="context" placeholder="(Bengali)">
            </div>
            <button type="submit" class="btn btn-primary">Generate</button>
        </form>
        <div id="loading">
            <div class="spinner-border text-primary" role="status"></div>
            <p>Generating content...</p>
        </div>
        <div id="response-container">
            <h5>Generated Content:</h5>
            <textarea id="response" class="form-control" readonly></textarea>
            <button id="copy-btn" class="btn btn-secondary mt-2">Copy to Clipboard</button>
        </div>
    </div>
    <footer>Developed by <a href="https://www.facebook.com/fiad.me" target="_blank">Md Sajedur Rahman Fiad</a></footer>
    <script>
        document.getElementById('content-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            document.getElementById('loading').style.display = 'block';
            document.getElementById('response-container').style.display = 'none';
            const formData = new FormData(this);
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                document.getElementById('response').value = data.content;
                document.getElementById('response-container').style.display = 'block';
            } catch (error) {
                alert('Error generating content');
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        document.getElementById('copy-btn').addEventListener('click', function() {
            const textarea = document.getElementById('response');
            textarea.select();
            document.execCommand('copy');
            alert('Copied to clipboard!');
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    product_name = request.form['product_name']
    context = request.form.get('context', None)
    content = Generate_Content(product_name, context)
    return jsonify({'content': content})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
