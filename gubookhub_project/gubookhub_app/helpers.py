from gubookhub_app.models import Course, Subject


def list_courses(subject_name, max_results=0, contains=""):
    course_list = []
    subject = Subject.objects.get(name=subject_name)
    if contains:
        course_list = Course.objects.filter(subject=subject, title__icontains=contains).order_by('title')

    if max_results > 0:
        if len(course_list) > max_results:
            course_list = course_list[:max_results]

    return course_list

def list_subjects(contains=""):
    subject_list = []
    if contains:
        subject_list = Subject.objects.filter(name__icontains=contains).order_by('name')
    return subject_list

# split a list into x lists with n elements each
def list_split(arr, n):
    result = []
    for i in range(0,len(arr),n):
        temp = []
        for j in range(i, i+n):
            if j < len(arr):
                temp.append(arr[j])
        result.append(temp)
    return result

    