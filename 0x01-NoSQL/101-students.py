def top_students(mongo_collection):
    # Get all students from the collection
    students = mongo_collection.find()

    # List to store students with their average score
    students_with_avg = []

    # Calculate the average score for each student
    for student in students:
        # Ensure that the student has the 'topics' field
        if 'topics' in student:
            # Calculate the average score
            total_score = sum(topic['score'] for topic in student['topics'])
            average_score = total_score / len(student['topics'])
            student['averageScore'] = average_score
            students_with_avg.append(student)

    # Sort the students by average score in descending order
    sorted_students = sorted(students_with_avg, key=lambda x: x['averageScore'], reverse=True)

    # Return the sorted list of students
    return sorted_students
