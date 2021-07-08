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
            t = re.findall('http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',line)
            
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
        a = " "
        if '' in line:
            a = re.findall(r'(\/.*?\.[\w:]+)',line)
            print(a)
            if a == []:
                print(type(a))
                msg = "Incorrect format for WORKDIR"
                return msg

            else:
                msg = "All good"
                return msg
                
    if command == 'USER':
        b = " "
        if '' in line:
            b = re.findall(r'^[$]?[a-zA-Z0-9_.+-]+',line)
            print(b)
            if b == []:
                print(type(b))
                msg = "Incorrect format for USER"
                return msg

            else:
                msg = "All good"
                return msg

    if command == 'ARG':
        c = " "
        if '' in line:
            c = re.findall(r'(\w*)=?(\".*?\"|\S*)', line)
            print(c)
            if c == [('', '')]:
                print(type(c))
                msg = "Incorrect format for ARG"
                return msg

            else:
                msg = "All good"
                return msg

    if command == 'ENV':
        d = " "
        if '' in line:
            d = re.findall(r'(\w*)=(\"[\w\s\+()\.]*\"|[\w\s\-\:\.])*(\w*.?))', line)
            print(d)
            if d == []:
                print(type(d))
                msg = "Incorrect format for ENV"
                return msg

            else:
                msg = "All good"
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
        commands = ['FROM','EXPOSE','COPY','ADD','WORKDIR','USER','ARG','ENV']
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
    