from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('mongodb+srv://ongsim0629:subin0629@cluster0.p8xwfrb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.project0



# HTML 화면 보여주기 
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/books/list', methods=['GET'])
def show_books():
    # 1. db에서 books 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    book_list = list(db.books.find({},{"_id" : False}).sort("like", -1))
    # 2. 성공하면 success 메시지와 함께 all_books 목록을 클라이언트에 전달합니다.
    return jsonify({"result" : "success", "all_books" : book_list})


@app.route('/api/books/like', methods=['POST'])
def like_book():
    # 1. 클라이언트가 전달한 title_give를 title_receive 변수에 넣습니다.
    title_receive = request.form['title_give']
    # 2. books 목록에서 find_one으로 title이 title_receive와 일치하는 book을 찾습니다.
    book = db.books.find_one({"title":title_receive})
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = book['like'] + 1
    # 4. books 목록에서 title이 title_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!
    db.books.update_one({"title":title_receive},{'$set': {"like": new_like}})
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '좋아요 처리 완료!'})


@app.route('/api/books/delete', methods=['POST'])
def delete_book():
    # 1. 클라이언트가 전달한 title_give를 title_receive 변수에 넣습니다.
    title_receive = request.form['title_give']
    # 2. books 목록에서 delete_one으로 title이 title_receive와 일치하는 book을 제거합니다.
    db.books.delete_one({"title":title_receive})    
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '삭제 처리 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)