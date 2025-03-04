import pymongo
from generate_synthetic_data import (
    generate_country_data, generate_state_data, generate_district_data,
    generate_institution_data, generate_degree_data, generate_branch_data,
    generate_department_data, generate_designation_data, generate_knowledge_partner_data,
    generate_course_data, generate_module_data, generate_learner_data,
    generate_learner_education_data
)

def connect_to_mongodb():
    """Connect to MongoDB and create database"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["education_db"]
    return client, db

def create_indexes(db):
    """Create indexes for better query performance"""
    # Country indexes
    db.country.create_index("name", unique=True)
    
    # State indexes
    db.state.create_index("code", unique=True)
    db.state.create_index("country_id")
    
    # District indexes
    db.district.create_index("code", unique=True)
    db.district.create_index("state_id")
    
    # Institution indexes
    db.institution.create_index("aicte_code", unique=True)
    db.institution.create_index("l4g_code", unique=True)
    db.institution.create_index("l4g_group_code", unique=True)
    db.institution.create_index("district_id")
    
    # Degree indexes
    db.degree.create_index("short_name", unique=True)
    
    # Branch indexes
    db.branch.create_index("degree_id")
    
    # Department indexes
    db.department.create_index("name", unique=True)
    
    # Designation indexes
    db.designation.create_index("name", unique=True)
    
    # Knowledge Partner indexes
    db.knowledge_partner.create_index("name", unique=True)
    
    # Course indexes
    db.course.create_index("knowledge_partner_id")
    
    # Module indexes
    db.module.create_index("course_id")
    
    # Learner indexes
    db.learner.create_index("email", unique=True)
    db.learner.create_index("aadhaar_number", unique=True)
    
    # Learner Education indexes
    db.learner_education.create_index([("learner_id", 1), ("institution_id", 1)])
    db.learner_education.create_index("branch_id")

def insert_data(db):
    """Generate and insert synthetic data into MongoDB collections"""
    # Generate data
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

    # Insert Countries
    countries = country_df.to_dict('records')
    db.country.insert_many(countries)
    print(f"Inserted {len(countries)} countries")

    # Insert States (with country reference)
    states = state_df.to_dict('records')
    for state in states:
        state['country_id'] = state.pop('country_code')  # Rename for MongoDB convention
    db.state.insert_many(states)
    print(f"Inserted {len(states)} states")

    # Insert Districts (with state reference)
    districts = district_df.to_dict('records')
    for district in districts:
        district['state_id'] = district.pop('state_code')
    db.district.insert_many(districts)
    print(f"Inserted {len(districts)} districts")

    # Insert Institutions (with district reference)
    institutions = institution_df.to_dict('records')
    for institution in institutions:
        institution['district_id'] = institution.pop('district_code')
    db.institution.insert_many(institutions)
    print(f"Inserted {len(institutions)} institutions")

    # Insert Degrees
    degrees = degree_df.to_dict('records')
    db.degree.insert_many(degrees)
    print(f"Inserted {len(degrees)} degrees")

    # Insert Branches (with degree reference)
    branches = branch_df.to_dict('records')
    for branch in branches:
        branch['degree_id'] = branch.pop('degree_code')
    db.branch.insert_many(branches)
    print(f"Inserted {len(branches)} branches")

    # Insert Departments
    departments = department_df.to_dict('records')
    db.department.insert_many(departments)
    print(f"Inserted {len(departments)} departments")

    # Insert Designations
    designations = designation_df.to_dict('records')
    db.designation.insert_many(designations)
    print(f"Inserted {len(designations)} designations")

    # Insert Knowledge Partners
    knowledge_partners = knowledge_partner_df.to_dict('records')
    db.knowledge_partner.insert_many(knowledge_partners)
    print(f"Inserted {len(knowledge_partners)} knowledge partners")

    # Insert Courses (with knowledge partner reference)
    courses = course_df.to_dict('records')
    for course in courses:
        course['knowledge_partner_id'] = course.pop('knowledge_partner_code')
    db.course.insert_many(courses)
    print(f"Inserted {len(courses)} courses")

    # Insert Modules (with course reference)
    modules = module_df.to_dict('records')
    for module in modules:
        module['course_id'] = module.pop('course_code')
    db.module.insert_many(modules)
    print(f"Inserted {len(modules)} modules")

    # Insert Learners
    learners = learner_df.to_dict('records')
    db.learner.insert_many(learners)
    print(f"Inserted {len(learners)} learners")

    # Insert Learner Education records (with references)
    learner_educations = learner_education_df.to_dict('records')
    for edu in learner_educations:
        edu['learner_id'] = edu.pop('learner_code')
        edu['institution_id'] = edu.pop('institution_code')
        edu['branch_id'] = edu.pop('branch_code')
    db.learner_education.insert_many(learner_educations)
    print(f"Inserted {len(learner_educations)} learner education records")

def main():
    # Connect to MongoDB
    client, db = connect_to_mongodb()
    
    try:
        # Drop existing collections if they exist
        for collection in db.list_collection_names():
            db[collection].drop()
        
        # Insert all data
        insert_data(db)
        
        # Create indexes
        create_indexes(db)
        
        print("\nDatabase creation completed successfully!")
        print("Database name: education_db")
        print("Collections created:")
        for collection in db.list_collection_names():
            print(f"- {collection}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    main() 