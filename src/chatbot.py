def get_answer(question):
    question = question.lower()
    
    campus_info = {
        "library": "Library is open 9AM - 6PM, located in Main Block Ground Floor.",
        "canteen": "Canteen is at Ground Floor, Main Block. Open 8AM - 8PM.",
        "placement": "Placement Cell is in Block B, Room 101. Contact: placement@college.edu",
        "principal": "Principal is Dr. [Name]. Office at Admin Block, Room 1.",
        "cse": "CSE Department is in Block A. HOD: Prof. [Name]",
        "hostel": "Boys Hostel: North Campus. Girls Hostel: South Campus.",
        "fee": "Fee payment can be done online at college portal or at accounts section.",
        "admission": "Admissions open in June. Visit admin office or college website.",
    }
    
    for keyword, answer in campus_info.items():
        if keyword in question:
            return answer
    
    return "I don't have that information yet. Please contact the admin office or visit the college website."
