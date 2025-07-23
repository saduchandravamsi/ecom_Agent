# api_server.py
from flask import Flask, request, render_template_string
import json
from ecommerce_agent import answer_question

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>E-commerce AI Agent API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #0d6efd; }
        h2 { color: #212529; }
        code { background: #f8f9fa; padding: 2px 4px; border-radius: 3px; }
        #question { width: 100%; max-width: 500px; margin: 10px 0; padding: 8px; font-size: 16px; }
        button { padding: 8px 16px; background: #0d6efd; color: white; border: none; border-radius: 4px; cursor: pointer; }
        pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .panel { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .json-panel { background: #e9ecef; padding: 10px; }
        .error { color: #dc3545; }
    </style>
</head>
<body>
    <h1>E-commerce AI Agent API</h1>

    <div class="panel">
        <h2>Browser Test Form</h2>
        <p>Enter your e-commerce analytics question below:</p>
        <input type="text" id="question" placeholder="What is the total sales across all products?" />
        <button id="askButton">Ask</button>
        <div id="resultPanel" style="margin-top: 20px;">
            <div id="friendlyPanel" class="panel">Friendly Answer: <span style="font-weight:bold;" id="friendly"></span></div>
            <div id="answerPanel" class="panel">
                <div style="font-weight:bold;">Full Answer (JSON):</div>
                <pre id="answer"></pre>
            </div>
        </div>
    </div>

    <div class="panel">
        <h2>API Usage</h2>
        <p>Send <b>POST</b> requests to <code>/ask</code> with a JSON body like:</p>
        <pre>{"question": "What is the total sales across all products?"}</pre>
        <p>Example with curl:</p>
        <pre>curl -X POST http://localhost:8000/ask \\
  -H "Content-Type: application/json" \\
  -d '{"question": "What is the total sales across all products?"}'</pre>
        <p>Check server status at <a href="/health" target="_blank"><code>/health</code></a>.</p>
    </div>

    <script>
        document.getElementById('askButton').onclick = async function() {
            const question = document.getElementById('question').value.trim();
            if (!question) return;
            const resultPanel = document.getElementById('resultPanel');
            const friendlyPanel = document.getElementById('friendly');
            const answerPanel = document.getElementById('answer');

            resultPanel.style.display = 'block';
            friendlyPanel.textContent = "Loading...";
            answerPanel.textContent = "Loading...";

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });
                const data = await response.json();
                friendlyPanel.textContent = data.friendly || data.error || "--";
                friendlyPanel.className = data.status === 'error' ? 'error' : '';
                answerPanel.textContent = JSON.stringify(data, null, 2);
            } catch (err) {
                friendlyPanel.textContent = "Error: " + err.message;
                friendlyPanel.className = 'error';
                answerPanel.textContent = "";
            }
        };
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML)

@app.route('/ask', methods=['POST'])
def ask():
    if not request.is_json:
        return json.dumps({"status": "error", "error": "Request must be JSON."}), 400
    data = request.get_json()
    if not data or 'question' not in data:
        return json.dumps({"status": "error", "error": "Missing 'question' in request."}), 400
    return answer_question(data['question'])

@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

# from flask import Flask, request, jsonify, render_template_string
# from ecommerce_agent import answer_question

# app = Flask(__name__)

# # --- API Endpoints ---

# @app.route('/ask', methods=['POST'])
# def ask():
#     if not request.is_json:
#         return jsonify({"status": "error", "error": "Request must be JSON"}), 400
#     data = request.get_json()
#     if not data or 'question' not in data:
#         return jsonify({"status": "error", "error": "Missing 'question' in request"}), 400
#     result = answer_question(data['question'])
#     return jsonify(result)

# @app.route('/health', methods=['GET'])
# def health():
#     return jsonify({"status": "healthy"})

# # --- Homepage & Browser UI ---

# HOME_HTML = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>E-commerce AI Agent API</title>
#     <style>
#         body { font-family: sans-serif; margin: 40px; }
#         h1, h2 { color: #333; }
#         code { background: #f5f5f5; padding: 2px 4px; border-radius: 3px; }
#         textarea { width: 100%; height: 100px; margin: 10px 0; }
#         button { padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
#         pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
#     </style>
# </head>
# <body>
#     <h1>E-commerce AI Agent API</h1>

#     <h2>Browser Test Form</h2>
#     <form action="/ask" method="post" id="questionForm">
#         <label for="question">Ask a question:</label><br>
#         <textarea id="question" name="question" placeholder="What is the total sales across all products?"></textarea><br>
#         <button type="submit">Ask</button>
#     </form>
#     <pre id="result">Submit a question above to see the answer...</pre>

#     <h2>Usage</h2>
#     <p><strong>POST /ask</strong> (with JSON body <code>{"question": "..."}</code>) – Agent Q&A</p>
#     <p><strong>GET /health</strong> – Check server status</p>
#     <p>See logs in your terminal for SQL and debug output.</p>

#     <h2>Examples</h2>
#     <ul>
#         <li>What is the total sales across all products?</li>
#         <li>Which product had the highest CPC?</li>
#         <li>Calculate the RoAS (Return on Ad Spend).</li>
#         <li>List all eligible products.</li>
#         <li>Show total ad spend by product.</li>
#         <li>How many units were sold via ads for product P1001?</li>
#     </ul>

#     <script>
#         document.getElementById('questionForm').onsubmit = async function(e) {
#             e.preventDefault();
#             const question = document.getElementById('question').value;
#             const result = document.getElementById('result');
#             result.textContent = "Loading...";
#             try {
#                 const response = await fetch('/ask', {
#                     method: 'POST',
#                     headers: { 'Content-Type': 'application/json' },
#                     body: JSON.stringify({ question })
#                 });
#                 const data = await response.json();
#                 result.textContent = JSON.stringify(data, null, 2);
#             } catch (error) {
#                 result.textContent = "Error: " + error.message;
#             }
#         };
#     </script>
# </body>
# </html>
# """

# @app.route('/', methods=['GET'])
# def home():
#     return render_template_string(HOME_HTML)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
