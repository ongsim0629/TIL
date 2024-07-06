from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
app = Flask(__name__)

# db 처리
client = MongoClient('mongodb+srv://ongsim0629:subin0629@cluster0.p8xwfrb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.project0

# HTML 처리
@app.route('/')
def home():
   return render_template('index.html')

# API 목록
# 할 일 목록 출력 API
@app.route('/api/todos/list', methods=['GET'])
def show_todo():
   # db에서 todo 목록 전체 검색 -> 완료처리 된 todo들을 먼저 띄워줌
   todo_list = list(db.testtodo.find({},{"_id" : False}).sort("complete", -1))
   # 성공하면 결과 -> success에, todo_list는 todos에 저장해서 client에 전달
   return jsonify({"result" : "success", "todos" : todo_list})

# 할 일 추가 API
@app.route('/api/todos', methods=['POST'])
def append_todo():
    # 클라이언트가 전달한 todo_give를 todo_receive 변수에 저장
    todo_receive = request.form['todo_give']
    # 클라이언트가 작성한 할 일을 바탕으로 db에 insert할 내용 작성
    todo = {'todo':todo_receive,'complete':0}
    # 3. db에 insert
    db.testtodo.insert_one(todo)
    # 5. 성공하면 success 메시지를 반환
    return jsonify({'result': 'success', 'msg': '등록 완료!'})

# 할 일 삭제 API
@app.route('/api/todos/delete', methods=['POST'])
def delete_todo():
    # 클라이언트가 전달한 todo_give를 todo_receive 변수에 저장
    todo_receive = request.form['todo_give']
    # todos 목록에서 delete_one으로 todo가 todo_receive와 일치하는 todo 제거
    db.testtodo.delete_one({"todo":todo_receive})    
    # 성공하면 success 메시지 반환
    return jsonify({'result': 'success', 'msg': '할 일 삭제 완료!'})

# 할 일 완료 API
@app.route('/api/todos/complete', methods=['POST'])
def complete_todo():
    # 클라이언트가 전달한 todo_give를 todo_receive 변수에 저장
    todo_receive = request.form['todo_give']
    # todos 목록에서 find_one으로 todo가 todo_receive와 일치하는 todo를 탐색
    todo = db.testtodo.find_one({"todo": todo_receive})
    # todo의 complete 에 1을 더해준 new_complete 변수 만들기
    new_complete = todo['complete'] + 1
    # db에 변경사항 업데이트
    db.testtodo.update_one({"todo":todo_receive},{'$set': {"complete": new_complete}})
    # 성공하면 success 메시지 반환
    return jsonify({'result': 'success', 'msg': '할 일 체크 완료!'})

# 할 일 완료 취소 API
@app.route('/api/todos/incomplete', methods=['POST'])
def incomplete_todo():
    # 클라이언트가 전달한 todo_give를 todo_receive 변수에 저장
    todo_receive = request.form['todo_give']
    # todos 목록에서 find_one으로 todo가 todo_receive와 일치하는 todo를 탐색
    todo = db.testtodo.find_one({"todo": todo_receive})
    # todo의 complete 에 1을 빼준 new_complete 변수 만들기
    new_complete = todo['complete'] - 1
    # db에 변경사항 업데이트
    db.testtodo.update_one({"todo":todo_receive},{'$set': {"complete": new_complete}})
    # 성공하면 success 메시지 반환
    return jsonify({'result': 'success', 'msg': '할 일 체크 취소 완료!'})

# 할 일 수정 API
@app.route('/api/todos/update', methods=['POST'])
def update_todo():
    # 클라이언트가 전달한 todo_give를 todo_receive 변수에 저장
    todo_receive = request.form['todo_give']
    # 클라이언트가 전달한 new_todo를 new_todo 변수에 저장
    new_todo = request.form['new_todo']
    # todo의 내용이 수정 전의 todo와 일치하는 db의 값에 새로운 todo를 업데이트
    db.testtodo.update_one({"todo":todo_receive},{'$set': {"todo": new_todo}})
    # 성공하면 success 메시지 반환
    return jsonify({'result': 'success', 'msg': '할 일 업데이트 완료!'})

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)