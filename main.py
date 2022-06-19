from flask import Flask, render_template, request, url_for, flash, redirect, session
import sqlite3
from werkzeug.exceptions import abort
import re
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')

def index():
    conn = get_db_connection()
    View = conn.execute('SELECT * FROM View').fetchall()
    return render_template('index.html', View=View)



def get_post(post_id,table):
    conn = get_db_connection()
    post = conn.execute(table,
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id, 'SELECT * FROM View WHERE id_ткани = ?')
    return render_template('post.html', post=post)

##################################################################################
#################################################################################
########## Категории тканей ####################

@app.route('/costume')
def costume():
    conn = get_db_connection()
    cost = conn.execute('SELECT * FROM View WHERE назначение_ткани LIKE ?  ', ('Костюмные',)).fetchall()
    return render_template('costume.html', cost=cost)

@app.route('/childish')
def childish():
    conn = get_db_connection()
    cost = conn.execute('SELECT * FROM View WHERE назначение_ткани LIKE ?  ', ('Детские',)).fetchall()
    return render_template('costume.html', cost=cost)

@app.route('/elegant')
def elegant():
    conn = get_db_connection()
    cost = conn.execute('SELECT * FROM View WHERE назначение_ткани LIKE ?  ', ('Нарядные',)).fetchall()
    return render_template('costume.html', cost=cost)


##################################################################################
##################################################################################

@app.route('/allproducer')
def allproducer():
    conn = get_db_connection()
    allproducer = conn.execute('SELECT * FROM производитель').fetchall()
    conn.close()
    return render_template('allproducer.html', allproducer=allproducer)

@app.route('/allmaterial')
def allmaterial():
    conn = get_db_connection()
    allmaterial = conn.execute('SELECT * FROM материал_ткани').fetchall()
    conn.close()
    return render_template('allmaterial.html', allmaterial=allmaterial)

@app.route('/alldiscount')
def alldiscount():
    conn = get_db_connection()
    alldiscount = conn.execute('SELECT * FROM скидка').fetchall()
    conn.close()
    return render_template('alldiscount.html', alldiscount=alldiscount)

@app.route('/allcomposition')
def allcomposition():
    conn = get_db_connection()
    allcomposition = conn.execute('SELECT * FROM View_Cond').fetchall()
    conn.close()
    return render_template('allcomposition.html', allcomposition=allcomposition)

@app.route('/allcloth')
def allcloth():
    conn = get_db_connection()
    allcloth = conn.execute('SELECT * FROM View').fetchall()
    conn.close()
    return render_template('allcloth.html', allcloth=allcloth)
##################################################################################
############## поиск ############################

@app.route('/search', methods=('GET', 'POST'))
def search():
    conn = get_db_connection()
    cur = conn.cursor()
    mater = cur.execute('SELECT * FROM материал_ткани ').fetchall()
    purpose = cur.execute('SELECT * FROM ткань ').fetchall()
    disc = cur.execute('SELECT * FROM скидка').fetchall()
    if request.method == 'POST':
        материал = request.form['материал']
        назначение = request.form['назначение']
        мин_цена = request.form['мин_цена']
        макс_цена = request.form['макс_цена']
        скидка = request.form['скидка']
        post = conn.execute('SELECT * FROM View WHERE материал LIKE ?  ', (материал,)).fetchall()
        nash = conn.execute('SELECT * FROM View WHERE назначение_ткани LIKE ?  ', (назначение,)).fetchall()
        dis = conn.execute('SELECT * FROM View WHERE величина_скидки LIKE ?  ', (скидка,)).fetchall()
        cash = conn.execute('SELECT * FROM View WHERE цена_за_метр  >= ? AND цена_за_метр <= ?  ', (мин_цена, макс_цена)).fetchall()
        conn.commit()
        conn.close()
        return render_template('search.html', post=post, nash=nash, cash=cash, dis=dis)

    return render_template('search.html', mater=mater, purpose=purpose,  disc=disc)


############## поиск  ############################
##################################################################################


@app.route('/allcloth/<int:id>/edit', methods=('GET', 'POST'))
def edit_cloth(id):
    post = get_post(id, 'SELECT * FROM View WHERE id_ткани = ?')
    conn = get_db_connection()
    cur = conn.cursor()
    prod = cur.execute('SELECT * FROM производитель ').fetchall()
    disc = cur.execute('SELECT * FROM скидка ').fetchall()
    if request.method == 'POST':
        название_ткани = request.form['название_ткани']
        цена_за_метр = request.form['цена_за_метр']
        цвет = request.form['цвет']
        назначение_ткани = request.form['назначение_ткани']
        тип_ткани = request.form['тип_ткани']
        ширина_ткани = request.form['ширина_ткани']
        фото_ткани = request.form['фото_ткани']
        страна_производитель = request.form['страна_производитель']
        название_скидки = request.form['название_скидки']

        if not название_ткани:
            flash('процентное содержание is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            a = cur.execute('SELECT id_производителя FROM производитель WHERE страна_производитель LIKE ?  ', (страна_производитель,)).fetchall()[0][0]
            b = cur.execute('SELECT id_скидки FROM скидка WHERE название LIKE ?  ', (название_скидки,)).fetchall()[0][0]
            conn.execute('UPDATE ткань SET название= ?, цена_за_метр= ?, цвет= ?, назначение= ?, тип_ткани= ?,ширина_ткани=?, фото_ткани= ?, id_производителя= ?, id_скидки= ?'
                         ' WHERE id_ткани = ?',
                         (название_ткани, цена_за_метр, цвет, назначение_ткани, тип_ткани, ширина_ткани, фото_ткани, a, b, id))
            conn.commit()
            conn.close()
            return redirect(url_for('allcloth'))

    return render_template('edit_cloth.html', post=post, prod=prod, disc=disc)


@app.route('/allcloth/<int:id>/delete', methods=('POST',))
def delete_cloth(id):
    post = get_post(id, 'SELECT * FROM ткань WHERE id_ткани = ?')
    conn = get_db_connection()
    conn.execute('DELETE FROM ткань WHERE id_ткани = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['название']))
    return redirect(url_for('allcloth'))

@app.route('/allcomposition/<int:id>/edit', methods=('GET', 'POST'))
def edit_comp(id):
    post = get_post(id, 'SELECT * FROM View_Cond WHERE id_состава_ткани = ?')
    conn = get_db_connection()
    cur = conn.cursor()
    mater = cur.execute('SELECT * FROM материал_ткани ').fetchall()
    clot = cur.execute('SELECT * FROM ткань ').fetchall()
    if request.method == 'POST':
        название_ткани = request.form['название_ткани']
        материал = request.form['материал']
        процентное_содержание_состава = request.form['процентное_содержание_состава']


        if not процентное_содержание_состава:
            flash('процентное содержание is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            a = cur.execute('SELECT id_материала FROM материал_ткани WHERE материал LIKE ?  ', (материал,)).fetchall()[0][0]
            b = cur.execute('SELECT id_ткани FROM ткань WHERE название LIKE ?  ', (название_ткани,)).fetchall()[0][0]
            conn.execute('UPDATE состав_ткани SET процентное_содержание= ?, id_материала= ?, id_ткани= ?'
                         ' WHERE id_состав_ткани = ?',
                         (процентное_содержание_состава, a, b, id))


            conn.commit()
            conn.close()
            return redirect(url_for('allcomposition'))

    return render_template('edit_comp.html', post=post, mater=mater, clot=clot)

@app.route('/allcomposition/<int:id>/delete', methods=('POST',))
def delete_comp(id):
    post = get_post(id, 'SELECT * FROM состав_ткани WHERE id_состав_ткани = ?')
    conn = get_db_connection()
    conn.execute('DELETE FROM состав_ткани WHERE id_состав_ткани = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['процентное_содержание_состава']))
    return redirect(url_for('allcomposition'))

@app.route('/alldiscount/<int:id>/edit', methods=('GET', 'POST'))
def edit_dis(id):
    post = get_post(id, 'SELECT * FROM скидка WHERE id_скидки = ?')

    if request.method == 'POST':
        название = request.form['название']
        величина_скидки = request.form['величина_скидки']
        дата_начала_скидки = request.form['дата_начала_скидки']
        дата_конца_скидки = request.form['дата_конца_скидки']

        if not название:
            flash('скидка is required!')
        else:
            conn = get_db_connection()

            conn.execute('UPDATE скидка SET название= ?,величина_скидки= ?,дата_начала_скидки= ?,дата_конца_скидки= ?'
                         ' WHERE id_скидки = ?',
                         (название, величина_скидки, дата_начала_скидки, дата_конца_скидки,  id))
            conn.commit()
            conn.close()
            return redirect(url_for('alldiscount'))

    return render_template('edit_dis.html', post=post)

@app.route('/alldiscount/<int:id>/delete', methods=('POST',))
def delete_dis(id):
    post = get_post(id, 'SELECT * FROM скидка WHERE id_скидки = ?')
    conn = get_db_connection()
    conn.execute('DELETE FROM скидка WHERE id_скидки = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['название']))
    return redirect(url_for('alldiscount'))

@app.route('/allmaterial/<int:id>/edit', methods=('GET', 'POST'))
def edit_mr(id):
    post = get_post(id, 'SELECT * FROM материал_ткани WHERE id_материала = ?')

    if request.method == 'POST':
        материал = request.form['материал']

        if not материал:
            flash('материал is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE материал_ткани SET материал = ?'
                         ' WHERE id_материала = ?',
                         (материал,  id))
            conn.commit()
            conn.close()
            return redirect(url_for('allmaterial'))

    return render_template('edit_mr.html', post=post)

@app.route('/allmaterial/<int:id>/delete', methods=('POST',))
def delete_mr(id):
    post = get_post(id, 'SELECT * FROM материал_ткани WHERE id_материала = ?')
    conn = get_db_connection()
    conn.execute('DELETE FROM материал_ткани WHERE id_материала = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['материал']))
    return redirect(url_for('allmaterial'))

@app.route('/allproducer/<int:id>/edit', methods=('GET', 'POST'))
def edit_pr(id):
    post = get_post(id, 'SELECT * FROM производитель WHERE id_производителя = ?')

    if request.method == 'POST':
        страна_производитель = request.form['страна_производитель']

        if not страна_производитель:
            flash('страна_производитель is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE производитель SET страна_производитель = ?'
                         ' WHERE id_производителя = ?',
                         (страна_производитель,  id))
            conn.commit()
            conn.close()
            return redirect(url_for('allproducer'))

    return render_template('edit.html', post=post)

@app.route('/allproducer/<int:id>/delete', methods=('POST',))
def delete_pr(id):
    post = get_post(id, 'SELECT * FROM производитель WHERE id_производителя = ?')
    conn = get_db_connection()
    conn.execute('DELETE FROM производитель WHERE id_производителя = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['страна_производитель']))
    return redirect(url_for('allproducer'))





@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/create_all')
def create_all():

    return render_template('create_all.html')
'''
@app.route('/create', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()
    cur = conn.cursor()
    option = cur.execute('SELECT * FROM producer ').fetchall()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        producer = request.form.get('producer_country')

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            a = cur.execute('SELECT id FROM producer WHERE producer_country LIKE ?  ', (producer, )).fetchall()[0][0]
            conn.execute('INSERT INTO posts (title, content,producer_id) VALUES (?, ?, ?)',
                         (title, content, a))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html', option=option)
 '''



@app.route('/create_cloth', methods=('GET', 'POST'))
def create_cloth():
    conn = get_db_connection()
    cur = conn.cursor()
    prod = cur.execute('SELECT * FROM производитель ').fetchall()
    disc = cur.execute('SELECT * FROM скидка ').fetchall()
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        colour = request.form['colour']
        purpose = request.form['purpose']
        type = request.form['type']
        width = request.form['width']
        photo = request.form['photo']
        producer = request.form.get('producer')
        discount = request.form.get('discount')
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            a = cur.execute('SELECT id_производителя FROM производитель WHERE страна_производитель LIKE ?  ', (producer, )).fetchall()[0][0]
            b = cur.execute('SELECT id_скидки FROM скидка WHERE название LIKE ?  ', (discount, )).fetchall()[0][0]
            conn.execute('INSERT INTO ткань (название, цена_за_метр, цвет, назначение, тип_ткани,ширина_ткани, фото_ткани, id_производителя, id_скидки) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         (title, price, colour, purpose, type, width, photo, a, b))
            conn.commit()
            conn.close()
            return redirect(url_for('create_cloth'))

    return render_template('create_cloth.html', prod=prod, disc=disc )

@app.route('/create_composition', methods=('GET', 'POST'))
def create_composition():
    conn = get_db_connection()
    cur = conn.cursor()
    mater = cur.execute('SELECT * FROM материал_ткани ').fetchall()
    clot = cur.execute('SELECT * FROM ткань ').fetchall()
    if request.method == 'POST':
        percentage = request.form['percentage']
        material = request.form.get('material')
        cloth = request.form.get('cloth')
        if not percentage:
            flash('percentage is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            a = cur.execute('SELECT id_материала FROM материал_ткани WHERE материал LIKE ?  ', (material, )).fetchall()[0][0]
            b = cur.execute('SELECT id_ткани FROM ткань WHERE название LIKE ?  ', (cloth, )).fetchall()[0][0]
            conn.execute('INSERT INTO состав_ткани (процентное_содержание, id_материала, id_ткани) VALUES (?, ?, ?)',
                         (percentage, a, b))
            conn.commit()
            conn.close()
            return redirect(url_for('create_composition'))

    return render_template('create_composition.html', mater=mater, clot=clot)


@app.route('/create_producer', methods=('GET', 'POST'))
def create_producer():
    if request.method == 'POST':
        prod = request.form['prod']
        if not prod:
            flash('производитель не введен!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            conn.execute('INSERT INTO производитель (страна_производитель) VALUES (?)',
                         (prod,))
            conn.commit()
            conn.close()
            return redirect(url_for('create_producer'))

    return render_template('create_producer.html')

@app.route('/create_material', methods=('GET', 'POST'))
def create_material():
    if request.method == 'POST':
        material = request.form['material']
        if not material:
            flash('материал ткани не введен!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            conn.execute('INSERT INTO материал_ткани (материал) VALUES (?)',
                         (material,))
            conn.commit()
            conn.close()
            return redirect(url_for('create_material'))

    return render_template('create_material.html')

@app.route('/create_discount', methods=('GET', 'POST'))
def create_discount():
    if request.method == 'POST':
        title = request.form['title']
        value = request.form['value']
        start = request.form['start']
        finish = request.form['finish']
        if not title:
            flash('название не введено!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            conn.execute('INSERT INTO скидка (название,величина_скидки,дата_начала_скидки,дата_конца_скидки) VALUES (?,?,?,?)',
                         (title, value, start, finish))
            conn.commit()
            conn.close()
            return redirect(url_for('create_discount'))

    return render_template('create_discount.html')

######################################учетные записи##################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM accounts WHERE username LIKE ?  AND password LIKE ?', (username, password,))

        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('create_all.html', msg=msg)
        else:
            msg = 'Некорректный логин / пароль !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM accounts WHERE username LIKE ?  AND password LIKE ?', (username, password,))

        account = cur.fetchall() #fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            conn.execute('INSERT INTO accounts VALUES (NULL, ?, ?, ?)', (username, password, email,))
            conn.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

















if __name__ == "__main__":
    app.run(debug=True)  # add debug mode