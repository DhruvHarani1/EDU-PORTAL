# Student Performance Intelligence - Documentation

## Overview
The **Student Performance Intelligence** module is a sophisticated analytics engine designed to move beyond simple grading sheets. Instead of just showing *what* a student scored, it analyzes *how* they scored it, identifying patterns of consistency, growth, and volatility.

---

## 1. Performance vs. Stability Matrix (The Scatter Plot)

### **What is it?**
This chart answers the question: *"Is this student reliable?"*
It plots every student on a 2-dimensional plane based on two distinct metrics: **Average Score** and **Stability Score**.

### **How it Works**
*   **X-Axis (Performance)**: The student's average percentage across all exams.
    *   *Right* = High Grades.
    *   *Left* = Low Grades.
*   **Y-Axis (Unpredictability)**: calculated using the Standard Deviation of their scores.
    *   **Inverted Axis**: We invert this axis so that the "Best" outcome (Low Standard Deviation / High Consistency) is at the **Top**.
    *   *Top* = Consistent (Scores basically stay the same).
    *   *Bottom* = Volatile (Scores fluctuate wildly, e.g., 90% in one test, 40% in another).

### **The Four Quadrants**
1.  **🏆 Consistent Toppers (Top Right)**:
    *   *High Scores + High Stability*.
    *   These are your "Set and Forget" students. They consistently perform at an elite level.
2.  **⚠️ Struggling (Top Left)**:
    *   *Low Scores + High Stability*.
    *   **Critical Insight**: These students are consistently failing. They aren't having "bad days"; they have a fundamental gap in understanding. They need different teaching methods, not just "more study."
3.  **⚡ Volatile Geniuses (Bottom Right)**:
    *   *High Avg + Low Stability*.
    *   These students are capable of brilliance but unreliable. They might ace Math but fail Ethics, or ace Mid-terms but flake on Finals. They need discipline/focus coaching.
4.  **📉 Critical / Chaotic (Bottom Left)**:
    *   *Low Avg + Low Stability*.
    *   The most dangerous zone. They are failing and their performance is erratic. Requires immediate intervention.

---

## 2. Class Academic DNA (Radar Chart)

### **What is it?**
A visual footprint of the entire batch's intellectual strengths and weaknesses.

### **How it Works**
*   It aggregates the average marks of *every student* for *every subject*.
*   **Shape Analysis**:
    *   **Perfect Circle**: A well-rounded class functioning equally well in all subjects.
    *   **Spiky Shape**: Indicates Imbalance. If the "Math" point is far out but "History" is close to the center, the class is technically strong but theoretically weak.
    *   **Small Shape**: The entire batch is underperforming across the board.

---

## 3. Critical Attention Required (The Danger Zone)

### **What is it?**
A prioritized "Triage List" for the Faculty. It automatically flags students who are at risk of dropping out or failing the year.

### **The Logic**
A student enters the Danger Zone if:
1.  **Average Score < 40%**: Failing threshold.
2.  (Optional/Hidden Logic): **Fail Count > 2 Subjects**.

### **Strategic Value**
Faculty members should check this list every Monday. The "Intervention Plan" link allows them to view the specific student's breakdown and schedule counseling.

---

## 4. AI Executive Review (Insights Engine)

### **What is it?**
An automated "Data Scientist" that reviews the raw numbers and generates plain-English feedback for the Head of Department (HOD).

### **How the Heuristics Work**
The AI doesn't just "guess"; it follows a strict decision tree based on **Growth Velocity**:

1.  **Growth Velocity Calculation**:
    *   The system compares `Semester 1 Average` vs `Semester 3 Average` for every student.
    *   *Positive Growth*: Student is improving.
    *   *Negative Growth*: Student is declining.

2.  **Batch Status Determination**:
    *   If total average growth > 2%: Status = **"Improving"**.
    *   If total average growth < -2%: Status = **"Declining"**.
    *   Otherwise: Status = **"Stable"**.

3.  **Strategic Suggestions**:
    *   *Scenario A (Declining > Improving)*: Suggests "Reviewing Teaching Pace" (The material might be too fast).
    *   *Scenario B (>10% of class in Danger Zone)*: Suggests "Parent-Teacher Meetings" (Systemic failure).
    *   *Scenario C (Stable)*: Suggests "Maintaining Momentum".

4.  **Actionable Tips**:
    *   The system dynamically counts how many students are "Rising Stars" (High Growth) and suggests using them as peer mentors.
    *   It identifies the count of students in the "Top Left" quadrant and suggests focusing on their foundational concepts.

---
---

# Engagement & Attendance Metrics

## Overview
The **Engagement Module** shifts focus from grades to **behavior**. It answers the question: *"Are students showing up, and are they burned out?"*
It uses attendance data to predict dropout risks and identify systemic scheduling fatigue.

---

## 5. Weekly Engagement Pulse (The "Burnout" Chart)

### **What is it?**
A bar chart that visualizes the collective energy levels of the class across the week (Mon-Fri).

### **How it Works**
*   It calculates the **Aggregate Attendance %** for each day of the week over the entire semester.
*   **Color Logic**:
    *   **Indigo (Normal)**: Attendance > 70%.
    *   **Red ("Burnout Day")**: Attendance < 70%.
    
### **Strategic Value**
If the chart turns **Red on Fridays**, it indicates "Weekend Fatigue."
*   *Action*: Move heavy lectures (Math, Physics) to Tue/Wed and keep Fridays for lighter labs or seminars.
If the chart turns **Red on Mondays**, it indicates "Momentum Loss."
*   *Action*: Introduce quizzes or gamified starts to the week.

---

## 6. Truancy Risk Registry (Dropout Prediction)

### **What is it?**
A "Watch List" of students who are dangerously close to being detained or dropping out due to lack of attendance.

### **The Probability Model**
The system treats **75% Attendance** as the critical academic threshold.
*   **Risk Calculation**: `Probability of Dropout = 100 - Attendance %`.
*   *Example*: A student with 40% attendance has a **60% Probability** of being detained or dropping out.

### **Status Codes**
*   **At Risk**: Any student below 75%.
*   **Critical**: Any student below 60%.

---

## 7. AI Pattern Recognition (Behavioral Insights)

### **What is it?**
The AI looks for non-obvious patterns in the daily logs to suggest administrative changes.

### **Detected Patterns**
1.  **Fatigue detection**:
    *   The AI scans for the "Lowest Attendance Day" of the week.
    *   If that day drops below 70%, it flags a **"Fatigue Alert"** and suggests rescheduling heavy classes.
    
2.  **Systemic Truancy**:
    *   The AI counts how many students are in the *Truancy Risk Registry*.
    *   If **> 15%** of the class is at risk, it flags a **"High Truancy Risk"** alert. This implies the issue is not with individual students, but with the course itself (e.g., bad timing, poor transport, toxic environment).
    *   *Action*: "Initiate Automated SMS Warnings".
