import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import random
import string
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
from schema.metadata import SchemaMetadata, INSTITUTION_TYPE_CHOICES, TYPE_CHOICES, GENDER_CHOICES, MODULE_TYPE_CHOICES
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

fake = Faker()

def generate_country_data(n=10):
    countries = []
    for i in range(1, n+1):
        countries.append({
            'id': i,
            'name': fake.country()
        })
    return pd.DataFrame(countries)

def generate_state_data(n=30, country_df=None):
    states = []
    for i in range(1, n+1):
        states.append({
            'id': i,
            'name': fake.state(),
            'code': f"ST{str(i).zfill(3)}",
            'country_code': random.choice(country_df['id'].tolist())
        })
    return pd.DataFrame(states)

def generate_district_data(n=100, state_df=None):
    districts = []
    for i in range(1, n+1):
        districts.append({
            'id': i,
            'name': fake.city(),
            'code': f"DT{str(i).zfill(3)}",
            'state_code': random.choice(state_df['id'].tolist())
        })
    return pd.DataFrame(districts)

def generate_institution_data(n=50, district_df=None):
    institutions = []
    for i in range(1, n+1):
        institutions.append({
            'id': i,
            'name': f"{fake.company()} Institution of Technology",
            'short_name': f"IIT{str(i).zfill(2)}",
            'aicte_code': f"AICTE{str(i).zfill(5)}",
            'eamcet_code': f"EAMCET{str(i).zfill(4)}",
            'l4g_code': f"L4G{str(i).zfill(6)}",
            'l4g_group_code': f"GRP{str(i).zfill(3)}",
            'type': random.choice(INSTITUTION_TYPE_CHOICES),
            'address': fake.address(),
            'website': fake.url(),
            'latlong': f"{fake.latitude()},{fake.longitude()}",
            'district_code': random.choice(district_df['id'].tolist())
        })
    return pd.DataFrame(institutions)

def generate_degree_data():
    degrees = [
        {'id': 1, 'name': 'Bachelor of Technology', 'short_name': 'BTech'},
        {'id': 2, 'name': 'Master of Technology', 'short_name': 'MTech'},
        {'id': 3, 'name': 'Bachelor of Science', 'short_name': 'BSc'},
        {'id': 4, 'name': 'Master of Science', 'short_name': 'MSc'},
        {'id': 5, 'name': 'Bachelor of Engineering', 'short_name': 'BE'}
    ]
    return pd.DataFrame(degrees)

def generate_branch_data(degree_df=None):
    branches = []
    branch_names = [
        'Computer Science', 'Electronics', 'Mechanical', 'Civil', 
        'Electrical', 'Chemical', 'Biotechnology', 'Aerospace'
    ]
    id_counter = 1
    for degree_id in degree_df['id']:
        for branch in branch_names:
            branches.append({
                'id': id_counter,
                'name': f"{branch} Engineering",
                'short_name': ''.join(word[0] for word in branch.split()),
                'degree_code': degree_id
            })
            id_counter += 1
    return pd.DataFrame(branches)

def generate_department_data(n=20):
    departments = []
    dept_names = [
        'Computer Science', 'Electronics', 'Mechanical', 'Physics',
        'Chemistry', 'Mathematics', 'English', 'Management'
    ]
    for i in range(1, n+1):
        departments.append({
            'id': i,
            'name': random.choice(dept_names) + f" Department {i}",
            'type': random.choice([t[0] for t in TYPE_CHOICES])
        })
    return pd.DataFrame(departments)

def generate_designation_data():
    designations = [
        {'id': 1, 'name': 'Professor', 'type': 'academic', 'priority': 1},
        {'id': 2, 'name': 'Associate Professor', 'type': 'academic', 'priority': 2},
        {'id': 3, 'name': 'Assistant Professor', 'type': 'academic', 'priority': 3},
        {'id': 4, 'name': 'Head of Department', 'type': 'academic', 'priority': 1},
        {'id': 5, 'name': 'Dean', 'type': 'academic', 'priority': 1}
    ]
    return pd.DataFrame(designations)

def generate_knowledge_partner_data(n=10):
    partners = []
    for i in range(1, n+1):
        partners.append({
            'id': i,
            'name': f"{fake.company()} Learning Solutions",
            'address': fake.address(),
            'website': fake.url(),
            'info': fake.text(max_nb_chars=200)
        })
    return pd.DataFrame(partners)

def generate_course_data(n=30, knowledge_partner_df=None):
    courses = []
    course_prefixes = ['Introduction to', 'Advanced', 'Fundamentals of', 'Applied']
    course_subjects = ['Programming', 'Data Science', 'AI', 'Machine Learning', 'Web Development']
    
    for i in range(1, n+1):
        courses.append({
            'id': i,
            'name': f"{random.choice(course_prefixes)} {random.choice(course_subjects)}",
            'info': fake.text(max_nb_chars=200),
            'knowledge_partner_code': random.choice(knowledge_partner_df['id'].tolist())
        })
    return pd.DataFrame(courses)

def generate_module_data(n=100, course_df=None):
    modules = []
    for i in range(1, n+1):
        modules.append({
            'id': i,
            'name': f"Module {i}: {fake.catch_phrase()}",
            'info': fake.text(max_nb_chars=200),
            'module_sequence_number': random.randint(1, 10),
            'theory_practical': random.choice([t[0] for t in MODULE_TYPE_CHOICES]),
            'duration_minutes': random.choice([30, 45, 60, 90, 120]),
            'course_code': random.choice(course_df['id'].tolist())
        })
    return pd.DataFrame(modules)

def generate_learner_data(n=1000):
    learners = []
    for i in range(1, n+1):
        gender = random.choice([g[0] for g in GENDER_CHOICES])
        learners.append({
            'id': i,
            'name': fake.name(),
            'email': fake.email(),
            'mobile': fake.phone_number(),
            'gender': gender,
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=30).strftime('%Y-%m-%d'),
            'aadhaar_number': random.randint(100000000000, 999999999999)
        })
    return pd.DataFrame(learners)

def generate_learner_education_data(n=1500, learner_df=None, institution_df=None, branch_df=None):
    educations = []
    for i in range(1, n+1):
        year_of_joining = random.randint(2015, 2022)
        educations.append({
            'id': i,
            'rollno': f"{fake.random_number(digits=2)}{fake.random_letters(length=3)}{fake.random_number(digits=3)}",
            'year_of_joining': year_of_joining,
            'year_of_graduation': year_of_joining + 4,
            'learner_code': random.choice(learner_df['id'].tolist()),
            'institution_code': random.choice(institution_df['id'].tolist()),
            'branch_code': random.choice(branch_df['id'].tolist())
        })
    return pd.DataFrame(educations)

def generate_specialization_data(n=10, knowledge_partner_df=None):
    specializations = []
    for i in range(1, n+1):
        specializations.append({
            'id': i,
            'name': f"Specialization {i}",
            'info': fake.text(max_nb_chars=200),
            'knowledge_partner_code': random.choice(knowledge_partner_df['id'].tolist())
        })
    return pd.DataFrame(specializations)

def generate_specialization_course_data(n=10, course_df=None, specialization_df=None):
    specialization_courses = []
    for i in range(1, n+1):
        specialization_courses.append({
            'id': i,
            'course_sequence_number': i,
            'course_code': random.choice(course_df['id'].tolist()),
            'specialization_code': random.choice(specialization_df['id'].tolist())
        })
    return pd.DataFrame(specialization_courses)

def generate_program_data(n=10, knowledge_partner_df=None):
    programs = []
    for i in range(1, n+1):
        programs.append({
            'id': i,
            'name': f"Program {i}",
            'info': fake.text(max_nb_chars=200),
            'knowledge_partner_code': random.choice(knowledge_partner_df['id'].tolist())
        })
    return pd.DataFrame(programs)

def generate_program_specialization_data(n=10, program_df=None, specialization_df=None):
    program_specializations = []
    for i in range(1, n+1):
        program_specializations.append({
            'id': i,
            'program_code': random.choice(program_df['id'].tolist()),
            'specialization_code': random.choice(specialization_df['id'].tolist())
        })
    return pd.DataFrame(program_specializations)

def generate_program_requirement_data(n=10, program_df=None):
    program_requirements = []
    for i in range(1, n+1):
        program_requirements.append({
            'id': i,
            'name': f"Requirement {i}",
            'is_mandatory': random.choice([True, False]),
            'program_code': random.choice(program_df['id'].tolist())
        })
    return pd.DataFrame(program_requirements)

def generate_learner_employment_data(n=100, learner_df=None, institution_df=None, department_df=None, designation_df=None):
    employments = []
    for i in range(1, n+1):
        employments.append({
            'id': i,
            'empid': fake.random_number(digits=5),
            'year_of_joining': random.randint(2015, 2022),
            'learner_code': random.choice(learner_df['id'].tolist()),
            'institution_code': random.choice(institution_df['id'].tolist()),
            'department_code': random.choice(department_df['id'].tolist()),
            'designation_code': random.choice(designation_df['id'].tolist())
        })
    return pd.DataFrame(employments)

def generate_learner_program_requirement_data(n=100, learner_df=None, program_requirement_df=None):
    learner_requirements = []
    for i in range(1, n+1):
        learner_requirements.append({
            'id': i,
            'learner_code': random.choice(learner_df['id'].tolist()),
            'program_requirement_code': random.choice(program_requirement_df['id'].tolist()),
            'value': fake.text(max_nb_chars=50)
        })
    return pd.DataFrame(learner_requirements)

def main():
    # Generate all datasets
    country_df = generate_country_data()
    state_df = generate_state_data(country_df=country_df)
    district_df = generate_district_data(state_df=state_df)
    institution_df = generate_institution_data(district_df=district_df)
    degree_df = generate_degree_data()
    branch_df = generate_branch_data(degree_df=degree_df)
    department_df = generate_department_data()
    designation_df = generate_designation_data()
    knowledge_partner_df = generate_knowledge_partner_data()
    course_df = generate_course_data(knowledge_partner_df=knowledge_partner_df)
    module_df = generate_module_data(course_df=course_df)
    learner_df = generate_learner_data()
    learner_education_df = generate_learner_education_data(
        learner_df=learner_df,
        institution_df=institution_df,
        branch_df=branch_df
    )
    specialization_df = generate_specialization_data(10, knowledge_partner_df)
    specialization_course_df = generate_specialization_course_data(10, course_df, specialization_df)
    program_df = generate_program_data(10, knowledge_partner_df)
    program_specialization_df = generate_program_specialization_data(10, program_df, specialization_df)
    program_requirement_df = generate_program_requirement_data(10, program_df)
    learner_employment_df = generate_learner_employment_data(100, learner_df, institution_df, department_df, designation_df)
    learner_program_requirement_df = generate_learner_program_requirement_data(100, learner_df, program_requirement_df)

    # Save all dataframes to CSV files
    output_dir = 'synthetic_data'
    os.makedirs(output_dir, exist_ok=True)
    
    dataframes = {
        'Country': country_df,
        'State': state_df,
        'District': district_df,
        'Institution': institution_df,
        'Degree': degree_df,
        'Branch': branch_df,
        'Department': department_df,
        'Designation': designation_df,
        'Knowledge_Partner': knowledge_partner_df,
        'Course': course_df,
        'Module': module_df,
        'Learner': learner_df,
        'Learner_Education': learner_education_df,
        'Specialization': specialization_df,
        'Specialization_Course': specialization_course_df,
        'Program': program_df,
        'Program_Specialization': program_specialization_df,
        'Program_Requirement': program_requirement_df,
        'Learner_Employment': learner_employment_df,
        'Learner_Program_Requirement': learner_program_requirement_df
    }

    for name, df in dataframes.items():
        df.to_csv(f"{output_dir}/{name}.csv", index=False)
        print(f"Generated {name}.csv with {len(df)} records")

    # Convert CSV to SQL database
    database_url = 'sqlite:///our_database.db'
    engine = create_engine(database_url)
    Base = declarative_base()

    for name, df in dataframes.items():
        # Keep the table name in the database the same as the CSV file name
        table_name = name
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Converted {name}.csv to {table_name} table in the database")

if __name__ == "__main__":
    main()