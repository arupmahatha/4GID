from refiner import SQLRefiner

def main():
    """Test SQL refinement functionality"""
    refiner = SQLRefiner()
    
    # Test SQL query
    sql_query = """WITH ProgramMetrics AS (
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
ORDER BY enrolled_learners DESC;"""

    # sql_query = """SELECT * FROM Learner WHERE name = 'John Handcock';"""
    
    print(f"\nInput SQL: '{sql_query}'")
    
    try:
        # Refine SQL
        print("\nRefining SQL...")
        results = refiner.main_refiner(sql_query)
        
        print("\nExtracted Entities:")
        if results['extracted_entities']:
            for entity in results['extracted_entities']:
                print(f"Table: {entity['table']}")
                print(f"Column: {entity['column']}")
                print(f"Value: {entity['value']}")
                print("---")
        else:
            print("No entities were extracted from the SQL query")
        
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
        if results['refined_sql'] != results['original_sql']:
            print("SQL was refined to:")
            print(results['refined_sql'])
        else:
            print("No refinements were needed. Using original SQL.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 