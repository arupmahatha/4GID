from refiner import refine_sql

def main():
    """Test SQL refinement functionality"""
    
    # Test SQL query
    sql_query = """
    SELECT
        Learner.name AS Student_Name,
        Institution.name AS Institute_Name,
        Degree.short_name AS Program_Short_Name,
        Specialization.info AS Specialized_In,
        AVG(Module.theory_practical) AS Average_Theory_Practical_Ratio,
        COUNT(Learner_Program_Requirement.id) AS Number_Of_Requirements_Met,
        AVG(Module.duration_minutes) AS Average_Duration,
        GROUP_CONCAT(Department.name SEPARATOR ', ') AS Departments,
        Learner_Education.year_of_graduation - Learner_Education.year_of_joining AS Years_Of_Study,
        Learner_Employment.year_of_joining - Learner_Education.year_of_graduation AS Years_Of_Experience
    FROM
        Learner
        JOIN Learner_Education ON Learner.id = Learner_Education.learner_code
        JOIN Institution ON Learner_Education.institution_code = Institution.id
        JOIN Branch ON Learner_Education.branch_code = Branch.id
        JOIN Degree ON Branch.degree_code = Degree.id
        JOIN Specialization ON Degree.id = Specialization.degree_code
        JOIN Module ON Specialization_Course.course_code = Module.id
        LEFT JOIN Learner_Employment ON Learner.id = Learner_Employment.learner_code
        JOIN Department ON Institution.district_code = District.code AND Institution.state_code = State.code AND Institution.country_code = Country.code AND Institution.type = Department.type
    GROUP BY
        Learner.id,
        Institution.id,
        Degree.id,
        Specialization.id,
        Departments
    ORDER BY
        Number_Of_Requirements_Met DESC, Average_Theory_Practical_Ratio DESC, Years_Of_Study ASC, Years_Of_Experience ASC;
    """
    
    print("\n=== Testing SQL Refinement ===")
    print(f"\nInput SQL: '{sql_query}'")
    
    try:
        # Refine SQL
        print("\nRefining SQL...")
        results = refine_sql(sql_query)
        
        print("\nExtracted Entities:")
        for entity in results['extracted_entities']:
            print(f"Table: {entity['table']}")
            print(f"Column: {entity['column']}")
            print(f"Value: {entity['value']}")
            print("---")
        
        print("\nValue Mappings:")
        if results['value_mappings']:
            for mapping in results['value_mappings']:
                print(f"Original: '{mapping['original_value']}'")
                print(f"Matched: '{mapping['matched_value']}'")
                print(f"Score: {mapping['score']}")
                print("---")
        else:
            print("No value mappings needed")
        
        print("\nRefined SQL:")
        print(results['refined_sql'])
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 