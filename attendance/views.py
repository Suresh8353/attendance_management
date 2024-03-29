from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import cv2
import json, os, time
import face_recognition
import csv
from datetime import datetime
from .models import Students


def college_home(request):
    return render(request, 'home_page.html')


def take_attendance(request):
    lecture = ''
    if request.method == 'POST':
        data = json.loads(request.body)
        lecture = data.get('subject', None)
    output_path = 'H:/attendance_management/static/webcam_capture.jpeg'
    webcam = cv2.VideoCapture(0)
    # Check if the webcam is opened successfully
    if not webcam.isOpened():
        print("Error: Unable to open webcam.")
        return render(request, 'present.html', {'data': 'Unable to open webcam'})
    start_time = time.time()
    # Capture frames for 3 seconds
    while time.time() - start_time < 3:
        # Read a frame from the webcam
        success, frame = webcam.read()

    if not success:
        print("Error: Unable to read frame from webcam.")
        return render(request, 'present.html', {'data': 'Unable to read frame from webcam'})

    # Save the frame as an image
    cv2.imwrite(output_path, frame)
    # Release the webcam
    webcam.release()
    print("Image captured successfully.")
    target_image = frame
    folder_path = 'H:/attendance_management/static/student_images'
    file_names = os.listdir(folder_path)
    dataset_images = []
    student_names = []
    for file_name in file_names:
        if file_name.endswith('.jpeg'):
            image_path = os.path.join(folder_path, file_name)
            image = cv2.imread(image_path)
            dataset_images.append(image)
            student_names.append(file_name)
    # Convert the target image to RGB format (face_recognition expects RGB)
    target_rgb = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)

    # Detect faces in the target image
    target_face_locations = face_recognition.face_locations(target_rgb)
    target_face_encodings = face_recognition.face_encodings(target_rgb, target_face_locations)

    # Iterate through the dataset images
    for idx, dataset_image in enumerate(dataset_images):
        # Convert the dataset image to RGB format
        dataset_rgb = cv2.cvtColor(dataset_image, cv2.COLOR_BGR2RGB)
        # Detect faces in the dataset image
        dataset_face_locations = face_recognition.face_locations(dataset_rgb)
        dataset_face_encodings = face_recognition.face_encodings(dataset_rgb, dataset_face_locations)
        # Compare face encodings
        for target_encoding in target_face_encodings:
            for dataset_encoding in dataset_face_encodings:
                match = face_recognition.compare_faces([target_encoding], dataset_encoding)
                if match[0]:
                    matched_student = student_names[idx]
                    print(matched_student)
                    with open('H:/attendance_management/attendance_sheet.csv', 'a', newline='') as csvfile:
                        current_datetime = datetime.now()
                        d_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        data = []
                        name = matched_student.split(".")[0]
                        date = d_time
                        attendance = "Present"
                        data.append(name)
                        data.append(lecture)
                        data.append(date)
                        data.append(attendance)
                        result = [data]
                        csvwriter = csv.writer(csvfile, escapechar='\\')
                        for row in result:
                            csvwriter.writerow(row)
                        print("Student Present : ", name)
                        return JsonResponse({'message': f'Attendance taken for lecture: {lecture} of student {name}'})
                        # Return the present.html template with the data
    print("student Absent")
    return JsonResponse({"message": "Student is not present in class"})


def student_admission(request):
    if request.method == 'POST':
        name = request.POST.get('sname')
        father_name = request.POST.get('fname')
        course = request.POST.get('course')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        religion = request.POST.get('religion')
        image = request.POST.get('image')
        student_data = Students.objects.all()
        roll_number = len(student_data) + 1
        for student in student_data:
            if student.name == name and student.father_fame == father_name and student.mobile == int(mobile) and str(
                    student.dob) == dob:
                return HttpResponse(f'''<div style="margin:auto;margin-top:50px; border: 2px solid black; 
                        width:600px;height:400px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                        <h3 style='text-align:center;background-color:purple; color:white'>
                        Welcome {student.name} in my College</h3>
                        <h3>Sorry, You can't take admission again, because you are already student of my college.</h3>
                        <br><br><a href="/" style="margin-left:250px;">Back</a>''')
        Students.objects.create(name=name, roll_number=roll_number, father_name=father_name, dob=dob,
                                gender=gender, email=email, mobile=mobile, course=course, address=address,
                                city=city, state=state, pin=pin, religion=religion, image=image)
        return HttpResponse(f'''<div style="margin:auto;margin-top:100px; border: 2px solid black; 
                    width:620px;height:800px;font-size:25px; background-color:lightgrey; border-radius:30px;">
                    <h3 style='text-align:center;background-color:purple; color:white'>
                    Welcome {name} in my College</h3>
                    <h3>Your Admission process done successfully. Now you are student of my college</h3>
                    <table style="margin:auto;font-size:25px">
                    <tr><th>Student Image :</th><td>{image}</td></tr>
                    <tr><th>Student Name :</th><td>{name}</td></tr>
                    <tr><th>Roll Number :</th><td>{roll_number}</td></tr>
                    <tr><th>Father's Name :</th><td>{father_name}</td></tr>
                    <tr><th>Date Of Birth :</th><td>{dob}</td></tr>
                     <tr><th>Gender :</th><td>{gender}</td></tr>
                    <tr><th>Email ID :</th><td>{email}</td></tr>
                    <tr><th>Mobile No. :</th><td>{mobile}</td></tr>
                    <tr><th>Course :</th><td>{course}</td></tr>
                    <tr><th>Address :</th><td>{address}</td></tr>
                    <tr><th>Customer Name :</th><td>{city}</td></tr>
                    <tr><th>Father's Name :</th><td>{state}</td></tr>
                    <tr><th>Account No. :</th><td>{pin}</td></tr>
                    <tr><th>Father's Name :</th><td>{religion}</td></tr>
                </table><br><br><a href="/" style="margin-left:250px;">Back</a>''')

    else:
        return render(request, 'student_admission.html')


def student_information(request):
    info = Students.objects.all()
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%H:%M:%S')
    with open('H:/attendance_management/attendance_sheet.csv', mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        num_rows = 0
        for row in csv_reader:
            # student, lecture, date_str, attendance = row
            # date = datetime.strptime(date_str, '%Y-%m-%d').date()
            # if date == current_date:
            num_rows += 1
        data = {
            'total_student': info.count(),
            "present_student": num_rows - 1
        }
    return render(request, 'student_information.html', {'data': data})


def total_student(request):
    info = Students.objects.all()
    return render(request, 'total_student.html', {'data': info})


def present_student(request):
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%H:%M:%S')
    current_date_students = []
    with open('H:/attendance_management/attendance_sheet.csv', mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # print(row)
            # student, lecture, date_str, attendance = row
            # date = datetime.strptime(date_str, '%Y-%m-%d').date()
            # if date == current_date:
            current_date_students.append(row)
        print(current_date_students)
    return render(request, "present_student.html", {'data': current_date_students})
