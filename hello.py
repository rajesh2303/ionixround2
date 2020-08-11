'''i have already created database in mysql 3 table coustomers=> for bus angent=>for customers login show1=>for booked storage database name as db name'''

from flask import *
import random
import mysql.connector
con=mysql.connector.connect(user='root',password='',host='localhost',database='dbname')
cur=con.cursor()
app=Flask(__name__)
@app.route('/',methods=['POST','GET'])
def signup():
    return render_template('firstpage.html')    #home page 1.Admin 2.Agent 3.Logout
@app.route('/vd',methods=['POST','GET'])
def vd():
    return render_template('validateaa.html',status="color:black")   # post method for validation
@app.route('/validate',methods=['POST','GET'])
def validate():
    if request.method=='POST':
        name=request.form['Id']
        passw=request.form['fp']
        print(name,passw)
        if name=="Rajesh" and passw=="1234":     # for admin default user name and password as Rajesh 1234
            return render_template("admin1.html")
        return render_template('validateaa.html',status="color:red")
@app.route('/admin',methods=['POST','GET'])
def admin():           
    return render_template('admin1.html')
@app.route('/addbusadmin',methods=['POST','GET'])
def addbusadmin():
    return render_template('addbus3.html',status="color:black")    #for Entering bus details and validate auto generate id
@app.route('/busdb',methods=['POST','GET'])
def busdb():
    if request.method=='POST':
        name=request.form['fna']
        place=request.form['fr']
        placeto=request.form['ft']
        price=request.form['fp']
        seat=request.form['fs']
        if len(name)==0 or len(place)==0 or len(placeto)==0:
            return render_template('addbus3.html',status="color:red")
        def find():
            res=[]
            for x in range(3):
                res.append(random.randint(0,100))        #auto generate id it is an unique one already exist create new one
            re=""
            for i in range(len(res)):
                re+=str(res[i])
            return re
        N=3
        while(N!=4):  #already exist id auto generate a new one
            re=find()
            cur.execute("SELECT * FROM customers WHERE id = %s", (re, ))   
            myresult = cur.fetchall()
            if len(myresult)==0:
                break
        print(name,place,placeto,price,seat,re)
        cur.execute("insert into customers values(%s,%s,%s,%s,%s,%s)",(name,place,placeto,price,seat,re))   #store in bus database
        con.commit()
        print("success")
        li=[name,place,placeto,price,seat,re]
        print(li)
        return render_template('dispaddbus.html',value=li)
@app.route('/agentbus',methods=['POST','GET'])
def agentbus():
    return render_template('agentde.html',status="color:black")   #admin con conly create an agent so agent is created using this
@app.route('/agentdef',methods=['POST','GET'])
def agentdef():
    if request.method=='POST':
        name=request.form['fna']
        mobile=request.form['fm']
        passw=request.form['fp']
        print(name,mobile,passw)
        if len(name)==0 or len(mobile)==0 or len(passw)==0:
            return render_template('agentde.html',status="color:red")
        def find():
            res=[]
            for x in range(3):
                res.append(random.randint(0,100))
            re=""
            for i in range(len(res)):
                re+=str(res[i])                       #auto generate id for agent
            return re
        N=3
        while(N!=4):
            re=find()
            cur.execute("SELECT * FROM agent WHERE id = %s", (re, ))
            myresult = cur.fetchall()
            if len(myresult)==0:
                break
        print(name,mobile,passw,re)
        cur.execute("insert into agent values(%s,%s,%s,%s)",(name,mobile,passw,re))   #storing agent details in db as agent table
        con.commit()
        print("success")
        li=[name,mobile,passw,re]
        print(li)
        return render_template('dispaddagent.html',value=li)
@app.route('/vd1',methods=['POST','GET'])
def vd1():
    return render_template('validateaa1.html',status="color:black")     #agent validation
@app.route('/validate1',methods=['POST','GET'])
def validate1():
    if request.method=='POST':
        id1=request.form['Id']
        passw=request.form['fp']
        print(id1,passw)
        if len(id1)==0 and len(passw)==0:
            return render_template('validateaa1.html',status="color:red")
        cur.execute("SELECT password,id FROM agent WHERE id = %s", (id1, ))
        myresult = cur.fetchall()
        print(myresult)
        if len(myresult)==1 and myresult[0][0]==passw and myresult[0][1]==id1:
            return render_template('menu.html',status=id1)          
            con.commit()
        return render_template('validateaa1.html',status="color:red")
@app.route('/details',methods=['POST','GET'])
def details():
    cur.execute("SELECT * FROM customers")              #displaying all bus details by agent
    myresult = cur.fetchall()
    return render_template('details.html',status=myresult,val=len(myresult))
@app.route('/ticket',methods=['POST','GET'])
def ticket():
    if request.method=='POST':                           #ticket booking by agent
        id1=request.form['fna']
        return render_template('ticket.html',status="color:black",val=id1)
@app.route('/ticketv',methods=['POST','GET'])
def ticketv():
    if request.method=='POST':
        id1=request.form['Id']
        q=request.form['fna']
        cur.execute("SELECT * FROM customers WHERE id = %s", (id1, ))
        myresult = cur.fetchall()
        if len(myresult)==0:
            return render_template('ticket.html',status="color:red",val=q)
        return render_template('ticket2.html',cl="color:black",status=myresult,val=q)      #validating correct seats
@app.route('/t2v',methods=['POST','GET'])
def t2v():
    if request.method=='POST':
        id1=request.form['fna']
        se=request.form['se']
        q=request.form['fna1']
        cur.execute("SELECT * FROM customers WHERE id = %s", (se, ))
        myresult = cur.fetchall()
        print(myresult)
        if int(id1)<=int(myresult[0][3]):
            return render_template('confirm.html',price=int(id1)*int(myresult[0][4]),val=q,status=myresult,sel=id1) #conforming booking
        return render_template('ticket2.html',cl="color:red",status=myresult,val=q)
@app.route('/update',methods=['POST','GET'])
def update():
    if request.method=='POST':
        id1=request.form['se']
        re=request.form['re']
        q=request.form['fna1']
        print("final",q)
        cur.execute("SELECT * FROM customers WHERE id = %s", (id1, ))
        myresult = cur.fetchall()
        res=abs(int(re)-int(myresult[0][3]))
        print("update",id1,re)
        cur.execute(" UPDATE customers SET seats = %s WHERE id = %s ",(res,myresult[0][5]))   #update the table from the booked
        con.commit()
        cur.execute("insert into show1 values(%s,%s,%s,%s,%s,%s)",(q,myresult[0][0],myresult[0][1],myresult[0][2],re,int(re)*int(myresult[0][4])))
        con.commit()
        return render_template('menu.html',status=q)
@app.route('/finalshow',methods=['POST','GET'])
def finalshow():
    if request.method=='POST':
        id1=request.form['fna1']                           #displaying the pairticilar agents bookong
        cur.execute("SELECT * FROM show1 WHERE id = %s", (id1, ))
        myresult = cur.fetchall()
        myresult=myresult[::-1]
        print(myresult)
        return render_template('finalshow.html',status=myresult,val=len(myresult))
if __name__=='__main__':
    app.run()




 

