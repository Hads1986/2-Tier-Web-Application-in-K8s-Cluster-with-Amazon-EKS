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
IMAGE = os.environ.get("IMAGE") or "newyork.jpg"
DBPORT = int(os.environ.get("DBPORT", "3306"))
key_id = os.environ.get("key_id") or "ASIARA6JQWLY5KPLEDOU"
access_key = os.environ.get("access_key") or "YOd/cBOHgQj4iPiNg901qMqaEo/sNtWug06DfFgW"
session_token = os.environ.get("session_token") or "FwoGZXIvYXdzEFMaDFAXeenBiPVUqp/2aiLKAac1hqLfZtsKa21o/qbvx0Oy7h68sVqBevqAikoSOFSazYU7YCfZWwN+D3tXue/e++MMdREifmgUkrHZ6DfRueBLbfz7OMDuCUP+IQrJ+E8p9tv7Y39nTjwVS2vIxiMyDKjGFgTxpHim0P9zIpy+rnERxdxS67FDo4bw4gu20W3LbNZSfWs3sX5e2AfRv9S8hoSr6zHbsUwmZhOQC22VfS+zC8cmhS8RY+tjAIkfkzQZ95yvmMmFi7wyMSrKqgnE5t9aBOG6hHZt7k0o1bvyoQYyLUog0ak1KjQRLXDO5cGgpxZokT0MXyDVu8i73SVbw3XjZYea7lR0BVlYF/6cRg=="

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

bucket = "s3bucket-g7"
image_default = "newyork.jpg"

@app.route("/download", methods=['GET', 'POST'])
def download(bucket = bucket, imageName = image_default):
    try:
        bucket = "s3bucket-g7"
        image_default = "newyork.jpg"
        imagesDir = "static"
        
        if not os.path.exists(imagesDir):
            os.makedirs(imagesDir)
            
        imagePath = os.path.join(imagesDir, "image.png")
        
        session = boto3.Session(
            aws_access_key_id=key_id,
            aws_secret_access_key=access_key,
            region_name="us-east-1",
            aws_session_token=session_token
            )
        
        print(bucket, imageName)
        s3 = session.resource('s3')
        s3.Bucket(bucket).download_file(imageName, imagePath)
        return os.path.join(imagesDir, "image.png")
    except Exception as e:
        print("There was en exception! Error log: ", e)
       
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', image=image)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', image=image)
    
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
    return render_template('addempoutput.html', name=emp_name, image=image)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", image=image)


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
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], image=image)

if __name__ == '__main__':
    image = download(bucket, IMAGE)
    print(image)
    app.run(host='0.0.0.0',port=81,debug=True)