from flask import Blueprint, render_template, request, flash,redirect,url_for,session,send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
import glob

view = Blueprint('view',__name__)

@view.route('/')
def home():
    session['check_arr'] = []
    session['df_arr'] = []
    session['answer_arr'] = []
    session['base'] = []
    files2 = glob.glob('web/temp/*')
    for f2 in files2:
        os.remove(f2)
    files3 = glob.glob('web/basefile/*')
    for f3 in files3:
        os.remove(f3)
    files4 = glob.glob('web/checkfile/*')
    for f4 in files4:
        os.remove(f4)
    return render_template('home.html')

@view.route('/columnselector', methods=['POST','GET'])
def columnselector():
    if request.method == 'POST':
        base_file = request.files["basefile"]
        basepath = os.path.dirname(__file__)
        base_file_path = os.path.join(basepath, "basefile", secure_filename(base_file.filename))
        base_file.save(base_file_path)
        session['base_file_path'] = base_file_path
        df = pd.read_excel(session['base_file_path'])
        return render_template('basefilewanted.html', data=df.columns)
    else:
        return redirect(url_for('view.home'))


@view.route('/check', methods=['POST','GET'])
def check():
    if request.method== 'POST':
        df = pd.read_excel(session['base_file_path'])
        column = request.form.getlist('column')
        session['added_arr'] = column
        base = []
        for items in df['{}'.format(session['added_arr'][0])]:
                try:
                    math.floor(int(items))
                except:
                    pass
                base.append(items)
        for elements in session['added_arr'][1:]:
                for no, things in enumerate(df['{}'.format(elements)]):
                    try:
                        things = math.floor(int(things))
                    except:
                        pass
                    try:
                        things = things.replace('nan', '')
                    except:
                        pass
                    base[no] = str(base[no])+ ' ' +str(things)
        session['base'] = base    
        return render_template('check.html')
    else:
        return redirect(url_for('view.home'))


@view.route('/finder',methods=['POST','GET'])
def finder():
    if request.method == 'POST':
        answer_arr = session['answer_arr']
        check_file = request.files["checkfile"]
        checkpath = os.path.dirname(__file__)
        check_file_path = os.path.join(checkpath, "checkfile", secure_filename(check_file.filename))
        check_file.save(check_file_path)
        checking = open(check_file_path,'r')
        check_arr = []
        for things in open(check_file_path).readlines():
            things = things.replace(' ', '').lower()
            things = things.replace('locked', '')
            things = things.replace('\n', '')
            if len(things) <= 2:
                pass
            else:
                check_arr.append(things)
        session['check_arr'] = check_arr
        base = session['base']
        df_arr = []
        for aw in base:
            aw = aw.replace(' ', '')
            df_arr.append(aw.lower())
    

        for no, elements in enumerate(df_arr):
            if elements in check_arr:
                pass
            else:
                answer_arr.append(base[no])
        wi = open('web/temp/attendance.txt', 'a')
        for elemen in answer_arr:
            wi.write(elemen)
            wi.write('\n')
        wi.write('\n')
        wi.write('\n')
        wi.write('Number of students on roll: {}'.format(len(base)))
        wi.write('\n')
        wi.write('Number of students present: {}'.format(len(base)-len(answer_arr)))        
        wi.write('\n')
        wi.write('Number of students absent: {}'.format(len(answer_arr)))
        wi.close()
        answer_arr.append('Number of students on roll: {}'.format(len(base)))
        answer_arr.append('Number of students present: {}'.format(len(base)-len(answer_arr)))
        answer_arr.append('Number of students absent: {}'.format(len(answer_arr)))
        
        files = glob.glob('web/basefile/*')
        for f in files:
            os.remove(f)
        files2 = glob.glob('web/checkfile/*')
        for f2 in files2:
            os.remove(f2)
        return redirect(url_for('view.answer', filename='attendance.txt'))
    else:
        return redirect(url_for('view.home'))

@view.route('/return-files/<filename>')
def return_files_tut(filename):
    basepath = os.path.dirname(__file__)
    file_path = basepath + '/temp/' +filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

@view.route('/answer/<filename>')
def answer(filename):
    asd = []
    filse = open('web/temp/attendance.txt', 'r')
    for i in filse:
        asd.append(i)
    return render_template('answer.html',value=filename, aray=asd)

@view.route('/more')
def more():
    return render_template('more.html')
