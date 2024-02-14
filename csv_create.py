import csv
with open('D:/django_project/attendance_management/attendance_sheet.csv', 'a', newline='') as csvfile:
    data = []
    name = "Student Name"
    lecture = "Lecture"
    date = "Date"
    attendance = "Attendance"
    data.append(name)
    data.append(lecture)
    data.append(date)
    data.append(attendance)
    result = [data]
    csvwriter = csv.writer(csvfile, escapechar='\\')
    for row in result:
        csvwriter.writerow(row)
    print("Student Present : ", name)
