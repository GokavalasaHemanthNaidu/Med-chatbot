from flask import Flask, request, jsonify, render_template_string
from chatbot_py import respond

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(
        """
        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>MedBot</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                #container { max-width: 700px; margin: 0 auto; background: #fff; border: 1px solid #ddd; border-radius: 6px; }
                #messages { height: 400px; overflow-y: auto; padding: 10px; border-bottom: 1px solid #eee; }
                .msg { margin: 8px 0; }
                .me { color: #333; }
                .bot { color: #1c6ef2; }
                #input { display: flex; padding: 10px; }
                #input input { flex: 1; padding: 10px; font-size: 14px; }
                #input button { margin-left: 8px; padding: 10px 14px; }
            </style>
        </head>
        <body>
            <div id="container">
                <div id="messages"></div>
                <div id="input">
                    <input id="message" placeholder="Type your message..." />
                    <button onclick="send()">Send</button>
                </div>
            </div>
            <script>
                async function send() {
                    const inp = document.getElementById('message');
                    const text = inp.value.trim();
                    if (!text) return;
                    append('me', text);
                    inp.value='';
                    try {
                        const res = await fetch('/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text }) });
                        const data = await res.json();
                        append('bot', data.reply);
                    } catch (e) {
                        append('bot', 'Error contacting server');
                    }
                }
                function append(who, text) {
                    const m = document.createElement('div');
                    m.className = 'msg ' + (who==='me'?'me':'bot');
                    m.textContent = (who==='me'? 'You: ' : 'MedBot: ') + text;
                    document.getElementById('messages').appendChild(m);
                    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
                }
            </script>
        </body>
        </html>
        """
    )

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    reply = respond(message)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)