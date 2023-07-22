import heapq
import random

class Event:
    def __init__(self, event_type, event_time, event_parameters):
        self.event_type = event_type
        self.event_time = event_time
        self.event_parameters = event_parameters
    
    def __lt__(self, other):
        return self.event_time < other.event_time

class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.enrolled_courses = []
    
    def __repr__(self):
        return f"{self.name} (ID: {self.student_id})"

class Course:
    def __init__(self, course_code, course_name, max_capacity):
        self.course_code = course_code
        self.course_name = course_name
        self.max_capacity = max_capacity
        self.current_enrollment = 0
        self.enrolled_students = []
    
    def __repr__(self):
        return f"{self.course_name} (Code: {self.course_code})"

def initialize_simulation():
    server_idle_time = 0.0
    total_waiting_time = 0.0
    students_waited = 0

    # Initialize the list of courses with their maximum capacities
    courses = [
        Course("MCS", "Maths and Computer Science", 100),
        Course("CS", "Computer Science", 80),
        Course("DM ", "Double Maths", 60),
    ]

    enrolled_students = []
    event_queue = []

    # Generate initial events for student arrivals
    for i in range(1, 101):  # Assuming 100 students will enroll
        arrival_time = random.uniform(0, 10)  # Random arrival time between 0 to 10 (for simplicity)
        student_id = f"STU{i}"
        student_name = f"Student {i}"
        student_age = random.randint(17, 20)  # Random age between 17 to 20 (for simplicity)

        student = Student(student_id, student_name, student_age)
        course_choices = random.sample(courses, random.randint(1, 2))  # Randomly select 2 to 5 courses
        event_parameters = (student, course_choices)

        event = Event("Student Arrival", arrival_time, event_parameters)
        heapq.heappush(event_queue, event)

    # Add additional events for capacity changes, if necessary
    # For example, if you want to change the capacity of a course after a certain time
    
    return courses, enrolled_students, event_queue, server_idle_time, total_waiting_time, students_waited

def simulate_events(courses, enrolled_students, event_queue):
    server_idle_time = 0.0
    total_waiting_time = 0.0
    students_waited = 0
    current_time = 0.0

    while event_queue:
        current_event = heapq.heappop(event_queue)
        event_type = current_event.event_type
        event_parameters = current_event.event_parameters

        if current_time < current_event.event_time:
            server_idle_time += current_event.event_time - current_time
            current_time = current_event.event_time

        if event_type == "Student Arrival":
            student, course_choices = event_parameters
            print(f"{student} arrives at time {current_time:.2f}.")

            # Process student arrival event
            for course in course_choices:
                if course.current_enrollment < course.max_capacity:
                    course.current_enrollment += 1
                    course.enrolled_students.append(student)
                    student.enrolled_courses.append(course)
                    print(f" - Enrolled in: {course}")
                else:
                    print(f" - {course} is full. Cannot enroll.")
                    total_waiting_time += current_time
                    students_waited += 1

        elif event_type == "Capacity Change":
            # Process course capacity change event
            # For example, if you want to change the capacity of a course at a specific time
            pass

    # Calculate server idle time for the remaining events
    if enrolled_students or event_queue:
        server_idle_time += current_time

    return server_idle_time, total_waiting_time, students_waited


def track_simulation_statistics(enrolled_students, server_idle_time, total_waiting_time, students_waited):
    total_students = len(enrolled_students) + students_waited
    average_waiting_time = total_waiting_time / students_waited if students_waited > 0 else 0
    probability_to_wait = students_waited / total_students if total_students > 0 else 0

    return average_waiting_time, probability_to_wait

def output_results(enrolled_students, average_waiting_time, probability_to_wait, server_idle_time):
    print("\nEnrollment Status:")
    for student in enrolled_students:
        print(f"{student.name} (ID: {student.student_id}) enrolled in {len(student.enrolled_courses)} courses.")

    print("\nSimulation Results:")
    print(f"Average Waiting Time: {average_waiting_time:.2f} time units")
    print(f"Probability to Wait in Line: {probability_to_wait:.2f}")
    print(f"Server Idle Time: {server_idle_time:.2f} time units")

def simulate_student_enrollment():
    courses, enrolled_students, event_queue, server_idle_time, total_waiting_time, students_waited = initialize_simulation()
    server_idle_time, total_waiting_time, students_waited = simulate_events(courses, enrolled_students, event_queue)
    average_waiting_time, probability_to_wait = track_simulation_statistics(enrolled_students, server_idle_time, total_waiting_time, students_waited)
    output_results(enrolled_students, average_waiting_time, probability_to_wait, server_idle_time)

# Run the simulation
simulate_student_enrollment()
