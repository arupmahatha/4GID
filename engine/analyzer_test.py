from analyzer import SQLAnalyzer

def main():
    """Test SQLAnalyzer functionality"""
    analyzer = SQLAnalyzer()

    # Test query for educational program effectiveness
    test_query = "Evaluate the effectiveness of educational programs based on multiple metrics."
    
    # Test data - educational program metrics
    test_results = [{'program_name': 'Program 10', 'num_specializations': 3, 'num_courses': 5, 'enrolled_learners': 16, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 16.16}, {'program_name': 'Program 1', 'num_specializations': 2, 'num_courses': 1, 'enrolled_learners': 15, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 15.15}, {'program_name': 'Program 6', 'num_specializations': 2, 'num_courses': 0, 'enrolled_learners': 12, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 12.12}, {'program_name': 'Program 8', 'num_specializations': 0, 'num_courses': 0, 'enrolled_learners': 10, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 10.1}, {'program_name': 'Program 4', 'num_specializations': 1, 'num_courses': 2, 'enrolled_learners': 9, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 9.09}, {'program_name': 'Program 5', 'num_specializations': 0, 'num_courses': 0, 'enrolled_learners': 9, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 9.09}, {'program_name': 'Program 3', 'num_specializations': 0, 'num_courses': 0, 'enrolled_learners': 8, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 8.08}, {'program_name': 'Program 9', 'num_specializations': 0, 'num_courses': 0, 'enrolled_learners': 8, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 8.08}, {'program_name': 'Program 2', 'num_specializations': 0, 'num_courses': 0, 'enrolled_learners': 7, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 7.07}, {'program_name': 'Program 7', 'num_specializations': 1, 'num_courses': 0, 'enrolled_learners': 5, 'avg_years_to_complete': 4.0, 'enrollment_percentage': 5.05}]
    
    # Test analysis
    analysis_results = analyzer.main_analyzer(test_query, test_results)
    
    print("\nAnalysis Results:")
    if analysis_results['success']:
        print(f"Query: {analysis_results['query_info']}")
        print(f"Record count: {analysis_results['record_count']}")
        print(f"\nSuccess: {analysis_results['success']}")
        print("\nAnalysis:")
        print(analysis_results['analysis'])
    else:
        print(f"Analysis failed: {analysis_results['error']}")

if __name__ == "__main__":
    main() 