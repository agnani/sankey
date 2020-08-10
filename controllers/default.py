# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
from cryptography.fernet import Fernet


def index():
    msg = "out if"
    search = ""
    text = ""
    cars = [{'car': 'Ford', 'year': 2005},
            {'car': 'Mitsubishi', 'year': 2000},
            {'car': 'BMW', 'year': 2019},
            {'car': 'VW', 'year': 2011}]
    test2 = cars[1]
    test1 = test2.get("car")
    if request.post_vars:
        search = request.post_vars.search
        msg = "in index"
        text = test(search)

    rows = db(db.sankeyEmployee).select(orderby=db.sankeyEmployee.id)
    databas = db(db.sankeyUpload).select(orderby=db.sankeyUpload.id)
    test55 = db(db.test).select(orderby=db.test.id)
    max = db.sankeyUpload.id.max()
    out = db(db.sankeyUpload).select(max).first()[max]
    row = rows[0]
    man = 1
    data = 'Narayan&1'
    data1 = crypt(data)
    data2 = dcrypt(data1)
    a = db(db.sankeyEmployee.id == 3).select().first()
    a.update_record(softDelete=False)
    row1 = db.sankeyEmployee(db.sankeyEmployee.id == 1)
    id = 4
    data = db.sankeyUpload(db.sankeyUpload.id == 2)
    return locals()


def crypt(data):
    """
        Encrypts a message
    """
    key = load_key()
    encoded_data = data.encode()
    f = Fernet(key)
    encrypted_data = f.encrypt(encoded_data)
    return encrypted_data


def dcrypt(data):
    """
        Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(data)
    decrypted_decoded_data = decrypted_data.decode()
    return decrypted_decoded_data


def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()


def test(search):
    if search == "manish":
        msg = "yes"
    else:
        msg = "no"
    return msg


def login():
    user = ""
    pas = ""
    msg = ""
    pas1 = ""
    if request.post_vars:
        user = request.post_vars.usr
        pas = request.post_vars.pas
        row = db.sankeyEmployee(db.sankeyEmployee.email == user)
        if row:
            pas1 = row.password
            pas1 = pas1.encode()
            pas1 = dcrypt(pas1)
            if pas1 == pas:
                msg = "Login successful"
                session.email = row.email
                session.role = row.role
                session.name = row.name
                session.id = row.id
                session.index = "sankeyEmployee.id"
                redirect(URL('home'))
            else:
                msg = "Wrong Password"
        else:
            msg = "User not registered"
    return locals()


def home():
    verify()
    s_role = session.role
    s_name = session.name
    s_email = session.email
    s_id = session.id
    if s_role == 'User':
        redirect(URL('employee', args=(s_id)))
    pass

    size = 5
    count = db(db.sankeyEmployee.softDelete == False).count()
    max = count/size
    index = session.index
    
    if not request.vars.page:
        redirect(URL(vars={'page': 1}))
    else:
        page = int(request.vars.page)
    pass
    start = (page - 1) * size
    end = page * size
    user = s_name
    msg = db(db.sankeyEmployee.softDelete == False).select(orderby=index, limitby=(start, end))
    return locals()


def searching():
    verify()
    if request.post_vars:
        search = request.post_vars.search
        msg = db.executesql("SELECT * FROM sankeyEmployee WHERE email LIKE '%" + search + "%' ;")
        #msg = db(db.sankeyEmployee.email == search).select()
    pass
    return locals()


def sorting():

    index = request.args(0)  # Which column to sort
    attribute = request.args(1)  # In ascending or descending

    if index is None:
        index = 'sankeyEmployee.id'
        attribute = 0
    else:
        index = request.args(0)  # Which column to sort
        index = "sankeyEmployee." + index
        attribute = int(request.args(1))  # In ascending or descending
    pass

    if attribute == 1:
        index = index + " DESC"
    pass

    session.index = index
    redirect(URL('home'))
    return locals()


def employee():
    verify()
    s_role = session.role
    s_id = session.id
    i = int(request.args(0))
    msg = db.sankeyEmployee(db.sankeyEmployee.id == i)
    return locals()


def insert():
    verify()
    form = SQLFORM(db.sankeyEmployee).process()
    if form.accepted:
        max = db.sankeyEmployee.id.max()
        id = db(db.sankeyEmployee).select(max).first()[max]
        id = id - 1
        encrypt_all(id)
        redirect(URL('home'))
    pass
    return locals()


def view():
    s_role = session.role
    s_id = session.id
    msg = db.sankeyEmployee(db.sankeyEmployee.id == s_id)
    return locals()


def verify():
    s_email = session.email
    if s_email is None:
        redirect(URL('login'))
    else:
        verify1()
    pass
    return locals()


def verify1():
    s_role = session.role
    if s_role == 'User':
        redirect(URL('view'))
    pass
    return locals()


def upload():
    verify()
    import pandas as pd

    name = ""
    form = SQLFORM(db.sankeyUpload).process()
    if form.accepted:
        redirect(URL('download'))
        session.flash = "New record inserted"

    # read_file = pd.read_excel(r'E:\web2py_src\web2py\applications\Sankey\test.xlsx')
    # read_file.to_csv(r'E:\web2py_src\web2py\applications\Sankey\file.csv', index=None, header=True)
    return locals()


def download():
    verify()
    import pandas as pd

    max = db.sankeyUpload.id.max()
    id = db(db.sankeyUpload).select(max).first()[max]
    row = db.sankeyUpload(db.sankeyUpload.id == id)
    read_file = pd.read_excel(r'E:\web2py_src\web2py\applications\Sankey\uploads/' + row.folder)
    read_file.to_csv(r'E:\web2py_src\web2py\file1.csv', index=None, header=True)

    max = db.sankeyEmployee.id.max()
    id = db(db.sankeyEmployee).select(max).first()[max]

    db.sankeyEmployee.import_from_csv_file(open('file1.csv', 'r', encoding='utf-8', newline=''))

    encrypt_all(id)
    redirect(URL('home'))
    return locals()


def encrypt_all(id):
    data = db(db.sankeyEmployee.id > id).select()
    for row in data:
        text = row.password
        encrypted_text = crypt(text)
        row.update_record(password=encrypted_text)
    pass
    return locals()


def logout():
    session.email = None
    session.role = None
    session.name = None
    session.index = None
    redirect(URL('login'))
    return locals()


def update():
    import datetime

    verify()
    now = datetime.datetime.now()
    s_name = session.name
    s_role = session.role
    i = int(request.args(0))
    msg = db.sankeyEmployee(db.sankeyEmployee.id == i)
    if request.post_vars:
        name = request.post_vars.name
        surname = request.post_vars.surname
        email = request.post_vars.email
        date = request.post_vars.date
        role = request.post_vars.role
        gender = request.post_vars.gender
        salary = request.post_vars.salary
        a = db(db.sankeyEmployee.id == i).select().first()
        a.update_record(name=name)
        a.update_record(surname=surname)
        a.update_record(email=email)
        a.update_record(joining=date)
        a.update_record(salary=salary)
        a.update_record(role=role)
        a.update_record(gender=gender)
        a.update_record(ModifiedBY=s_name)
        a.update_record(ModificationTime=now)
        redirect(URL('employee', args=(i)))
    pass
    return locals()


def delete():
    id = request.args(0)
    a = db(db.sankeyEmployee.id == id).select().first()
    a.update_record(softDelete=True)
    redirect(URL('home'))
    return locals()
