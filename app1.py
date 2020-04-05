from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import yaml
from functools import wraps


app = Flask(__name__)


#configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'flask1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql=MySQL(app)
# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    return render_template('home.html')

#singup
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        password = userDetails['password']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,password,email) VALUES(%s,%s,%s)",(name, password,email))
        mysql.connection.commit()
        cur.close()

        flash('Registerd','success')
        return redirect(url_for('login'))
    return render_template('signup.html')




#Login
@app.route('/login',methods=['GET', 'POST' ])

def login():
    if request.method == 'POST' :
        #get form fields
        email = request.form['email']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()
         #get user name
        result = cur.execute("SELECT * FROM users WHERE email = %s",[email])

        if result > 0:
            # get stored hash
            data = cur.fetchone()
            password =data['password']

            #compare Passwords
            #if sha256_crypt.verify(password_candidate, password):
            if password_candidate == password:
                #passed
                session['logged_in'] = True
                #session['name'] = name

                flash('You are now logged in')
                return redirect(url_for('dash'))
            else:
                error = 'Invalid password'
                return render_template('login.html',error=error)
            cur.close()
        else:
            error = 'User name not found'
            return render_template('login.html',error=error)

    return render_template('login.html')


#logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have logged out','success')
    return redirect(url_for('login'))




#dashboard
@app.route('/dash')
@is_logged_in
def dash():
    cur=mysql.connection.cursor()
    leadcount1 = cur.execute("SELECT COUNT(name) FROM leads")
    ordercount = cur.execute("SELECT COUNT(name) FROM orders")
    contactcount = cur.execute("SELECT COUNT(name) FROM contact")
    mysql.connection.commit()
    result3 = leadcount1 + ordercount
    conrate = (ordercount / result3) * 100

    return render_template('dash.html',conrate = conrate,leadcount1 = leadcount1,ordercount = ordercount,contactcount = contactcount)






@app.route('/followuptable')
@is_logged_in
def followuptable():
      cur=mysql.connection.cursor()
      result = cur.execute("SELECT *FROM followup")
      followup = cur.fetchall()
      if result > 0:
          return render_template('followuptable.html',followup = followup)
      else:
          msg='no Entry'
          return render_template('followuptable.html',msg=msg)

      cur.close()
      return render_template('followuptable.html')






@app.route('/followupform', methods=['GET', 'POST'])
@is_logged_in
def followupform():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        c_name = userDetails['companyname']
        contact = userDetails['contact']
        date = userDetails['Date']
        time = userDetails['Time']
        f_type = userDetails['Type']
        product = userDetails['product']
        description = userDetails['description']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO followup (name,c_name,contact,date,time,f_type,product,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(name,c_name,contact,date,time,f_type,product,description))
        cur.execute("INSERT INTO followuplog (name,c_name,contact,date,time,f_type,product,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(name,c_name,contact,date,time,f_type,product,description))
        mysql.connection.commit()
        cur.close()

        flash('Registerd','success')
        return redirect(url_for('followuptable'))
    return render_template('followupform.html')








@app.route('/followupform1', methods=['GET', 'POST'])
@is_logged_in
def followupform1():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        c_name = userDetails['companyname']
        contact = userDetails['contact']
        date = userDetails['Date']
        time = userDetails['Time']
        f_type = userDetails['Type']
        product = userDetails['product']
        description = userDetails['description']

        cur=mysql.connection.cursor()
        result = cur.execute("SELECT *FROM followup where name=%s",[name])

        if result > 0:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM followup where name=%s",[name])

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO followup (name,c_name,contact,date,time,f_type,product,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(name,c_name,contact,date,time,f_type,product,description))
        cur.execute("INSERT INTO followuplog (name,c_name,contact,date,time,f_type,product,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(name,c_name,contact,date,time,f_type,product,description))
        mysql.connection.commit()
        cur.close()

        flash('Registerd','success')
        return redirect(url_for('followuptable'))
    return render_template('followupform1.html')








@app.route('/leadtable')
@is_logged_in
def leadtable():
      cur=mysql.connection.cursor()
      result = cur.execute("SELECT *FROM leads")
      leads = cur.fetchall()
      if result > 0:
          return render_template('leadtable.html',leads = leads)
      else:
          msg='no Entry'
          return render_template('leadtable.html',msg=msg)

      cur.close()
      return render_template('leadtable.html')





@app.route('/leadform', methods=['GET', 'POST'])
@is_logged_in
def leadform():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        c_name = userDetails['companyname']
        email = userDetails['email']
        phone = userDetails['phone']
        leadsource = userDetails['leadsource']
        Address = userDetails['Address']
        product = userDetails['product']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO leads(name,c_name,email,phone,leadsource,address,product) VALUES(%s,%s,%s,%s,%s,%s,%s)",(name, c_name,email,phone,leadsource,Address,product))
        cur.execute("INSERT IGNORE INTO contact(name,company_name,email,phone,source,address,product) VALUES(%s,%s,%s,%s,%s,%s,%s)",(name, c_name,email,phone,leadsource,Address,product))

        mysql.connection.commit()
        cur.close()


        flash('Registerd','success')
        return redirect(url_for('leadtable'))
    return render_template('leadform.html')





@app.route('/convert_lead/<string:name>', methods = ['GET', 'POST'])
@is_logged_in
def convert_lead(name):

    #cursor
    cur=mysql.connection.cursor()
     #app.logger.info(name)
    result = cur.execute("SELECT *FROM leads WHERE name=%s",[name])
    leads = cur.fetchone()

    name=leads['name']
    c_name=leads['c_name']
    email=leads['email']
    phone=leads['phone']
    leadsource=leads['leadsource']
    address=leads['address']
    product=leads['product']
    invoice=leads['invoice']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orders(name,company_name,email,phone,source,address,invoice) VALUES(%s,%s,%s,%s,%s,%s,%s)",(name,c_name,email,phone,leadsource,address,invoice))
    cur.execute("DELETE from leads WHERE name=%s",[name])
    mysql.connection.commit()
    cur.close()
    flash('Entry added to orders successfully','success')

    return redirect(url_for('leadtable'))
#    return render_template('edit_lead.html')





#delete fro leads
@app.route('/delete_lead/<string:id>',methods=['POST'])
@is_logged_in
def delete_lead(id):

     cur=mysql.connection.cursor()
     cur.execute("DELETE FROM leads where name=%s",[id])
     mysql.connection.commit()

     cur.close()
     flash('Entry Deleted','success')

     return redirect(url_for('leadtable'))




#for button followup
@app.route('/convert_followup/<string:name>', methods = ['GET', 'POST'])
@is_logged_in
def convert_followup(name):

    #cursor
    cur=mysql.connection.cursor()
     #app.logger.info(name)
    result = cur.execute("SELECT *FROM leads WHERE name=%s",[name])
    leads = cur.fetchone()

    name=leads['name']
    c_name=leads['c_name']
    email=leads['email']
    phone=leads['phone']
    leadsource=leads['leadsource']
    address=leads['address']
    product=leads['product']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO followup(name,c_name,contact,product) VALUES(%s,%s,%s,%s)",(name,c_name,phone,product))
    mysql.connection.commit()
    cur.close()
    flash('Entry added to followup successfully','success')

    return redirect(url_for('leadtable'))
#    return render_template('edit_student.html',form=form)









#convert from followup to orders
@app.route('/Cfollowup/<string:name>', methods = ['GET', 'POST'])
@is_logged_in
def Cfollowup(name):

    #cursor
    cur=mysql.connection.cursor()
     #app.logger.info(name)
    result = cur.execute("SELECT *FROM followup WHERE name=%s",[name])
    followup = cur.fetchone()

    name=followup['name']
    c_name=followup['c_name']
    contact=followup['contact']
    date=followup['date']
    time=followup['time']
    f_type=followup['f_type']
    product=followup['product']
    description=followup['description']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orders(name,company_name,phone) VALUES(%s,%s,%s)",(name,c_name,contact))
    cur.execute("DELETE from followup WHERE name=%s",[name])
    mysql.connection.commit()
    cur.close()
    flash('Entry added to orders successfully','success')

    return redirect(url_for('followuptable'))
#    return render_template('edit_student.html',form=form)





#delete from followup
@app.route('/delete_followup/<string:id>',methods=['POST'])
@is_logged_in
def delete_followup(id):

     cur=mysql.connection.cursor()
     cur.execute("DELETE FROM followup where name=%s",[id])
     mysql.connection.commit()

     cur.close()
     flash('Entry Deleted','success')

     return redirect(url_for('followuptable'))







#for button followup
@app.route('/convert_followup1/<string:name>', methods = ['GET', 'POST'])
@is_logged_in
def convert_followup1(name):

    #cursor
    cur=mysql.connection.cursor()
     #app.logger.info(name)
    result = cur.execute("SELECT *FROM followup WHERE name=%s",[name])
    followup = cur.fetchone()

    name=followup['name']
    c_name=followup['c_name']
    contact=followup['contact']
    date=followup['date']
    time=followup['time']
    f_type=followup['f_type']
    product=followup['product']
    description=followup['description']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO followup(name,c_name,contact,date,time,f_type,product,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(name,c_name,contact,date,time,f_type,product,description))
    mysql.connection.commit()
    cur.close()
    flash('Entry added to followup successfully','success')

    return redirect(url_for('followuptable'))
#    return render_template('edit_student.html',form=form)







@app.route('/ordertable')
@is_logged_in
def ordertable():
      cur=mysql.connection.cursor()
      result = cur.execute("SELECT *FROM orders")
      order = cur.fetchall()
      if result > 0:
          return render_template('ordertable.html',order = order)
      else:
          msg='no Entry'
          return render_template('ordertable.html',msg=msg)

      cur.close()
      return render_template('ordertable.html')






@app.route('/success_order/<string:name>', methods = ['GET', 'POST'])
@is_logged_in
def success_orded(name):


    #cursor
    cur=mysql.connection.cursor()
     #app.logger.info(name)
    result = cur.execute("SELECT *FROM orders WHERE name=%s",[name])
    orders = cur.fetchone()

    name=orders['name']
    company_name=orders['company_name']
    email=orders['email']
    phone=orders['phone']
    source=orders['source']
    address=orders['address']



    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orderslog(name,company_name,email,phone,source,address,status) VALUES(%s,%s,%s,%s,%s,%s,%s)",(name,company_name,email,phone,source,address,'successfull'))
    cur.execute("DELETE FROM orders WHERE name=%s",[name])
    mysql.connection.commit()
    cur.close()
    flash('Entry added to followup successfully','success')

    return redirect(url_for('ordertable'))
#    return render_template('edit_lead.html')








@app.route('/unsuccessful_order/<string:name>', methods = ['GET', 'POST'])
@is_logged_in
def unsuccessful_order(name):


    #cursor
    cur=mysql.connection.cursor()
     #app.logger.info(name)
    result = cur.execute("SELECT *FROM orders WHERE name=%s",[name])
    orders = cur.fetchone()

    name=orders['name']
    company_name=orders['company_name']
    email=orders['email']
    phone=orders['phone']
    source=orders['source']
    address=orders['address']



    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orderslog(name,company_name,email,phone,source,address,status) VALUES(%s,%s,%s,%s,%s,%s,%s)",(name,company_name,email,phone,source,address,'unsuccessfull'))
    cur.execute("DELETE FROM orders WHERE name=%s",[name])
    mysql.connection.commit()
    cur.close()
    flash('Entry added to orderslog successfully','success')

    return redirect(url_for('ordertable'))
#    return render_template('edit_lead.html')











@app.route('/producttable')
@is_logged_in
def producttable():
    cur=mysql.connection.cursor()
    cur.execute("UPDATE selection SET status = 'unselected' ")
    mysql.connection.commit()
    result = cur.execute("SELECT *FROM product")
    product = cur.fetchall()
    if result > 0:
        return render_template('producttable.html',product = product)
    else:
        msg='no Entry'
        return render_template('producttable.html',msg=msg)

    cur.close()
    return render_template('producttable.html')





@app.route('/productform', methods=['GET', 'POST'])
@is_logged_in
def productform():
    if request.method == 'POST':
        userDetails = request.form
        pname = userDetails['name']
        pcode = userDetails['code']
        pcategory = userDetails['category']
        vendorname = userDetails['Vendor']
        price = userDetails['Price']
        tax = userDetails['Tax']
        quantity = userDetails['Quantity']
        description = userDetails['description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO product(pname,pcode,pcategory,vendorname,price,tax,quantity,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(pname,pcode,pcategory,vendorname,price,tax,quantity,description))
        cur.execute("INSERT INTO selection(pcode,status) VALUES(%s,%s)",(pcode,'unselected'))
        mysql.connection.commit()
        cur.close()

        flash('Registerd','success')
        return redirect(url_for('producttable'))
    return render_template('productform.html')



@app.route('/delete_product/<string:id>',methods=['POST'])
@is_logged_in
def delete_product(id):

     cur=mysql.connection.cursor()
     cur.execute("DELETE FROM product where pcode=%s",[id])
     mysql.connection.commit()

     cur.close()
     flash('Entry Deleted','success')

     return redirect(url_for('producttable'))





@app.route('/product_selection')
@is_logged_in
def product_selection():
      cur=mysql.connection.cursor()
      result = cur.execute("SELECT *FROM product NATURAL JOIN selection where status !='selected'")
      product = cur.fetchall()
      if result > 0:
          return render_template('product_selection.html',product = product)
      else:
          msg='no Entry'
          return render_template('product_selection.html',msg=msg)

      cur.close()
      return render_template('product_selection.html')






@app.route('/select_order/<string:pcode>', methods = ['GET', 'POST'])
@is_logged_in
def select_order(pcode):

    cur = mysql.connection.cursor()
    cur.execute("UPDATE selection SET status='selected' WHERE pcode=%s",[pcode] )

    mysql.connection.commit()
    cur.close()
    flash('Entry added to followup successfully','success')

    return redirect(url_for('product_selection'))
#    return render_template('edit_lead.html')







@app.route('/product_quantity', methods=['GET', 'POST'])
@is_logged_in
def product_quantity():

    cur=mysql.connection.cursor()
    result = cur.execute("SELECT *FROM product NATURAL JOIN selection where status ='selected'")
    product = cur.fetchall()

    if result > 0:
        return render_template('product_quantity.html',product = product)
    else:
        msg='no Entry'
        return render_template('product_quantity.html',msg=msg)

    cur.close()
    return render_template('product_quantity.html')







@app.route('/invoice/<string:name>', methods = ['GET', 'POST'])
@is_logged_in
def invoice(name):
    if request.method == 'POST':
        userDetails = request.form
        rid = request.values.get('rid')
#        r_quantity = userDetails['rquantity']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE selection SET r_quantity=%s where pname=%s",[rid,name])
#        cur.execute("INSERT INTO selection(r_quantity) VALUES(%s) where pname=%s",(r_quantity,name))
        mysql.connection.commit()
        cur.close()
        flash('Entry added to orders successfully','success')

        return redirect(url_for('invoice'))
    return render_template('product_quantity.html')











@app.route('/invoice1')
@is_logged_in
def invoice1():
    #    return redirect(url_for('invoice'))
    return render_template('invoice.html')








@app.route('/check_product/<string:id>',methods=['POST'])
@is_logged_in
def check_product(id):

     cur=mysql.connection.cursor()
     cur.execute("UPDATE product SET status='selected' where id=%s",[id])
     mysql.connection.commit()

     cur.close()
     flash('Entry selected','success')

     return redirect(url_for('product_selection'))







@app.route('/contacttable')
@is_logged_in
def contacttable():
      cur=mysql.connection.cursor()
      result = cur.execute("SELECT distinct name,company_name,email,phone,source,address,product FROM contact")
      contact = cur.fetchall()
      if result > 0:
          return render_template('contacttable.html',contact = contact)
      else:
          msg='no Entry'
          return render_template('contacttable.html',msg=msg)

      cur.close()
      return render_template('contacttable.html')







@app.route('/contactform', methods=['GET', 'POST'])
@is_logged_in
def contactform():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        company_name = userDetails['companyname']
        email = userDetails['email']
        phone = userDetails['phone']
        source = userDetails['leadsource']
        address = userDetails['Address']
        product = userDetails['product']
        description = userDetails['description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact(name,company_name,email,phone,source,address,product,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(name,company_name,email,phone,source,address,product,description))
        mysql.connection.commit()
        cur.close()

        flash('Registerd','success')
        return redirect(url_for('contacttable'))
    return render_template('contactform.html')




@app.route('/delete_contact/<string:id>',methods=['POST'])
@is_logged_in
def delete_contact(id):

     cur=mysql.connection.cursor()
     cur.execute("DELETE FROM contact where name=%s",[id])
     mysql.connection.commit()

     cur.close()
     flash('Entry Deleted','success')

     return redirect(url_for('contacttable'))





@app.route('/report')
@is_logged_in
def report():
      cur=mysql.connection.cursor()
      result = cur.execute("SELECT *FROM contact")
      contact = cur.fetchall()
      if result > 0:
          return render_template('report.html',contact = contact)
      else:
          msg='no Entry'
          return render_template('report.html',msg=msg)

      cur.close()
      return render_template('report.html')





@app.route('/generate_report/<string:name>', methods = ['GET', 'POST'])
@is_logged_in
def generatereport(name):


    #cursor
    cur=mysql.connection.cursor()

    result = cur.execute("SELECT *FROM contact WHERE name=%s",[name])
    contact = cur.fetchone()
    result1 = cur.execute("SELECT *FROM followuplog WHERE name=%s",[name])
    followuplog = cur.fetchall()

    if result > 0:
        return render_template('generatereport.html',contact = contact, followuplog = followuplog)

    cur.close()
    return render_template('generatereport.html')









if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
