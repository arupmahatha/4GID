from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ColumnDefinition:
    description: str
    distinct_values: List[str] = None

    def __post_init__(self):
        if self.distinct_values is None:
            self.distinct_values = []

class TableDefinition:
    def __init__(self, description: str, key_purposes: List[str], 
                 common_queries: List[str], relationships: Dict[str, str], 
                 columns: Dict[str, ColumnDefinition] = None):
        self.description = description
        self.key_purposes = key_purposes
        self.common_queries = common_queries
        self.relationships = relationships
        self.columns = columns or {}

class LearningAnalyticsMetadata:
    def __init__(self):
        self.tables = {
            "student_performance": TableDefinition(
                description="Tracks student performance across courses and learning metrics",
                key_purposes=[
                    "Monitor student progress",
                    "Identify learning gaps",
                    "Predict student success"
                ],
                common_queries=[
                    "Performance by course",
                    "Learning engagement analysis",
                    "Student skill development tracking"
                ],
                relationships={
                    "course_catalog": "Performance linked to course details",
                    "student_profile": "Individual student progress tracking"
                },
                columns={
                    "Student_ID": ColumnDefinition(
                        description="Unique identifier for each student",
                        distinct_values=[]
                    ),
                    "Course_Name": ColumnDefinition(
                        description="Name of the course taken by the student",
                        distinct_values=[
                            "Introduction to Python", 
                            "Data Science Fundamentals", 
                            "Machine Learning Basics", 
                            "Web Development Bootcamp"
                        ]
                    ),
                    "Performance_Metric": ColumnDefinition(
                        description="Quantitative measure of student performance",
                        distinct_values=[
                            "Quiz Score", 
                            "Assignment Grade", 
                            "Final Exam Score", 
                            "Course Completion Rate"
                        ]
                    ),
                    "Learning_Progress": ColumnDefinition(
                        description="Tracking student's learning journey and skill acquisition",
                        distinct_values=[
                            "Beginner", 
                            "Intermediate", 
                            "Advanced", 
                            "Expert"
                        ]
                    ),
                    "Engagement_Level": ColumnDefinition(
                        description="Measure of student interaction and participation",
                        distinct_values=[
                            "Low", 
                            "Medium", 
                            "High", 
                            "Very High"
                        ]
                    )
                }
            )
        }

    def get_table_info(self, table_name):
        return self.tables.get(table_name)

    def get_column_info(self, table_name, column_name):
        table = self.tables.get(table_name)
        if table:
            return table.columns.get(column_name)
        return None