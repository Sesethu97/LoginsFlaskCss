from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("table.db")
con.execute("CREATE TABLE if not exists customer(pid integer primary key,name text,address text,contact integer,email text,password text)")
con.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("table.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from customer where name=? and email=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["password"]=data["password"]
            return redirect("customer")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("index"))


@app.route('/customer',methods=["GET","POST"])
def customer():
    return render_template("customer.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            email=request.form['email']
            password=request.form['password']
        
            con=sqlite3.connect("table.db")
            cur=con.cursor()
            
            cur.execute("insert into customer(name,address,contact,email,password)values(?,?,?,?,?)",(name,address,contact,email,password))
            con.commit()
            
            flash("Sign_up Successful","success")
        except:
            flash("Sign_up Unsuccessful","danger")
        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)