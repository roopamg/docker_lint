from flask import Flask, render_template, request
import os
import re

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY  

if __name__ == '__main__':
   app.run(debug = True)


def validate(command, line):
    msg = ""
    if command == 'FROM':
        if ' ' in line:
            msg = "Image name is not valid in FROM statement"
            return msg
        elif '' not in line:
            t = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',line)
            
        else:
            return 1
    if command == 'COPY':
        count = line.count(' ')
        print (line)
        if count != 1:
            msg = "Incorrect Format for COPY"
            return msg
        else:
            return 1
    if command == 'ADD':
        count = line.count(' ')
        print (line)
        if count != 1:
            msg = "Incorrect Format for COPY"
            return msg
        else:
            return 1
    """        
    if command == 'LABEL':
        if ' ' not in line:
            #t = re.findall(r'[A-Za-z0-9-.]=[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',line)
            t = re.findall(r'\b\w+:[\w\s]+\b(?!:)',line)
            
        else:
            msg = "Incorrect Format for LABEL"
            return msg
            """
            
    if command == 'WORKDIR':
        if '' in line:
            t = re.findall(r'(\/.*?\.[\w:]+)',line)

            msg = "All good"
            return msg
        else:
            msg = "Incorrect format for WORKDIR"
            return msg


    if command == 'EXPOSE':
        if '/' in line:
            line = line.split('/')
            if line[0].isnumeric():
                if line[1].upper() == 'TCP' or line[1].upper() == 'UDP':
                    return 1
                else:
                    msg = "Incorrect Protocoal in EXPOSE statement, It should be either TCP or UDP"
                    return msg
            else:
                msg = "Not valid port in EXPOSE statement"
                return msg
        elif line.count(' ') == 0:
            if line.isnumeric():
                return 1
            else:
                msg = "Not valid EXPOSE statement"
                return msg
        else:
            msg = "Not Valid Expose Statement"        
            return msg




@app.route("/",methods=['GET','POST'])                 
def hello():
    msg = ""
    code = ""
    if request.method == 'POST':
        code = request.form['code']
        nlines = code.count('\n')
        commands = ['FROM','EXPOSE','COPY','ADD','WORKDIR']
        for line in code.splitlines():
            print(line)
            cmd = line.split(" ",1)
            if cmd[0] not in commands:
                command = str(cmd[0])
                msg = "Error Validating "+command+", command not found"
            else:
                msg = validate(str(cmd[0]), cmd[1])
                if msg != 1:
                    break
    if msg == 1:
        msg = "All is well with your file"                
    templatedata = {
    'message' : msg, 'code': code
        }
    return render_template("lint.html", **templatedata)


@app.route('/demo')
def submit():

    return render_template("docker.html")

# @app.route('/submit', methods=['POST'])
# def submit():
#     error = ""
#     code = request.form['code']
#     nlines = code.count('\n')
#     commands = ['FROM','RUN','CMD','COPY','ADD']
#     for line in code.splitlines():
#         print(line)
#         #msg = check(line.split(" ",1)
#         if line not in commands:
#             msg = "Error Validating "+line+" command not found"
#         else:
#             msg = "All is well with your file"
#     return render_template("test.html",data=msg)
#     #return 'You entered: {}'.format(request.form['code'])
    