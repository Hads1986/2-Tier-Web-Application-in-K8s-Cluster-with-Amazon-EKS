from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import boto3

app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "password"
DATABASE = os.environ.get("DATABASE") or "employees"
BGIMG = os.environ.get("BGIMG") or "toronto.jpg"
GRPNAME = os.environ.get("GRPNAME") or "Group 17"
DBPORT = int(os.environ.get("DBPORT", "3306"))
key_id = os.environ.get("key_id") or "ASIARA6JQWLYY4WTXQ4B"
access_key = os.environ.get("access_key") or "2WmuCHhzDkmG3qv/ncd7tX+zlFvQOZaStKLk7fsE"
session_token = os.environ.get("session_token") or "FwoGZXIvYXdzEDQaDLJ0cuEznK5xA3FSWiLKATd96yurEzt3b3GPQSHo/f0Hhc5bVm5Ehbh18Kgh9LR0dfZ7md0BBPzYon0z2mbLGsh0QOcuqxUY+WOJbO2yp5FItQJjmEuKbxCo1p5+prwdtOAERI0VCgccggLMcNJT+RySfLNG/0k/frboJuYrT+arvzAf+aqvkYHEr+hEhHFZ3JfSNhuk1ecSjEsRgatquVImNNHVlGKu+3aJgYhi1G1/UMiHKcBpibiTY62H0hJ7TTkMXFwZQsYntCptP8IiKLkqE0G0gzX2WIYo7dvroQYyLfCM5kcozCUiHRyYPf0ocN1xilofWNw7cEzE8cbNMG9DzmDkgruLM3kYI2fphA=="

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
)

output = {}
table = 'employee';

bucket = "s3bucket-g7" #"clo835images17jaspreet"
image_default = "toronto.jpg"

@app.route("/download", methods=['GET', 'POST'])
def download(bucket = bucket, imageName = image_default):
    try:
        imagesDir = "static"
        if not os.path.exists(imagesDir):
            os.makedirs(imagesDir)
        bgImagePath = os.path.join(imagesDir, "background.png")
        
        session = boto3.Session(
            aws_access_key_id=key_id,
            aws_secret_access_key=access_key,
            region_name="us-east-1",
            aws_session_token=session_token
            )
        
        print(bucket, imageName)
        s3 = session.resource('s3')
        s3.Bucket(bucket).download_file(imageName, bgImagePath)
        return os.path.join(imagesDir, "background.png")
    except Exception as e:
        print("Exception occured while fetching the image! Check the log --> ", e)
       
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', image=image, group_name=GRPNAME)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', image=image, group_name=GRPNAME)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, image=image, group_name=GRPNAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", image=image, group_name=GRPNAME)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], image=image, group_name=GRPNAME)

if __name__ == '__main__':
    image = download(bucket, BGIMG)
    print(image)
    app.run(host='0.0.0.0',port=8080,debug=True)