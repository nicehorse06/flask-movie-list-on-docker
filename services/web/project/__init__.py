import os
import sys
import click
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for,
    flash,
    render_template
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)  # 初始化DB

login_manager = LoginManager(app)  # 初始化登入類

# Flask-Login提供一個current_user的變數，如果已登入，此view回傳該用戶model
@login_manager.user_loader
def load_user(user_id):  # 創建用戶加載回調函數，接受用戶 ID 作為參數
    user = User.query.get(int(user_id))  # 用 ID 作為 User 模型的主鍵查詢對應的用戶
    return user  # 返回用戶對象


# 宣告表的 schema
# 繼承UserMixin，可以多一些實用的方法，如is_authenticated判斷是否登入
class User(db.Model, UserMixin):  # 表名將會是 user（自動生成，小寫處理）
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))  # 密碼hash，不直接操作

    # 用來設置密碼
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 用來驗證密碼
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):  # 表名將會是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    title = db.Column(db.String(60))  # 電影標題
    year = db.Column(db.String(4))  # 電影年份


# 宣告路由
@app.route('/', methods=['GET', 'POST'])
def index():
    # request的值只有在view內才能調用，存在一些接收請求的參數
    if request.method == 'POST':
        # 因為@login_required會限制到整個view，而這裡只對POST做限制，故用current_user的方法做判斷
        if not current_user.is_authenticated:  # 如果當前用戶未認證
            return redirect(url_for('index'))  # 重定向到主頁
        # 獲取表單數據
        title = request.form.get('title')
        year = request.form.get('year')

        # 驗證資料
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))  # 回主頁面

        # 儲存資料
        movie = Movie(title=title, year=year)

        # 儲存於記憶體
        db.session.add(movie)
        # 真正存於DB
        db.session.commit()

        # flash連動template中的 get_flashed_messages()
        flash('Item created.')
        return redirect(url_for('index'))
    movies = Movie.query.all()  # 讀取所有電影記錄
    return render_template('index.html', movies=movies)


# 編輯文章
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回對應的編輯頁面

        movie.title = title  # 更新標題
        movie.year = year  # 更新年份
        db.session.commit()  # 提交數據庫會話
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主頁

    return render_template('edit.html', movie=movie)  # 傳入被編輯的電影記錄


# 刪除文章
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定POST
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)  # 刪除對應紀錄
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


# 登入功能
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 驗證失敗轉回登入頁面
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        # todo 這裡用戶只有一個時可以這樣用
        user = User.query.first()
        # 驗證用戶名和密碼是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用戶
            flash('Login success.')
            # 驗證成功回主頁面
            return redirect(url_for('index'))  # 重定向到主頁

        flash('Invalid username or password.')  # 如果驗證失敗，顯示錯誤消息
        return redirect(url_for('login'))  # 重定向回登錄頁面

    return render_template('login.html')


# 用戶登出登入的模組
@app.route('/logout', methods=['GET'])
@login_required  # 用於視圖保護，後面會詳細介紹
def logout():
    logout_user()  # 登出用戶
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首頁


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 會返回當前登錄用戶的數據庫記錄對象
        # 等同於下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.errorhandler(404)  # 傳入要處理的錯誤代碼
def page_not_found(e):  # 接受異常對象作為參數
    return render_template('404.html'), 404  # 返回模板和狀態碼


# context_processor裝飾器可以把很常用到的變量放到模板中，需回傳dict
@app.context_processor
def inject_user():  # 函數名可以隨意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同於return {'user': user}
