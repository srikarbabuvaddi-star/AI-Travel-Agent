from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✈️ AI Smart Travel Agent</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        .container {
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2.5rem;
            max-width: 650px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
            text-align: center;
        }
        .logo { font-size: 3.5rem; margin-bottom: 1rem; }
        h1 {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.8rem;
        }
        p { color: #94a3b8; font-size: 1.05rem; line-height: 1.6; margin-bottom: 1.5rem; }
        .badge {
            display: inline-block;
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 0.4rem 1rem;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.85rem;
            margin-bottom: 1.5rem;
        }
        .card {
            background: #0f172a;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.2rem;
            text-align: left;
            margin-bottom: 1.5rem;
        }
        .card h3 { color: #f3f4f6; font-size: 1.1rem; margin-bottom: 0.5rem; }
        .card code {
            display: block;
            background: #1e293b;
            color: #38bdf8;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-family: monospace;
            font-size: 0.95rem;
            margin-top: 0.5rem;
        }
        .btn-group { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
        .btn {
            display: inline-block;
            background: linear-gradient(90deg, #2563eb, #3b82f6);
            color: white;
            text-decoration: none;
            padding: 0.85rem 1.8rem;
            border-radius: 10px;
            font-weight: 700;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(59, 130, 246, 0.4); }
        .btn-secondary {
            background: #334155;
            color: #f8fafc;
        }
        .btn-secondary:hover { background: #475569; box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3); }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">✈️</div>
        <h1>AI Smart Travel Agent</h1>
        <div class="badge">⚡ Autonomous MCP Multi-Tool Engine</div>
        <p>This application is powered by an interactive Streamlit framework with real-time MCP tools (Weather, Places, Hotels, Transport, Budget & AI Score).</p>
        
        <div class="card">
            <h3>🌐 Streamlit Community Cloud (Recommended Free Hosting):</h3>
            <p style="font-size: 0.9rem; margin-bottom: 0.4rem;">Streamlit apps require WebSocket servers. Deploy live in 1-click on Streamlit Cloud:</p>
            <code>https://share.streamlit.io</code>
        </div>

        <div class="card">
            <h3>💻 Run Interactive App Locally:</h3>
            <code>streamlit run app.py</code>
        </div>

        <div class="btn-group">
            <a href="https://share.streamlit.io" target="_blank" class="btn">🚀 Deploy on Streamlit Cloud</a>
            <a href="https://github.com/srikarbabuvaddi-star/AI-Travel-Agent" target="_blank" class="btn btn-secondary">📁 GitHub Repository</a>
        </div>
    </div>
</body>
</html>"""
        self.wfile.write(html_content.encode('utf-8'))
