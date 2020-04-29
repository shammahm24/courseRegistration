import db
from flask import Flask, render_template, request,redirect,url_for

app = Flask(__name__)

currentUserID=0

@app.route('/')
def home():
        return render_template('index.html')

@app.route('/index')
def root():
    return render_template('index.html')
#admin related routes
@app.route('/admin',methods=['GET', 'POST'])
def admin():
    if request.method=='POST':
        print("in the post")
        value=request.form['adminID']
        print("Value returned is "+str(value))
        results=db.admin_exists(value)
        print("DB response is "+str(type(results[0])))
        if results[0]==True:
            currentUserID=value
            return render_template('admin.html')
        else:
            return redirect('/index')
    if request.method=='GET':
        return render_template('admin.html')

@app.route('/adminUsers',methods=['GET','POST'])
def adminUser():
    if request.method=='GET':
        data=db.select_users()
        return render_template('admin/users.html',data=data)

    if request.method=='POST':
        userType=request.form['type']
        fname=request.form['fname']
        print(str(fname))
        print(type(fname))
        lname=request.form['lname']
        print(str(lname))
        print(type(lname))
        email=request.form['email']
        print(str(email))
        print(type(email))
        dob=request.form['dob']
        print(str(dob))
        print(type(dob))
        address=request.form['address']
        print(str(address))
        print(type(address))
        phone=request.form['phone']
        print(str(phone))
        print(type(phone))
        nationality=request.form['nationality']
        print(str(nationality))
        print(type(fname))
        sex=request.form['sex']
        print(str(sex))
        print(type(sex))

        if userType=="student":
            major=request.form['major']
            gpa=request.form['gpa']
            print(str(gpa))
            print(type(gpa))
            advisor=request.form['advisor']
            db.insert_student(fname,lname,email,dob,address,phone,nationality,sex,major,gpa,advisor)

        if userType=="advisor":
            department=request.form['department']
            db.insert_advisor(fname,lname,email,dob,address,phone,nationality,sex,department)

        if userType=="admin":
            db.insert_admin(fname,lname,email,dob,address,phone,nationality,sex)

        return redirect('adminUsers')

@app.route('/adminUsersDelete',methods=['GET','POST'])
def deleteUser():
    if request.method=='POST':
        print("Delete route")
        value=request.form['user_id']
        db.delete_user(value)
        return redirect('adminUsers')



@app.route('/adminCourses',methods=['GET','POST'])
def adminCourses():
    if request.method=='POST':
        print("inserting course")
        value=request.form['courseName']
        print("Entered Value is "+str(value))
        db.insert_course(value)
        return redirect('/adminCourses')


    if request.method=='GET':
        data=db.select_courses()
        return render_template('admin/courses.html',data=data)

@app.route('/adminCoursesDelete',methods=['POST'])
def adminCourseDelete():
    if request.method=='POST':
        value=request.form['courseID']
        db.delete_course(value)
        return render_template('admin/courses.html')

@app.route('/adminRequests',methods=['POST','GET'])
def adminRequests():
    if request.method=='GET':
        data=db.select_approvedRequests()
        return render_template('admin/requests.html',data=data)

    if request.method=='POST':
        student=request.form['ID']
        section=request.form['sectionID']
        db.delete_request(student,section)
        return redirect('/adminRequests')

@app.route('/adminSections',methods=['GET','POST'])
def admninSections():
    if request.method=='POST':
        sectionNumber=request.form['sectionNumber']
        print("section Number:"+str(sectionNumber))
        location=request.form['location']
        print("section location:"+str(location))
        time=request.form['time']
        print("section time:"+str(time))
        days=request.form['days']
        print("section days:"+str(days))
        instructorFname=request.form['instructorFname']
        print("Fname:"+str(instructorFname))
        instructorLname=request.form['instructorLname']
        print("Lname:"+str(instructorLname))
        courseID=request.form['courseID']
        print("courseID:"+str(courseID))
        db.insert_section(sectionNumber,location,time,days,instructorFname,instructorLname,courseID)
        return redirect('/adminDepartments')

    if request.method=='GET':
        data=db.select_sections()
        return render_template('admin/sections.html',data=data)

@app.route('/adminSectionsDelete',methods=['POST'])
def adminSectionDelete():
    if request.method=='POST':
        value=request.form['sectionID']
        db.delete_section(value)
        return render_template('admin/sections.html')

@app.route('/adminDepartments',methods=['POST','GET'])
def admninDepartments():
    if request.method=='POST':
        value=request.form['departmentName']
        db.insert_department(value)
        return render_template('admin/departments.html')

    if request.method=='GET':
        data=db.select_departments()
        return render_template('admin/departments.html',data=data)


#student related routes
@app.route('/student',methods=['GET', 'POST'])
def student():
    global currentUserID
    if request.method=='POST':
        print("in the post")
        value=request.form['studentID']
        print("Value returned is "+str(value))
        results=db.student_exists(value)
        print("DB response is "+str(results))
        print("DB response is "+str(type(results[0])))
        if results[0]==True:
            currentUserID=value
            print("New Current User ID: "+str(currentUserID))
            return render_template('student.html')
        else:
            return redirect('/index')
    if request.method=='GET':
        return render_template('student.html')

@app.route('/studentregister',methods=['POST','GET'])
def studentRegiser():
    if request.method=='GET':
        data=db.select_sections()
        return render_template('student/register.html',data=data)

    if request.method=='POST':
        section=request.form['sectionID']
        print("Section ID registered:"+str(section)+" Student ID: "+str(currentUserID))
        db.registerForCourse(currentUserID,section)
        return redirect('/studentregister')

@app.route('/studentCourseSearch',methods=['POST','GET'])
def searchCourse():
    if request.method=='POST':
        course=request.form['courseName']
        data=db.select_section(course)
        return render_template('student/register.html',data=data)

@app.route('/studenthistory')
def history():
    return render_template('student/history.html')

@app.route('/studentrequests')
def studentrequests():
    data=db.select_unapprovedRequest(currentUserID)
    print("DB Data current USer: "+str(currentUserID))
    print("DB Data: "+str(data))
    return render_template('student/studentrequests.html',data=data)

#advisor related routes
@app.route('/advisor',methods=['GET', 'POST'])
def advisor():
    if request.method=='POST':
        print("in the post")
        value=request.form['advisorID']
        print("Value returned is "+str(value))
        results=db.advisor_exists(value)
        print("DB response is "+str(results))
        print("DB response is "+str(type(results[0])))
        if results[0]==True:
            currentUserID=value
            return render_template('advisor.html')
        else:
            return redirect('/index')
    if request.method=='GET':
        return render_template('advisor.html')

@app.route('/advisorMystudents',methods=['POST','GET'])
def advisorMystudents():
    if request.method=='GET':
        data=db.select_students()
        return render_template('advisor/mystudents.html',data=data)

    if request.method=='POST':
        search=request.form['searchID']
        print(str(search))
        data=db.select_student(search)
        print(str(data))
        return render_template('advisor/mystudents.html',data=data)

@app.route('/advisorCourses')
def advisorCourses():
    return render_template('advisor/courses.html')

@app.route('/advisorRequests',methods=['POST','GET'])
def advisorRequests():
    if request.method=='GET':
        data=db.select_unapprovedRequests()
        return render_template('advisor/requests.html',data=data)

    if request.method=='POST':
        student=request.form['ID']
        section=request.form['sectionID']
        db.updateRequest(student,section)
        return redirect('/advisorRequests')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
