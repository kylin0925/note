import sqlalchemy
import hashlib
import time
def init(db_name):
    eng = sqlalchemy.create_engine('sqlite:///' + db_name,echo=False)
    metadata = sqlalchemy.MetaData()
    codetbl = sqlalchemy.Table(
        'codetbl',
        metadata,
        sqlalchemy.Column('code_no',sqlalchemy.Integer,primary_key=True),
        sqlalchemy.Column('title',sqlalchemy.String),
        sqlalchemy.Column('code',sqlalchemy.String),
        sqlalchemy.Column('date',sqlalchemy.String))

    taglist = sqlalchemy.Table(
        'taglist',
        metadata,
        sqlalchemy.Column('no',sqlalchemy.Integer,primary_key=True),
        sqlalchemy.Column('tag',sqlalchemy.String),
        sqlalchemy.Column('code_no',sqlalchemy.Integer),
        )
    metadata.create_all(eng)
    return eng,codetbl,taglist

def max_code_no(tab):
    s = sqlalchemy.sql.select([sqlalchemy.func.max(tab.c.code_no)])

    conn = eng.connect()
    r = conn.execute(s)
    c = r.fetchone()
    if c[0] == None:
        return 0
    else:
        print "count ",c[0]
        return c[0]
def add(eng,tab,tagtbl,title,code,taglist):
    code_no = max_code_no(tab) + 1
    date = time.strftime("%Y-%m-%d %H:%M:%S")
    ins = tab.insert().values(title=title,code=code,date=date)
    ins.compile().params
    conn = eng.connect()
    r = conn.execute(ins)

    ins = tagtbl.insert()
    for tag in taglist:
        print 'add tag ',tag
        _ins=ins.values(tag=tag,code_no=code_no)
        _ins.compile().params
        r = conn.execute(_ins)

def modify(eng,tab,tagtbl,code_no,title,code,taglist):

    conn = eng.connect()
    stmt = tab.update().where(tab.c.code_no == code_no).values(title=title,code=code)
    r = conn.execute(stmt)

#    ins = tagtbl.insert()
#    for tag in taglist:
#        print 'add tag ',tag
#        _ins=ins.values(tag=tag,code_no=code_no)
#        _ins.compile().params
#        r = conn.execute(_ins)


def list_note(tab):
    s = sqlalchemy.sql.select([tab])

    conn = eng.connect()
    r = conn.execute(s)
    print '..'
    for row in r:
        print row[0],row[1],row[3]

def list_tag(tab):
    s = sqlalchemy.sql.select([tab])

    conn = eng.connect()
    r = conn.execute(s)
    print '..'
    tag_list = {} # tag tag_count
    for row in r:
        if tag_list.has_key(row['tag']) == True:
            tag_list[row['tag']]+=1
        else:
            tag_list[row['tag']]=1
        #print row['no'],row['tag']

    for t in tag_list:
        print t,tag_list[t]
def list_one_note(tab,tagtbl,code_no):
    s = sqlalchemy.sql.select([tab]).where(tab.c.code_no==code_no)

    conn = eng.connect()
    r = conn.execute(s)
    row = r.fetchone()
    print row[0]
    print row[1]
    print row[2]
    print row[3]

    s = sqlalchemy.sql.select([tagtbl]).where(tagtbl.c.code_no==code_no)
    conn = eng.connect()
    r = conn.execute(s)
    print "Tags: "
    for row in r:
        print row[1]

    print '..'

def delete_note(eng,codetbl,tagtbl,code_no):

    conn = eng.connect()
    r = conn.execute(codetbl.delete().where(codetbl.c.code_no == code_no))
    r = conn.execute(tagtbl.delete().where(tagtbl.c.code_no == code_no))

def query(tab):
    s = sqlalchemy.sql.select([tab])

    conn = eng.connect()
    r = conn.execute(s)
    for row in r:
        print row

def new_note():
    title = raw_input("title :")
    content = raw_input("content :")
    tag_list = []
    while True:
        tag = raw_input("tag(type q to end):")
        if tag == 'q':
            break
        tag_list.append(tag)

    return title,content,tag_list

eng,codetbl,tagtbl = init("foo.db")

while True:
    print "1. new note"
    print "2. list note"
    print "3. list tag"
    print "4. modify"
    print "5. delete"
    print "q to quit"
    ch = raw_input(":")
    if ch == '1':
        title,content,tag_list = new_note()
        print title,content,tag_list
        #add(eng,codetbl,taglist,"123",'test',['1','2'])
        add(eng,codetbl,tagtbl,title,content,tag_list)
    elif ch == '2':

        #query(codetbl)
        #query(taglist)
        list_note(codetbl)
        ch = raw_input('choose :')
        try:
            ich = int(ch)
            list_one_note(codetbl,tagtbl,ich)
        except:
            print 'choice error'
    elif ch == '3':
        list_tag(tagtbl)
    elif ch == '4':
        list_note(codetbl)
        ch = raw_input('choose :')
        ich = int(ch)
        try:
            ich = int(ch)
        except:
            print 'delete choice error'
        #modify input        
        title,content,tag_list = new_note()

        modify(eng,codetbl,tagtbl,ich,title,content,tag_list)

    elif ch == '5':
        list_note(codetbl)
        ch = raw_input('choose :')
        ich = int(ch)
        try:
            ich = int(ch)
        except:
            print 'delete choice error'

        delete_note(eng,codetbl,tagtbl,ich)
    elif ch == 'q':
        break
