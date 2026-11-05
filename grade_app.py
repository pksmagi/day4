
import streamlit as st

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Grade Manager")
st.write("Add students and view their academic performance.")

# ---------------- GRADE CALCULATION ----------------
def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


# ---------------- SESSION STATE ----------------
# Student records survive Streamlit reruns.
if "students" not in st.session_state:
    st.session_state.students = []


# ---------------- ADD STUDENT FORM ----------------
st.subheader("Add a Student")

with st.form("student_form"):
    name = st.text_input("Student Name")

    mark = st.number_input(
        "Student Mark",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5
    )

    submitted = st.form_submit_button("Add Student")

    if submitted:
        if not name.strip():
            st.error("Please enter the student name.")

        elif not 0 <= mark <= 100:
            st.error("Mark must be between 0 and 100.")

        else:
            student = {
                "Name": name.strip(),
                "Mark": mark,
                "Grade": get_grade(mark)
            }

            st.session_state.students.append(student)

            st.success(f"{name.strip()} added successfully!")


# ---------------- STUDENT RESULTS ----------------
st.subheader("Student Results")

if st.session_state.students:

    st.dataframe(
        st.session_state.students,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- CLASS STATISTICS ----------------
    marks = [
        student["Mark"]
        for student in st.session_state.students
    ]

    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    st.subheader("Class Figures")

    col1, col2, col3 = st.columns(3)

    col1.metric("Class Average", f"{average:.1f}")
    col2.metric("Highest Mark", f"{highest:g}")
    col3.metric("Lowest Mark", f"{lowest:g}")

    st.write("Total Students:", len(st.session_state.students))

else:
    st.info("No students added yet. Please add a student.")
    
    col1, col2, col3 = st.columns(3)

    col1.metric("Class Average", "—")
    col2.metric("Highest Mark", "—")
    col3.metric("Lowest Mark", "—")
