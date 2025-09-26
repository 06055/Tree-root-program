from flask import Flask,render_template,request,jsonify

import mysql.connector



"""
1.Страница выбора древа
2.Добавление древа 
3.Вход в древо 
4.Добавление 1 связи

"""

"""
1.При нажатии на круг(названием) то выскакивает окно с выбором 
--1.Выбор удалить
--2.Выбор изменить
--3.Добавить описание
--4.Добавить связя с этим кругом(названием)
"""




"""
Исправить ошибку с добавлением
добавить возможность добавления кружочка(со связей)

"""


app = Flask(__name__)


@app.route('/')
def main_fux():


    return render_template("window_main.html")


@app.route('/registering_show')
def registering_show():

    return render_template('window_register.html')


@app.route('/registering', methods = ['POST'])
def registering():
    dbconfig = {'host':'127.0.0.1','user':'Vitaly','password':'newpassword','db':'Project_Tree_Root'}
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()

    user_name = request.form["user_name"]
    user_password = request.form["user_password"]
    message_for_password_and_user_name = 'Successfully registered'

    if user_name != '' and user_password != '' :
        if len(user_name) < 4 or len(user_password) < 5:
            message_for_password_and_user_name = 'Name or password is too short'

        _SQL = """SELECT user_name FROM table_for_logi WHERE user_name = %s """
        cursor.execute(_SQL,(user_name,))
        result = cursor.fetchone()



        if result:
            message_for_password_and_user_name = 'The name is already taken'


        else:

            _SQL = """INSERT INTO table_for_logi(user_name,password) VALUES(%s,Sha1(%s))"""
            cursor.execute(_SQL,(user_name,user_password,))
            dbc.commit()

    return render_template('window_main.html',message_for_password_and_user_name = message_for_password_and_user_name)


@app.route('/logining_show')
def logining_show():

    return render_template('window_logining.html')


@app.route('/logining', methods = ['POST'])
def logining():
    threes_list = list()

    user_name = request.form["user_name"]
    user_password = request.form["user_password"]

    if user_name != '' and user_password != '' :
        dbconfig = {'host':'127.0.0.1','user':'Vitaly','password':'newpassword','db':'Project_Tree_Root'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """SELECT id FROM table_for_logi WHERE user_name = %s AND password = Sha1(%s) """
        cursor.execute(_SQL,(user_name,user_password))
        get_id_user = cursor.fetchone()

    if get_id_user:
        _SQL = """SELECT * FROM table_threes WHERE user_id = %s"""
        cursor.execute(_SQL,(get_id_user))
        threes_from_cursor = cursor.fetchall()
        for i in threes_from_cursor:
            threes_list.append(i)
    else:
        return render_template('window_logining.html',message_error = 'Name or password is incorrect' )
    return render_template('main_page_root.html', get_id_user = get_id_user, threes_list = threes_list)


@app.route('/main_page_add', methods=['POST', 'GET'])
def main_page():
    threes_list = []

    get_threesName = request.form.get('threesName', '')
    get_hidden_id_user = request.form.get('hidden_id_user', '')

    if get_hidden_id_user and get_threesName:
        dbconfig = {
            'host': '127.0.0.1',
            'user': 'Vitaly',
            'password': 'newpassword',
            'db': 'Project_Tree_Root'
        }
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()


        _CHECK_SQL = """SELECT * FROM table_threes WHERE name=%s AND user_id=%s"""
        cursor.execute(_CHECK_SQL, (get_threesName, get_hidden_id_user,))
        copy_name = cursor.fetchone()

        if not copy_name:
            _SQL = """INSERT INTO table_threes(name, user_id) VALUES(%s, %s)"""
            cursor.execute(_SQL, (get_threesName, get_hidden_id_user,))
            dbc.commit()

        get_threesName = ''

        cursor.close()
        dbc.close()


    if get_hidden_id_user:
        dbconfig = {
            'host': '127.0.0.1',
            'user': 'Vitaly',
            'password': 'newpassword',
            'db': 'Project_Tree_Root'
        }
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """SELECT * FROM table_threes WHERE user_id=%s"""
        cursor.execute(_SQL, (get_hidden_id_user,))
        threes_from_cursor = cursor.fetchall()
        threes_list.extend(threes_from_cursor)
        cursor.close()
        dbc.close()

    return render_template('main_page_root.html', get_id_user=get_hidden_id_user, threes_list=threes_list)



dbconfig = {'host':'127.0.0.1','user':'Vitaly','password':'newpassword','db':'Project_Tree_Root'}

@app.route('/three_in_show')
def three_in_show():
    three_id = request.args.get('three_id')
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor(dictionary=True)  
    _SQL = """SELECT id, name, back_core_id, three_id FROM table_connection_cores WHERE three_id = %s"""
    cursor.execute(_SQL, (three_id,))
    cores = cursor.fetchall()
    cursor.close()
    dbc.close()

    return render_template("window_three_in.html", three_id=three_id, cores_json=cores)


@app.route('/three_in_add', methods=['POST'])
def three_in_add():
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()


    get_name_core = request.form.get('threesName', '').strip()
    get_three_id = request.form.get("three_id", "").strip()

    if not get_name_core:
        return jsonify({'success': False, 'message': 'Name is empty'})

    if not get_three_id:
        return jsonify({'success': False, 'message': 'Tree ID is missing'})


    cursor.execute(
        """SELECT * FROM table_connection_cores WHERE three_id = %s AND back_core_id = 0""",
        (get_three_id,)
    )
    result = cursor.fetchone()

    if result:
        cursor.close()
        dbc.close()
        return jsonify({'success': False, 'message': 'This tree already has a root core'})

    cursor.execute(
        """INSERT INTO table_connection_cores (name, back_core_id, three_id) VALUES (%s, %s, %s)""",
        (get_name_core, 0, get_three_id)
    )
    dbc.commit()


    cursor.execute("""SELECT name FROM table_connection_cores WHERE three_id = %s""", (get_three_id,))
    cores = cursor.fetchall()
    cores_names = [str(core[0]) for core in cores] 

    cursor.close()
    dbc.close()

    return jsonify({'success': True, 'message': 'Root core created', 'cores': cores_names})



@app.route('/three_in_add_new_connect', methods=["POST"])
def three_in_add_new_connect():
    three_id = request.args.get('three_id')
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()

    
    get_three_id = request.form.get("three_id")
    new_connected_core = request.form.get("new_connected_core")
    selected_core = request.form.get("thecores")  

    _SQL = """SELECT name FROM table_connection_cores WHERE three_id = %s"""
    cursor.execute(_SQL, (get_three_id,))
    cores = cursor.fetchall()  
    cores_names = [core[0] for core in cores]


    _SQL = """SELECT id from table_connection_cores WHERE name = %s and three_id = %s"""
    cursor.execute(_SQL,(selected_core,get_three_id,))
    back_core_id = cursor.fetchone()
    back_core_id = back_core_id[0]
    
    _SQL = """INSERT INTO table_connection_cores(name,back_core_id,three_id) VALUES(%s,%s,%s) """
    cursor.execute(_SQL,(new_connected_core,back_core_id,get_three_id,))
    dbc.commit()

    cursor.close()
    dbc.close()

    print("three_id:", get_three_id)
    print("new_connected_core:", new_connected_core)
    print("selected_core:", selected_core)  

    return render_template("window_three_in.html", three_id=get_three_id, cores = cores_names)




if __name__ == "__main__":
    app.run(debug=True)




"""/
Проблема с добавлением(Добавляет но с ошибкой)

"""