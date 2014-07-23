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
        _ins=ins.values(tag=tag,code_no=code_no)
        _ins.compile().params
        r = conn.execute(_ins)

def list_note(tab):
    s = sqlalchemy.sql.select([tab])

    conn = eng.connect()
    r = conn.execute(s)
    for row in r:
        print row[0],row[1]


def query(tab):
    s = sqlalchemy.sql.select([tab])

    conn = eng.connect()
    r = conn.execute(s)
    for row in r:
        print row

eng,codetbl,taglist = init("foo.db")

add(eng,codetbl,taglist,"123",'test',['1','2'])

query(codetbl)
query(taglist)
list_note(codetbl)
