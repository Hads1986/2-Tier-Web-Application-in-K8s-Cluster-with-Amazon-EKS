from flask import Flask, render_template, request, url_for
from pymysql import connections
import os
import boto3
import botocore

app = Flask(__name__)

DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPWD = os.environ.get("DBPWD")
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT"))

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port= DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
)

output = {}
table = 'employee';

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html')

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html')
    
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
    return render_template('addempoutput.html', name=emp_name)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html")


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
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
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"])
                           
def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket to the /tmp/ directory
    """
    s3 = boto3.resource('s3')
    output = f"/tmp/{file_name}"  # Use the /tmp/ directory for storing the downloaded file
    s3.Bucket(bucket).download_file(file_name, output)

    return output

# Replace "my-bucket-name" and "my-image.jpg" with your own bucket and file names
file_name = "toronto.jpg"
bucket = "s3bucket-g7"

# Call the function to download the file and save it locally
local_file_path = download_file(file_name, bucket)
print(f"File downloaded and saved to {local_file_path}")

    app.run(host='0.0.0.0',port=8080,debug=True)