import sqlalchemy
import hashlib
import time
class note:
    eng = None
    codetbl = None
    taglist = None
    def init(self,db_name):
        self.eng = sqlalchemy.create_engine('sqlite:///' + db_name,echo=False)
        metadata = sqlalchemy.MetaData()
        self.codetbl = sqlalchemy.Table(
            'codetbl',
            metadata,
            sqlalchemy.Column('code_no',sqlalchemy.Integer,primary_key=True),
            sqlalchemy.Column('title',sqlalchemy.String),
            sqlalchemy.Column('code',sqlalchemy.String),
            sqlalchemy.Column('date',sqlalchemy.String))

        self.taglist = sqlalchemy.Table(
            'taglist',
            metadata,
            sqlalchemy.Column('no',sqlalchemy.Integer,primary_key=True),
            sqlalchemy.Column('tag',sqlalchemy.String),
            sqlalchemy.Column('code_no',sqlalchemy.Integer),
            )
        metadata.create_all(self.eng)
        #return eng,codetbl,taglist

    def max_code_no(self):
        s = sqlalchemy.sql.select([sqlalchemy.func.max(self.codetbl.c.code_no)])

        conn = self.eng.connect()
        r = conn.execute(s)
        c = r.fetchone()
        if c[0] == None:
            return 0
        else:
            print "count ",c[0]
            return c[0]

    def add(self,title,code,taglist):
        code_no = self.max_code_no() + 1
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        ins = self.codetbl.insert().values(title=title,code=code,date=date)
        ins.compile().params
        conn = self.eng.connect()
        r = conn.execute(ins)
        self.add_tag_list(taglist,code_no)

    def add_tag_list(self,taglist,code_no):
        ins = self.taglist.insert()
        conn = self.eng.connect()
        for tag in taglist:
            print 'add tag ',tag
            _ins=ins.values(tag=tag,code_no=code_no)
            _ins.compile().params
            r = conn.execute(_ins)
# not test
    def modify(self,eng,tab,tagtbl,code_no,title,code,taglist):

        conn = eng.connect()
        stmt = tab.update().where(tab.c.code_no == code_no).values(title=title,code=code)
        r = conn.execute(stmt)

#    ins = tagtbl.insert()
#    for tag in taglist:
#        print 'add tag ',tag
#        _ins=ins.values(tag=tag,code_no=code_no)
#        _ins.compile().params
#        r = conn.execute(_ins)


    def list_note(self):
        s = sqlalchemy.sql.select([self.codetbl])

        conn = self.eng.connect()
        r = conn.execute(s)
        print '..'
        for row in r:
            print row[0],row[1],row[3]

    def list_tag(self):
        s = sqlalchemy.sql.select([self.taglist])

        conn = self.eng.connect()
        r = conn.execute(s)
        tag_list = {} # tag tag_count
        for row in r:
            if tag_list.has_key(row['tag']) == True:
                tag_list[row['tag']]+=1
            else:
                tag_list[row['tag']]=1

        for t in tag_list:
            print t,tag_list[t]

    def list_one_note(self,code_no):
        s = sqlalchemy.sql.select([self.codetbl]).where(self.codetbl.c.code_no==code_no)

        conn = self.eng.connect()
        r = conn.execute(s)
        row = r.fetchone()
        print 'title :',row["title"]
        print 'code :',row['code']
        print 'date :',row['date']
        #print row[3]
        self.list_tag_by_code_no(code_no)

    def list_tag_by_code_no(self,code_no):
        s = sqlalchemy.sql.select([self.taglist]).where(self.taglist.c.code_no==code_no)
        conn = self.eng.connect()
        r = conn.execute(s)
        print 'tags :'
        for row in r:
            print "\t",row[1]

    def delete_note(self,code_no):
        conn = self.eng.connect()
        r = conn.execute(self.codetbl.delete().where(self.codetbl.c.code_no == code_no))

    def delete_tag_by_code_no(self,code_no):
        conn = self.eng.connect()
        r = conn.execute(self.taglist.delete().where(self.taglist.c.code_no == code_no))

#def query(tab):
#    s = sqlalchemy.sql.select([tab])
#
#    conn = eng.connect()
#    r = conn.execute(s)
#    for row in r:
#        print row

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

#eng,codetbl,tagtbl = init("foo.db")
note_db = note()
note_db.init('note.db')
#note_db.add('test','123',[1,2])
#print 'list'
#note_db.list_note()
#print 'list tag'
#note_db.list_tag()
#note_db.list_one_note(2)
#note_db.delete_note(2)
#note_db.delete_tag_by_code_no(3)
#print 'aftert delete'
#note_db.list_note()
#note_db.list_tag()
while True:
    print "1. new note"
    print "2. list note"
    print "3. list tag"
#    print "4. modify"
#    print "5. delete"
    print "q to quit"
    ch = raw_input(":")
    if ch == '1':
        title,content,tag_list = new_note()
        print title,content,tag_list
        #add(eng,codetbl,taglist,"123",'test',['1','2'])
        note_db.add(title,content,tag_list)
    elif ch == '2':

        #query(codetbl)
        #query(taglist)
        note_db.list_note()
        ch = raw_input('choose :')
        try:
            ich = int(ch)
            note_db.list_one_note(ich)
        except:
            print 'choice error'
        print "modify "
        print "modify tag"
        tag_ch = raw_input()
        
    elif ch == '3':
        list_tag(tagtbl)
#    elif ch == '4':
#        list_note(codetbl)
#        ch = raw_input('choose :')
#        ich = int(ch)
#        try:
#            ich = int(ch)
#        except:
#            print 'delete choice error'
#        #modify input        
#        title,content,tag_list = new_note()
#
#        modify(eng,codetbl,tagtbl,ich,title,content,tag_list)
#
#    elif ch == '5':
#        list_note(codetbl)
#        ch = raw_input('choose :')
#        ich = int(ch)
#        try:
#            ich = int(ch)
#        except:
#            print 'delete choice error'
#
#        delete_note(eng,codetbl,tagtbl,ich)
    elif ch == 'q':
        break
