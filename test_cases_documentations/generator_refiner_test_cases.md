# SQL Test Cases for Generator and Refiner
This document contains test cases that demonstrate the pipeline of generating SQL from natural language queries and then refining those SQL queries to handle real-world entity matching.


## Test Case 1: Learner Name Search

   ### Natural Language Query (for generator.py)
   ```
   Find all information about a learner named John Handcock
   ```

   ### Generated SQL (for refiner.py)
   ```sql
   SELECT * FROM Learner WHERE name = 'John Handcock';
   ```

   ### Expected Refinement
   The refiner should match "John Handcock" to "John Hancock" in the database.


## Test Case 2: Email Domain Search

   ### Natural Language Query (for generator.py)
   ```
   Show me the names and email addresses of all learners who use example.ord as their email domain
   ```

   ### Generated SQL (for refiner.py)
   ```sql
   SELECT name, email FROM Learner WHERE email LIKE '%example.ord%';
   ```

   ### Expected Refinement
   The refiner should correct the domain from "example.ord" to "example.org".


## Test Case 3: Course Name Search

   ### Natural Language Query (for generator.py)
   ```
   Find all details about courses related to Web Developement
   ```

   ### Generated SQL (for refiner.py)
   ```sql
   SELECT * FROM Course WHERE name LIKE '%Web Developement%';
   ```

   ### Expected Refinement
   The refiner should correct "Developement" to "Development" and match with "Introduction to Web Development".


## Test Case 4: Multiple Conditions Search

   ### Natural Language Query (for generator.py)
   ```
   Find the name and email of a learner named David Gardner or who has the email allisonthomson@example.com
   ```

   ### Generated SQL (for refiner.py)
   ```sql
   SELECT l.name, l.email 
   FROM Learner l 
   WHERE l.name = 'David Gardner' 
   OR l.email = 'allisonthomson@example.com';
   ```

   ### Expected Refinement
   The refiner should:
   - Correct "Gardner" to "Garner"
   - Correct "thomson" to "thompson" in the email


## Test Case 5: Course Description Search

   ### Natural Language Query (for generator.py)
   ```
   Find courses that mention Developement or programing in their descriptions
   ```

   ### Generated SQL (for refiner.py)
   ```sql
   SELECT name, description 
   FROM Course 
   WHERE description LIKE '%Developement%' 
   OR description LIKE '%programing%';
   ```

   ### Expected Refinement
   The refiner should correct:
   - "Developement" to "Development"
   - "programing" to "programming"