# Module 3 Lab

This lab contains some exercises that will allow you to explore working with a sqlite database.

To work on this lab check it out to a machine that has `sqlite3`, either your local machine or the CS lab machines.

Once you have checked out the lab, from the directory that has this README.md file and legislators.db, run the following command:

    sqlite3 legislators.db

This will open the sqlite3 shell and you will be able to run SQL commands against the database.

    sqlite3> .tables
    legislators    other_identifiers    roles

    sqlite3> .schema legislators
    CREATE TABLE legislators (
        bioguide_id VARCHAR PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        birthday DATE NOT NULL,
        gender VARCHAR NOT NULL,
        current_chamber VARCHAR NOT NULL,
        current_state VARCHAR NOT NULL,
        current_district INTEGER,
        current_party VARCHAR NOT NULL
        ); 

## Part 1 - Basic Queries

1. Write a query that returns the first name, last name, and birthday of all legislators currently serving in Illinois.

```sql
SELECT first_name, last_name, birthday FROM legislators WHERE current_state = 'IL';
```

2. Write queries to find the oldest and youngest legislators currently serving.

```sql
SELECT first_name, last_name, birthday FROM legislators ORDER BY birthday ASC LIMIT 1;
SELECT first_name, last_name, birthday FROM legislators ORDER BY birthday DESC LIMIT 1;
```

3. Write a query that returns all legislators that have a last name that starts with the same letter as your own.  (Hint: use the `LIKE` operator)

```sql
SELECT first_name, last_name FROM legislators WHERE last_name LIKE 'T%';
```

## Part 2 - Aggregation

1. Write a query that returns the total number of legislators currently serving in the House.  (Hint: current_chamber is either "rep" or "sen")

```sql
SELECT COUNT(*) FROM legislators WHERE current_chamber = 'rep';
```

(Why 440?  Because there are 435 representatives and 5 delegates.)

2. Write a query that lists the top 10 states by number of legislators currently serving in the House.

```sql
SELECT current_state, COUNT(*) FROM legislators WHERE current_chamber = 'rep' GROUP BY current_state ORDER BY COUNT(*) DESC LIMIT 10;
```

3. Modify the above query to list how many legislators are currently serving in the House in each state but only for states that have more than 10 legislators currently serving in the House.

(Hint: this is a good place to use the `HAVING` clause)

```sql
SELECT current_state, COUNT(*) FROM legislators WHERE current_chamber = 'rep' GROUP BY current_state HAVING COUNT(*) > 10 ORDER BY COUNT(*) DESC;
```

4. Write a query that returns the average age of legislators currently serving in the House.

```sql
SELECT AVG(strftime('%Y', 'now') - strftime('%Y', birthday)) FROM legislators WHERE current_chamber = 'rep';
```

(If you solved this one, good job!  Learning to read documentation is an important skill, we didn't cover this function in class.)

5. Write a query that returns the average age of legislators currently serving in the House by state.

```sql
SELECT current_state, AVG(strftime('%Y', 'now') - strftime('%Y', birthday)) FROM legislators WHERE current_chamber = 'rep' GROUP BY current_state;
```

## Part 3 - Joining Tables

The `roles` table contains information about the roles that legislators have served in the past.

Take a look at this table's schema:

    sqlite3> .schema roles
    CREATE TABLE roles (
        bioguide_id VARCHAR NOT NULL,
        chamber VARCHAR NOT NULL,
        state VARCHAR NOT NULL,
        district INTEGER,
        party VARCHAR NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        FOREIGN KEY (bioguide_id) REFERENCES legislators (bioguide_id)
        );

1. First, just using the `roles` table, write a query to find the top 10 house seats that have had the most different people serve in them.  (Note: our data does not include all historical data, so this is not an accurate picture.)

Hint: What field(s) would you GROUP BY to get the answer you want?

```sql
SELECT state, district, COUNT(*) FROM roles WHERE chamber = 'rep' GROUP BY state, district ORDER BY COUNT(*) DESC LIMIT 10;
```

We can group by multiple fields to get the answer we want.

2. Write a query that finds the name of the legislator with the earliest recorded role in the house.

```sql
SELECT first_name, last_name, start_date FROM legislators JOIN roles ON legislators.bioguide_id = roles.bioguide_id WHERE chamber = 'rep' ORDER BY start_date ASC LIMIT 1;
```

Chuck Grassley has been in Congress since 1975.

3. Write a query that finds the names of legislators that are currently serving in the Senate which have served in the House in the past.

(It is OK for your results to contain duplicates, you can experiment with changing SELECT to SELECT DISTINCT to eliminate them if you'd like.)

```sql
SELECT DISTINCT first_name, last_name FROM legislators JOIN roles ON legislators.bioguide_id = roles.bioguide_id WHERE chamber = 'rep' AND current_chamber = 'sen';
```

Without the DISTINCT, you'll get multiple rows for each legislator since they have multiple entries in the `roles` table.

4. Write a query that returns the legislator that has the most "role" entries in the database.

## Part 4 - Using sqlite3 from Python

1. Write a Python script that uses the sqlite3 module to connect to the database and execute the query from Part 1, Question 1.

```python
import sqlite3

conn = sqlite3.connect('legislators.db')
c = conn.cursor()
c.execute('SELECT first_name, last_name, birthday FROM legislators WHERE current_state = "IL"')
print(c.fetchall())
```

2. Write a Python script that prompts a user for a state and prints out the details of all legislators currently serving in that state.

Be sure to consider injection attacks when writing your script.

```python
import sqlite3

conn = sqlite3.connect('legislators.db')
c = conn.cursor()
state = input('Enter a state: ')
c.execute('SELECT first_name, last_name, birthday FROM legislators WHERE current_state = ?', (state,))
print(c.fetchall())
```

## Further Exploration

Everything beyond here is more advanced than most will need for 30122 but if you're already familiar with SQL might be interesting to you.

Take a look at the `other_identifiers` table.  This table contains other identifiers for legislators that are not bioguide_ids.

    sqlite3> .schema other_identifiers
    CREATE TABLE other_identifiers (
        bioguide_id VARCHAR NOT NULL,
        type VARCHAR NOT NULL,
        value VARCHAR NOT NULL,
        FOREIGN KEY(bioguide_id) REFERENCES legislators(bioguide_id)
        );

When we have data that'd naturally fit into a list (like `roles`), we can use a separate table to store that data.

The other_identifiers table in some ways resembles a Python dictionary in its usage.  It allows us to associate somewhat arbitrary key-value pairs (in this case identifier_type and identifier_value) with a legislator.

1. Write a query that obtains the details for the legislator with the fec ID H2VT01076.

```sql
SELECT first_name, last_name FROM legislators JOIN other_identifiers ON legislators.bioguide_id = other_identifiers.bioguide_id WHERE type = 'fec' AND value = 'H2VT01076';
```

2. Use SELECT DISTINCT to find all the different identifier types in the other_identifiers table.

```sql
SELECT DISTINCT type FROM other_identifiers;
```

3. Write a Python script that prompts the user for a legislator's name and then prints out basic information and the identifiers for that legislator in a neat table:

    Name: Alexandria Ocasio-Cortez
    Office: NY-14
    FEC ID: H8NY15148
    Open Secrets ID: N00041162
    ICPSR: 21949
    ...

While it may be tempting to make two or more queries, can you do this with one SQL query?

```python
import sqlite3

conn = sqlite3.connect('legislators.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
name = "Ocasio-Cortez"
c.execute('SELECT first_name, last_name, current_state, current_district, type, value FROM legislators JOIN other_identifiers ON legislators.bioguide_id = other_identifiers.bioguide_id WHERE last_name = ?', (name,))
rows = c.fetchall()
for row in rows:
    print('Name: {} {}'.format(row['first_name'], row['last_name']))
    print('Office: {}-{}'.format(row['current_state'], row['current_district']))
    print('{}: {}'.format(row['type'], row['value']))
```
