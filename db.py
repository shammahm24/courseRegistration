import mysql.connector
import sqlalchemy
from sqlalchemy import text
import mysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine




mydb = sqlalchemy.create_engine(
     #Equivalent URL:
     #mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username="#######",
        password="########",
        database="#######",
        query={"unix_socket": "/cloudsql/{}".format("adb-########-east1:project")},
    ),
)
Session = sessionmaker(bind=mydb)

# create a Session
session = Session()
mycursor = "a"#mydb.cursor(buffered=True)
conn=mydb.connect()
print(mydb)

#check ID on login
def student_exists(studentID):
    sql=sqlalchemy.text(
        "SELECT EXISTS(SELECT * FROM STUDENT WHERE StuID=:param)"
    )
    result=conn.execute(sql, param=studentID).fetchone()

    return result


def admin_exists(adminID):
    sql=sqlalchemy.text(
        "SELECT EXISTS(SELECT * FROM ADMIN WHERE adminID=:param)"
    )
    result=conn.execute(sql, param=adminID).fetchone()

    return result



def advisor_exists(advisorID):
    sql=sqlalchemy.text(
        "SELECT EXISTS(SELECT * FROM ADVISOR WHERE AdvisorID=:param)"
    )
    result=conn.execute(sql, param=advisorID).fetchone()

    return result

# Insert
def insert_department(departmentName):
    sql=sqlalchemy.text(
        "INSERT IGNORE INTO DEPARTMENT(DepName) VALUES(:param)"
    )
    conn.execute(sql, param=departmentName)



def insert_course(courseName):
    sql=sqlalchemy.text(
        "INSERT IGNORE INTO COURSE(CourseName) VALUES(:param)"
    )
    conn.execute(sql, param=courseName)


def insert_admin(fname,lname,email,dob,address,phone,nationality,sex):
    sql=sqlalchemy.text(
        "INSERT INTO USER(Fname,Lname,email,DOB,Address,Phone,isDomestic,sex) VALUES(:fname,:lname,:email,STR_TO_DATE(:date,'%d-%M-%Y'),:address,:phone,:nationality,:sex)"
    )
    conn.execute(sql,fname=fname,lname=lname,email=email,date=dob,address=address,nationality=nationality,sex=sex)

    sql1=sqlalchemy.text(
        "INSERT INTO ADMIN(AdminID) VALUES((SELECT MAX(ID) FROM USER))"
    )
    conn.execute(sql1)



def insert_instructor(department):
    sql=sqlalchemy.text(
        "INSERT INTO USER(Fname,Lname,email,DOB,Address,Phone,isDomestic,sex) VALUES(:fname,:lname,:email,STR_TO_DATE(:date,'%d-%M-%Y'),:address,:phone,:nationality,:sex)"
    )
    conn.execute(sql,fname=fname,lname=lname,email=email,date=dob,address=address,nationality=nationality,sex=sex)

    sql1=sqlalchemy.text(
        "INSERT INTO INSTRUCTOR VALUES((SELECT MAX(ID) FROM USER),(SELECT DepID FROM DEPARTMENT WHERE DepName=:department))"
    )
    conn.execute(sql1,department=department)



def insert_advisor(fname,lname,email,dob,address,phone,nationality,sex,department):
    sql=sqlalchemy.text(
        "INSERT INTO USER(Fname,Lname,email,DOB,Address,Phone,isDomestic,sex) VALUES(:fname,:lname,:email,STR_TO_DATE(:date,'%d-%M-%Y'),:address,:phone,:nationality,:sex)"
    )
    conn.execute(sql,fname=fname,lname=lname,email=email,date=dob,address=address,nationality=nationality,sex=sex)

    sql1=sqlalchemy.text(
        "INSERT INTO ADVISOR(AdvisorID,DepartmentID) VALUES((SELECT MAX(ID) FROM USER),(SELECT DepID FROM DEPARTMENT WHERE DepName=:department))"
    )
    conn.execute(sql1,department=department)

    sql2=sqlalchemy.text(
        "INSERT INTO INSTRUCTOR VALUES((SELECT MAX(ID) FROM USER),(SELECT DepID FROM DEPARTMENT WHERE DepName=:department))"
    )
    conn.execute(sql2,department=department)



def insert_student(fname,lname,email,dob,address,phone,nationality,sex,major,gpa,advisorDepartment):
    sql=sqlalchemy.text(
        "INSERT INTO USER(Fname,Lname,email,DOB,Address,Phone,isDomestic,sex) VALUES(:fname,:lname,:email,STR_TO_DATE(:date,'%d-%M-%Y'),:address,:phone,:nationality,:sex)"
    )
    conn.execute(sql,fname=fname,lname=lname,email=email,date=dob,address=address,nationality=nationality,sex=sex)

    sql1=sqlalchemy.text(
        "INSERT INTO STUDENT(StuID,Major,GPA,AdvisorID) VALUES((SELECT MAX(ID) FROM USER),:major,:gpa,(SELECT AdvisorID FROM ADVISOR JOIN DEPARTMENT ON ADVISOR.DepartmentID=DEPARTMENT.DepID WHERE DepName=:department))"
    )
    conn.execute(sql1,major=major,gpa=gpa,department=advisorDepartment)



def insert_section(sectionNumber,location,sectionTime,Days,InstructorFname,InstructorLname,CourseID):
    sql=sqlalchemy.text(
        "SELECT InstructorID FROM INSTRUCTOR JOIN USER ON INSTRUCTOR.InstructorID=USER.ID WHERE Fname=:fname AND Lname=:lname"
    )
    instructor=conn.execute(sql,fname=fname,lname=lname).fetchone()

    sql1=sqlalchemy.text(
        "INSERT INTO SECTION(SectionNumber,Location,SectionTime,Days,InstructorID,CourseID) VALUES(:sectionNumber,:location,:sectionTime,:days,:instructorID,:courseID)"
    )
    conn.execute(sql1,sectionNumber=sectionNumber,location=location,sectionTime=sectionTime,days=Days,instructorID=instructor[0],courseID=CourseID)



def registerForCourse(studentId,sectionID):
    sql=sqlalchemy.text(
        "INSERT INTO REQUEST(StuID,SectionID,isRegistered) VALUES(:studentID,:sectionID,FALSE)"
    )
    conn.execute(sql,studentID=studentId,sectionID=sectionID)



def insert_grade(grade,studentId,CourseId,semester):
    sql=sqlalchemy.text(
        "INSERT INTO GRADE(Grade,StuID,CourseID,semester) VALUES(:grade,:studentId,:courseId,:semester)"
    )
    conn.execute(sql,grade=grade,studentId=studentId,courseId=CourseId,semester=semester)


#select queries
def select_courses():
    sql=sqlalchemy.text(
        "SELECT * FROM COURSE"
    )
    courses=conn.execute(sql).fetchall()
    return courses



def select_sections():
    sql=sqlalchemy.text(
        """SELECT S.sectionID, C.CourseName,S.SectionNumber, S.Location, S.SectionTime, S.Days
        FROM SECTION S
        JOIN COURSE C ON S.CourseID=C.CourseID"""
    )
    sections=conn.execute(sql).fetchall()
    return sections

def select_section(courseName):
    sql=sqlalchemy.text(
        """SELECT S.sectionID, C.CourseName,S.SectionNumber, S.Location, S.SectionTime, S.Days
        FROM SECTION S
        JOIN COURSE C ON S.CourseID=C.CourseID
        WHERE C.CourseName=:courseName"""
    )
    sections=conn.execute(sql,courseName=courseName).fetchall()
    return sections


def select_departments():
    sql=sqlalchemy.text(
        "SELECT * FROM DEPARTMENT"
    )
    departments=conn.execute(sql).fetchall()
    return departments



def select_users():
    sql=sqlalchemy.text(
        "SELECT ID,Fname, Lname, email, phone, DOB FROM USER"
    )
    users=conn.execute(sql).fetchall()
    return users



def select_student(studentID):
    sql=sqlalchemy.text(
        """SELECT U.ID,U.Fname,U.Lname,S.GPA,U.email,U.phone,U.DOB
                FROM USER U
                JOIN STUDENT S on U.ID=S.StuID
                WHERE U.ID=:studentID"""
    )
    students=conn.execute(sql,studentID=studentID).fetchall()
    return students




def select_students():
    sql=sqlalchemy.text(
        """SELECT U.ID,U.Fname,U.Lname,S.GPA,U.email,U.phone,U.DOB
                FROM USER U
                JOIN STUDENT S on U.ID=S.StuID"""
    )
    students=conn.execute(sql).fetchall()
    return students



def select_unapprovedRequests():
    sql=sqlalchemy.text(
        """SELECT U.ID,U.Fname,U.Lname, C.CourseName, SEC.SectionNumber,SEC.sectionID
                FROM USER U
                JOIN STUDENT S on U.ID=S.StuID
                JOIN REQUEST R on S.StuID=R.StuID
                JOIN SECTION SEC on R.SectionID=SEC.sectionID
                JOIN COURSE C on C.CourseID=SEC.CourseID
                WHERE R.isRegistered=FALSE"""
    )
    requests=conn.execute(sql).fetchall()
    return requests

def select_unapprovedRequest(studentID):
    sql=sqlalchemy.text(
        """SELECT U.ID,U.Fname,U.Lname, C.CourseName, SEC.SectionNumber,SEC.sectionID
                FROM USER U
                JOIN STUDENT S on U.ID=S.StuID
                JOIN REQUEST R on S.StuID=R.StuID
                JOIN SECTION SEC on R.SectionID=SEC.sectionID
                JOIN COURSE C on C.CourseID=SEC.CourseID
                WHERE R.isRegistered=FALSE AND R.StuID=:stuID"""
    )
    requests=conn.execute(sql,stuID=studentID).fetchall()
    return requests


def select_approvedRequests():
    sql=sqlalchemy.text(
        """SELECT U.ID,U.Fname,U.Lname, C.CourseName, SEC.SectionNumber,SEC.sectionID
                FROM USER U
                JOIN STUDENT S on U.ID=S.StuID
                JOIN REQUEST R on S.StuID=R.StuID
                JOIN SECTION SEC on R.SectionID=SEC.sectionID
                JOIN COURSE C on C.CourseID=SEC.CourseID
                WHERE R.isRegistered=TRUE"""
    )
    requests=conn.execute(sql).fetchall()
    return requests

def select_advisor(advisorID):
    sql=sqlalchemy.text(
        """SELECT U.ID,U.Fname,U.Lname
                FROM USER U
                JOIN ADVISOR A on U.ID=A.AdvisorID
                WHERE U.ID=:advisorID"""
    )
    advisors=conn.execute(sql,advisorID=advisorID).fetchall()
    return advisors

#update queries
def updateRequest(studentID,sectionID):
    sql="UPDATE REQUEST SET isRegistered=TRUE WHERE StuID=:studentID AND SectionID=:sectionID"
    conn.execute(sql,studentID=studentID,sectionID=sectionID)


#delete queries
def delete_user(userId):
    sql=sqlalchemy.text(
        "DELETE FROM USER WHERE ID=:userid"
    )
    conn.execute(sql,userid=userId)


    sql=sqlalchemy.text(
        "DELETE FROM STUDENT WHERE ID=:userid"
    )
    conn.execute(sql,userid=userId)


    sql=sqlalchemy.text(
        "DELETE FROM ADVISOR WHERE ID=:userid"
    )
    conn.execute(sql,userid=userId)


    sql=sqlalchemy.text(
        "DELETE FROM INSTRUCTOR WHERE ID=:userid"
    )
    conn.execute(sql,userid=userId)


    sql=sqlalchemy.text(
        "DELETE FROM ADMIN WHERE ID=:userid"
    )
    conn.execute(sql,userid=userId)


def delete_course(courseId):
    sql=sqlalchemy.text(
        "DELETE FROM COURSE WHERE CourseID=:courseId"
    )
    conn.execute(sql,courseId=courseId)


def delete_section(sectionId):
    sql=sqlalchemy.text(
        "DELETE FROM SECTION WHERE sectionID=:sectionid"
    )
    conn.execute(sql,sectionid=sectionId)


def delete_department(depId):
    sql=sqlalchemy.text(
        "DELETE FROM DEPARTMENT WHERE DepID=:depid"
    )
    conn.execute(sql,depid=depId)


def delete_request(stuID,section):
    sql=sqlalchemy.text(
        "DELETE FROM REQUEST WHERE StuID=:studentID AND SectionID=:sectionID"
    )
    conn.execute(sql,studentID=stuID,sectionID=section)
