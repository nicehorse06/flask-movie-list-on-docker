import click

from flask.cli import FlaskGroup

from project import app, db, User, Movie

cli = FlaskGroup(app)


@cli.command("forge")
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的兩個變量移動到這個函數內
    name = 'Jimmy Ma'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


# 設置flask命令，可以重啟db資料，命令為
'''
$ flask initdb

or

$ flask initdb --drop
'''
@cli.command()  # 註冊為命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 設置選項
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判斷是否輸入了選項
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 輸出提示信息


# 設置註冊admin帳號的指令，option()用來寫入名稱和密碼，指令為flask admin
@cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 設置密碼
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 設置密碼
        db.session.add(user)

    db.session.commit()  # 提交數據庫會話
    click.echo('Done.')


if __name__ == "__main__":
    cli()
