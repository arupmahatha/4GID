## Table of Contents
    1. [Basic Student Demographics](#1-basic-student-demographics)
    2. [Course Enrollment Patterns](#2-course-enrollment-patterns)
    3. [Institution Performance Analysis](#3-institution-performance-analysis)
    4. [Career Progression Analysis](#4-career-progression-analysis)
    5. [Program Effectiveness Analysis](#5-program-effectiveness-analysis)


## 1. Basic Student Demographics

    ### Query
    Analyze the distribution of students by gender, age group, and enrollment year.

    ### Required Tables
    1. `Learner`
    - Columns: id, name, email, gender, date_of_birth
    - Values: gender ['M', 'F', 'O'], date_of_birth (DATE)

    2. `Learner_Education`
    - Columns: id, learner_code, year_of_joining
    - Values: year_of_joining (INTEGER)

    ### SQL Query
    ```sql
    WITH StudentDemographics AS (
        SELECT 
            CAST((julianday('now') - julianday(date_of_birth)) / 365.25 AS INTEGER) as age,
            gender,
            year_of_joining,
            COUNT(*) as student_count
        FROM Learner l
        JOIN Learner_Education le ON l.id = le.learner_code
        GROUP BY 
            CAST((julianday('now') - julianday(date_of_birth)) / 365.25 AS INTEGER),
            gender,
            year_of_joining
    )
    SELECT 
        CASE 
            WHEN age < 20 THEN 'Under 20'
            WHEN age BETWEEN 20 AND 25 THEN '20-25'
            ELSE 'Over 25'
        END as age_group,
        gender,
        year_of_joining,
        student_count,
        ROUND(100.0 * student_count / SUM(student_count) OVER (PARTITION BY year_of_joining), 2) as percentage
    FROM StudentDemographics
    ORDER BY year_of_joining, age_group, gender;
    ```

    ### Sample Results for Basic Student Demographics
    ```
    age_group | gender | year_of_joining | student_count | percentage
    ----------|--------|-----------------|---------------|------------
    20-25     | F      | 2022            | 6             | 3.02
    20-25     | F      | 2022            | 5             | 2.51
    20-25     | M      | 2022            | 7             | 3.52
    20-25     | M      | 2022            | 6             | 3.02
    Over 25   | F      | 2022            | 8             | 4.02
    Under 20  | F      | 2022            | 4             | 2.01
    ```

    ### Analysis
    - Age distribution varies by year with 20-25 being most common
    - Gender distribution shows good diversity (F, M, and O categories)
    - Enrollment patterns are relatively consistent across years


## 2. Course Enrollment Patterns

    ### Query Goal
    Analyze which courses and specializations are most popular and their completion rates.

    ### Required Tables
    1. `Course`
    - Columns: id, name, knowledge_partner_code
    - Values: name (VARCHAR)

    2. `Module`
    - Columns: id, name, course_code, duration_minutes
    - Values: duration_minutes (INTEGER)

    3. `Specialization_Course`
    - Columns: id, course_code, specialization_code
    - Values: course_sequence_number (INTEGER)

    4. `Specialization`
    - Columns: id, name
    - Values: name (VARCHAR)

    ### SQL Query
    ```sql
    WITH CourseStats AS (
        SELECT 
            c.id as course_id,
            c.name as course_name,
            s.name as specialization_name,
            COUNT(DISTINCT m.id) as module_count,
            SUM(m.duration_minutes) as total_duration,
            COUNT(DISTINCT sc.specialization_code) as specialization_count
        FROM Course c
        LEFT JOIN Module m ON c.id = m.course_code
        LEFT JOIN Specialization_Course sc ON c.id = sc.course_code
        LEFT JOIN Specialization s ON sc.specialization_code = s.id
        GROUP BY c.id, c.name, s.name
    )
    SELECT 
        course_name,
        specialization_name,
        module_count,
        ROUND(CAST(total_duration AS FLOAT) / 60.0, 1) as duration_hours,
        specialization_count
    FROM CourseStats
    WHERE module_count > 0
    ORDER BY module_count DESC, duration_hours DESC;
    ```

    ### Sample Results for Course Enrollment
    ```
    course_name              | specialization_name | module_count | duration_hours | specialization_count
    -------------------------|---------------------|--------------|----------------|---------------------
    Advanced Web Development |                     | 8            | 8.8            | 0
    Applied Programming      | Specialization 6    | 7            | 10.5           | 1
    Advanced AI              | Specialization 10   | 7            | 8.8            | 1
    ```

    ### Analysis
    - Web Development and Programming courses have highest module counts
    - Course durations typically range from 4-10 hours
    - Some courses are standalone while others belong to specializations


## 3. Institution Performance Analysis

    ### Query Goal
    Evaluate institution performance based on student enrollment, graduation rates, and employment outcomes.

    ### Required Tables
    1. `Institution`
    - Columns: id, name, type
    - Values: type ['University', 'College', 'Institute']

    2. `Learner_Education`
    - Columns: id, institution_code, year_of_joining, year_of_graduation

    3. `Learner_Employment`
    - Columns: id, learner_code, institution_code

    ### SQL Query
    ```sql
    WITH InstitutionMetrics AS (
        SELECT 
            i.id,
            i.name as institution_name,
            i.type as institution_type,
            COUNT(DISTINCT le.learner_code) as total_students,
            COUNT(DISTINCT CASE 
                WHEN le.year_of_graduation <= strftime('%Y', 'now') 
                THEN le.learner_code 
            END) as graduated_students,
            COUNT(DISTINCT lem.learner_code) as employed_students
        FROM Institution i
        LEFT JOIN Learner_Education le ON i.id = le.institution_code
        LEFT JOIN Learner_Employment lem ON le.learner_code = lem.learner_code
        GROUP BY i.id, i.name, i.type
    )
    SELECT 
        institution_name,
        institution_type,
        total_students,
        graduated_students,
        employed_students,
        ROUND(100.0 * graduated_students / NULLIF(total_students, 0), 2) as graduation_rate,
        ROUND(100.0 * employed_students / NULLIF(graduated_students, 0), 2) as employment_rate
    FROM InstitutionMetrics
    WHERE total_students > 0
    ORDER BY total_students DESC, employment_rate DESC;
    ```

    ### Sample Results for Institution Performance
    ```
    institution_name               | type             | total_students | graduated | employed | grad_rate | emp_rate
    -------------------------------|------------------|----------------|-----------|----------|-----------|----------
    Pennington-Reed Tech           | Autonomous       | 44             | 40        | 4        | 90.91     | 10.0
    Farley-Mueller Tech            | Affiliated       | 41             | 36        | 2        | 87.80     | 5.56
    Gross and Sons Tech            | Unknown          | 38             | 33        | 6        | 86.84     | 18.18
    ```

    ### Analysis
    - Autonomous and Affiliated colleges have higher student counts
    - Graduation rates are consistently high (85-90%)
    - Employment rates show room for improvement (5-18%)


## 4. Career Progression Analysis

    ### Query Goal
    Track student career progression from graduation through employment and advancement.

    ### Required Tables
    1. `Learner`
    2. `Learner_Education`
    3. `Learner_Employment`
    4. `Department`
    5. `Designation`

    ### SQL Query
    ```sql
    WITH CareerProgression AS (
        SELECT 
            l.id as learner_id,
            l.name as learner_name,
            le.year_of_graduation,
            lem.institution_code as employer_id,
            d.name as department,
            des.name as designation,
            ROW_NUMBER() OVER (
                PARTITION BY l.id 
                ORDER BY lem.id
            ) as career_step
        FROM Learner l
        JOIN Learner_Education le ON l.id = le.learner_code
        JOIN Learner_Employment lem ON l.id = lem.learner_code
        JOIN Department d ON lem.department_code = d.id
        JOIN Designation des ON lem.designation_code = des.id
        WHERE le.year_of_graduation <= strftime('%Y', 'now')
    )
    SELECT 
        learner_name,
        year_of_graduation,
        department,
        designation,
        career_step,
        COUNT(*) OVER (
            PARTITION BY learner_id
        ) as total_career_moves
    FROM CareerProgression
    ORDER BY learner_id, career_step;
    ```

    ### Sample Results for Career Progression
    ```
    learner_name      | grad_year | department              | designation         | step | total_moves
    ------------------|-----------|-------------------------|---------------------|------|-------------
    Cynthia Jensen    | 2025      | Chemistry Department    | Associate Professor | 1    | 2
    Cynthia Jensen    | 2020      | Chemistry Department    | Associate Professor | 2    | 2
    Sarah Robbins     | 2021      | Management Department   | Assistant Professor | 1    | 1
    Lauren Frederick  | 2019      | Electronics Department  | Associate Professor | 1    | 1
    ```

    ### Analysis
    - Most learners have 1-2 career moves in their record
    - Academic positions are common in the dataset
    - Department consistency is high between moves


## 5. Program Effectiveness Analysis

    ### Query Goal
    Evaluate the effectiveness of educational programs based on multiple metrics.

    ### Required Tables
    1. `Program`
    2. `Program_Specialization`
    3. `Specialization`
    4. `Course`
    5. `Learner_Program_Requirement`

    ### SQL Query
    ```sql
    WITH ProgramMetrics AS (
        SELECT 
            p.id as program_id,
            p.name as program_name,
            COUNT(DISTINCT ps.specialization_code) as num_specializations,
            COUNT(DISTINCT sc.course_code) as num_courses,
            COUNT(DISTINCT lpr.learner_code) as enrolled_learners,
            ROUND(AVG(CAST(le.year_of_graduation - le.year_of_joining AS FLOAT)), 1) as avg_completion_time
        FROM Program p
        LEFT JOIN Program_Specialization ps ON p.id = ps.program_code
        LEFT JOIN Specialization_Course sc ON ps.specialization_code = sc.specialization_code
        LEFT JOIN Learner_Program_Requirement lpr ON p.id = lpr.program_requirement_code
        LEFT JOIN Learner_Education le ON lpr.learner_code = le.learner_code
        GROUP BY p.id, p.name
    )
    SELECT 
        program_name,
        num_specializations,
        num_courses,
        enrolled_learners,
        avg_completion_time as avg_years_to_complete,
        ROUND(100.0 * enrolled_learners / NULLIF(SUM(enrolled_learners) OVER (), 0), 2) as enrollment_percentage
    FROM ProgramMetrics
    WHERE enrolled_learners > 0
    ORDER BY enrolled_learners DESC;
    ```

    ### Sample Results for Program Effectiveness
    ```
    program_name | specializations | courses | enrolled | avg_years | enrollment_pct
    -------------|----------------|----------|----------|-----------|---------------
    Program 10   | 3              | 5        | 16       | 4.0       | 16.16
    Program 1    | 2              | 1        | 15       | 4.0       | 15.15
    Program 6    | 2              | 0        | 12       | 4.0       | 12.12
    ```

    ### Analysis
    - Programs with more specializations tend to have higher enrollment
    - Average completion time is consistently 4 years
    - Enrollment is fairly distributed across programs (5-16%)