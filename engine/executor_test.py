from executor import SQLExecutor

def main():
    """Test SQLExecutor functionality"""
    executor = SQLExecutor()

    test_query = """
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
        """
    # test_query = "DELETE FROM Institution WHERE id = 1;"

    print(f"Executing Query:\n{test_query}")
    
    success, results, formatted_results, error = executor.main_executor(test_query)
    
    if success:
        print(f"\nSuccess! Found {len(results)} rows")
        print("\nFormatted Results:")
        print(formatted_results)
        print("\nRaw Results:")
        print(results)
    else:
        print(f"\nFailed: {error}")

if __name__ == "__main__":
    main() 