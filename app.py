from flask import (
    Flask, request, render_template, url_for, redirect, flash, session, jsonify)
from flask_cors import CORS  # CORS 라이브러리 임포트

import openai
import os
import markdown

app = Flask(__name__)
app.secret_key = 'dlwndud124@'

users = {'abc' : '1234'}

#.env로부터 API KEY 획득
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
#기본 파라미터 설정
MODEL = 'gpt-4-turbo'
TEMPERATURE = 0.0
MAX_TOKENS = 128000

# Basic function
# 기본 함수: context의 메시지가 최대 길이를 초과했는지 확인하는 코드
def check_tokens(items):
    cnt = 0

    if items is None:
        return cnt

    for item in items:
        cnt += len(item['content'])

    return cnt

CORS(app)

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/query')
    else:
        return redirect('/login')
    
@app.route('/login', methods=['GET', 'POST'])
def login() :
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password :
            session['username'] = username
            return redirect('/query')    
        else:
            return '''
            <script>
                alert("올바른 ID와 비밀번호를 입력해주세요.");
                window.location.href = '/login';
            </script>
            '''
    else :
        return render_template('login.html')


@app.route('/query', methods=['GET', 'POST'])
def query() :
    if request.method == 'POST':
        # JSON 데이터 접근
        data = request.get_json()
        # 이제 여기서 JSON 데이터를 볼 수 있습니다.
        message = data['question'][-1]

        context = []
        if len(context) == 0:
            context.append({"role": "system", "content": "You are a helpful assistant."})
            context.append({"role": "user", "content": message})
        else:
            context.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(model=MODEL,
                                                    messages=context,
                                                    temperature=TEMPERATURE)
        
        answer = response['choices'][0]['message']['content']
        #codes = codes = markdown.markdown(answer, extensions=['fenced_code', 'codehilite'])

        # 대화 목록에 추가
        context.append({'role': 'assistant', 'content': answer})

        return {'response' : answer }
    else :
        return render_template('query.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)