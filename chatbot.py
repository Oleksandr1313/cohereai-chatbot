from flask import *
import cohere
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

cohere_client = cohere.Client('api-key')

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        user_message = request.form['message']
        print(f"User message: {user_message}")

        response = cohere_client.generate(
            model='command-xlarge-nightly',
            prompt=f'User: {user_message}\nBot:', 
            max_tokens=150, 
            temperature=0.7
        )

        bot_reply = response.generations[0].text.strip()
        print(f"Bot reply: {bot_reply}")

        session['chat_history'].append({'role': 'User', 'message': user_message})
        session['chat_history'].append({'role': 'Bot', 'message': bot_reply})
        session.modified = True

    return render_template('index.html', chat_history=session['chat_history'])

@app.route('/clear')
def clear():
    session.pop('chat_history', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
