from dataclasses import dataclass
from typing import List, Set, Dict, Optional

@dataclass
class Column:
    name: str
    type: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    references: Optional[str] = None
    choices: Optional[List[str]] = None
    max_length: Optional[int] = None
    null: bool = False
    blank: bool = False
    unique: bool = False
    default: Optional[str] = None

@dataclass
class Relationship:
    from_table: str
    to_table: str
    type: str  # OneToOne, OneToMany, ManyToMany
    description: str

# Create your choices here
TYPE_CHOICES = [('academic', 'academic'), ('corporate', 'corporate'), ('government', 'government')]
GENDER_CHOICES = [('M', 'male'), ('F', 'female'), ('O', 'other')]
MODULE_TYPE_CHOICES = [('T', 'theory'), ('P', 'practical')]
INSTITUTION_TYPE_CHOICES = [
    'Public University',
    'Private University-State',
    'Private University-Deemed to be',
    'Autonomous College',
    'Affiliated College',
    'Unknown'
]

class SchemaMetadata:
    def __init__(self):
        self.tables = {
            "Country": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=30, default='', unique=True)
            ],
            
            "State": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=30, default=''),
                Column("code", "str", max_length=15, default='', unique=True),
                Column("country_code", "int", is_foreign_key=True, references="Country.id")
            ],
            
            "District": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=30, default=''),
                Column("code", "str", max_length=15, default='', unique=True),
                Column("state_code", "int", is_foreign_key=True, references="State.id")
            ],
            
            "Institution": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=255, default=''),
                Column("short_name", "str", max_length=30, null=True, blank=True),
                Column("aicte_code", "str", max_length=15, unique=True, null=True, blank=True),
                Column("eamcet_code", "str", max_length=15, null=True, blank=True),
                Column("l4g_code", "str", max_length=9, default='', unique=True),
                Column("l4g_group_code", "str", max_length=6, null=True, blank=True, unique=True),
                Column("type", "str", choices=INSTITUTION_TYPE_CHOICES),
                Column("address", "str", max_length=255, null=True, blank=True),
                Column("website", "str", max_length=255, null=True, blank=True),
                Column("latlong", "str", max_length=60, null=True, blank=True),
                Column("district_code", "int", is_foreign_key=True, references="District.id")
            ],
            
            "Degree": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=90, default='', unique=True),
                Column("short_name", "str", max_length=15, default='', unique=True)
            ],
            
            "Branch": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=150, default=''),
                Column("short_name", "str", max_length=9, default=''),
                Column("degree_code", "int", is_foreign_key=True, references="Degree.id")
            ],
            
            "Department": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=90, default='', unique=True),
                Column("type", "str", choices=TYPE_CHOICES, default='academic')
            ],
            
            "Designation": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=90, default='', unique=True),
                Column("type", "str", choices=TYPE_CHOICES, default='academic'),
                Column("priority", "int", default='0')
            ],
            
            "Knowledge_Partner": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=90, default='', unique=True),
                Column("address", "str", max_length=255, null=True, blank=True),
                Column("website", "str", max_length=60, null=True, blank=True),
                Column("info", "str", max_length=255, null=True, blank=True)
            ],
            
            "Course": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=150, default=''),
                Column("info", "str", null=True, blank=True),
                Column("knowledge_partner_code", "int", is_foreign_key=True, references="Knowledge_Partner.id")
            ],
            
            "Module": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=150, default=''),
                Column("info", "str", null=True, blank=True),
                Column("module_sequence_number", "int", default='0'),
                Column("theory_practical", "str", choices=MODULE_TYPE_CHOICES, default='T'),
                Column("duration_minutes", "int", default='0'),
                Column("course_code", "int", is_foreign_key=True, references="Course.id")
            ],
            
            "Specialization": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=150, default=''),
                Column("info", "str", max_length=255, null=True, blank=True),
                Column("knowledge_partner_code", "int", is_foreign_key=True, references="Knowledge_Partner.id")
            ],
            
            "Specialization_Course": [
                Column("id", "int", is_primary_key=True),
                Column("course_sequence_number", "int", default='0'),
                Column("course_code", "int", is_foreign_key=True, references="Course.id"),
                Column("specialization_code", "int", is_foreign_key=True, references="Specialization.id")
            ],
            
            "Program": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=150, default=''),
                Column("info", "str", max_length=255, null=True, blank=True),
                Column("knowledge_partner_code", "int", is_foreign_key=True, references="Knowledge_Partner.id")
            ],
            
            "Program_Specialization": [
                Column("id", "int", is_primary_key=True),
                Column("program_code", "int", is_foreign_key=True, references="Program.id"),
                Column("specialization_code", "int", is_foreign_key=True, references="Specialization.id")
            ],
            
            "Program_Requirement": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=255, default=''),
                Column("is_mandatory", "bool", default='False'),
                Column("program_code", "int", is_foreign_key=True, references="Program.id")
            ],
            
            "Learner": [
                Column("id", "int", is_primary_key=True),
                Column("name", "str", max_length=60, default=''),
                Column("email", "str", unique=True, default=''),
                Column("mobile", "str", max_length=15, default=''),
                Column("gender", "str", choices=GENDER_CHOICES, default='O', max_length=1),
                Column("date_of_birth", "date", null=True, blank=True),
                Column("aadhaar_number", "int", null=True, blank=True)
            ],
            
            "Learner_Education": [
                Column("id", "int", is_primary_key=True),
                Column("rollno", "str", max_length=50, null=True, blank=True),
                Column("year_of_joining", "int", default='0'),
                Column("year_of_graduation", "int", default='0'),
                Column("learner_code", "int", is_foreign_key=True, references="Learner.id"),
                Column("institution_code", "int", is_foreign_key=True, references="Institution.id"),
                Column("branch_code", "int", is_foreign_key=True, references="Branch.id")
            ],
            
            "Learner_Employment": [
                Column("id", "int", is_primary_key=True),
                Column("empid", "str", max_length=30, default=''),
                Column("year_of_joining", "int", default='0'),
                Column("learner_code", "int", is_foreign_key=True, references="Learner.id"),
                Column("institution_code", "int", is_foreign_key=True, references="Institution.id"),
                Column("department_code", "int", is_foreign_key=True, references="Department.id"),
                Column("designation_code", "int", is_foreign_key=True, references="Designation.id")
            ],
            
            "Learner_Program_Requirement": [
                Column("id", "int", is_primary_key=True),
                Column("learner_code", "int", is_foreign_key=True, references="Learner.id"),
                Column("program_requirement_code", "int", is_foreign_key=True, references="Program_Requirement.id"),
                Column("value", "str", max_length=255, null=True, blank=True)
            ]
        }
        # Generate relationships from column references
        self._generate_relationships()

    def _generate_relationships(self):
        """Generate relationships based on foreign key references and many-to-many relationships"""
        self.relationships = []
        
        # Track many-to-many relationships from Django model definitions
        many_to_many = {
            "Specialization": {
                "courses": ("Course", "Specialization_Course")
            },
            "Program": {
                "specializations": ("Specialization", "Program_Specialization")
            }
        }
        
        # First handle foreign key relationships
        for table_name, columns in self.tables.items():
            for column in columns:
                if column.is_foreign_key and column.references:
                    ref_table, ref_column = column.references.split('.')
                    
                    # Add ManyToOne relationship
                    self.relationships.append(
                        Relationship(
                            from_table=table_name,
                            to_table=ref_table,
                            type="ManyToOne",
                            description=f"{table_name} belongs to {ref_table}"
                        )
                    )
                    
                    # Add reverse OneToMany relationship
                    self.relationships.append(
                        Relationship(
                            from_table=ref_table,
                            to_table=table_name,
                            type="OneToMany",
                            description=f"{ref_table} has many {table_name}"
                        )
                    )
        
        # Then handle many-to-many relationships
        for model, m2m_fields in many_to_many.items():
            for field_name, (related_model, through_model) in m2m_fields.items():
                self.relationships.append(
                    Relationship(
                        from_table=model,
                        to_table=related_model,
                        type="ManyToMany",
                        description=f"{model} has and belongs to many {related_model} through {through_model}"
                    )
                )

    def get_relationships_for_table(self, table_name: str) -> List[Relationship]:
        """Get all relationships where the given table is involved"""
        return [r for r in self.relationships if r.from_table == table_name or r.to_table == table_name]

    def get_related_tables(self, table_name: str) -> Set[str]:
        """Get all tables that are related to the given table"""
        related = set()
        for rel in self.relationships:
            if rel.from_table == table_name:
                related.add(rel.to_table)
            elif rel.to_table == table_name:
                related.add(rel.from_table)
        return related

    def get_table_columns(self, table_name: str) -> List[Column]:
        """Get all columns for a given table"""
        return self.tables.get(table_name, [])

    def get_table_info(self, table_name: str) -> Dict:
        """Get comprehensive information about a table including its columns and relationships"""
        columns = self.get_table_columns(table_name)
        relationships = self.get_relationships_for_table(table_name)
        related_tables = self.get_related_tables(table_name)
        
        return {
            "name": table_name,
            "columns": columns,
            "relationships": relationships,
            "related_tables": related_tables
        }