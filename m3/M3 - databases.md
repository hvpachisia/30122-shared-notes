# Module 3: Storing Data

## Motivation

We've now seen formats like JSON, CSV, and XML for storing data on disk.

Imagine building an application that was getting continuous data updates:

```python
def add_new_transaction(user_id, date, amount, note):
    # In this fictional example, imagine we're storing data in a JSON object
    # . {"user_id": 12345,
    #    "balance": 7500.12,
    #    "transactions": [
    #       {"amount": 100, "note": "deposit", "date": "2023-01-01"},
    #       {"amount": -70, "note": "comcast", "date": "2023-01-11"},
    #    ]
    #    }

    # load data from disk
    with open("transactions.json") as f:
        data = json.load(f)
    
    # search for user
    for user_rec in data:
        if user_rec["user_id"] == user_id:
            user = data["user_id"]
            break
    
    # update user
    user["transactions"].append({
        "amount": amount,
        "note": note,
        "date": date,
    })
    user["balance"] += amount

    # save data back out to disk
    with open("transactions.json", "w") as f:
        json.dump(data, f)
```

**What issues exist with the above?**

A database allows us to store data on disk and interact with subsets of it.

Common tasks with data:

* Retrieval of specific records by criteria.
* Update one or more records at once.
* Delete records.

In the simplest case, `sqlite3` for instance, a database can be a single file on disk.  Not all databases work that way though, many times instead of dealing with a local file you would interact with a database over a network.  We'll see later that there is a common interface for interacting with databases that allows you to mostly ignore these differences.

## Relational Databases

Relational databases came about in the 1970s, and are still the most popular type of database.  We'll see why.

The core concepts of a relational database are:

**Tables** - A table is a collection of records of a similar type.  (e.g. students, courses, grades would each be their own table)
    You can think of a table in some ways like a class in Python, in that it represents a distinct composite type.

**Column** - A column is a type of data that all records in a table have.  (e.g. student ID, name, email, etc.)

**Row** - A row is a record in a table. Each row has a value for each column in that table.
    You can think of a row as a single piece of data, so one row per student, course, or grade. This would be the data represented by a single instance of a class in Python, or a dictionary or tuple.

Two other concepts that'll be important later:

**Index** - An index is a way to quickly find a record in a table without having to search through all the records. They can be a single row (e.g. student.id), or a combination of columns (e.g. student.first_name, student.last_name).  Indexes are used to speed up queries, and are a key part of relational databases.

**Foreign Key** - A foreign key is a column in a table that references a column in another table.  This is how you can link records in different tables together.  For example, a student record might have a foreign key to a course record, so you can link a student to a course.

Relational databases are built on a concept called *Relational Algebra*, which defines a series of operations that can be done on data. These operations are the basis for SQL, the language we'll use to interact with relational databases.

**SQL** is a language for interacting with relational databases.  It's a declarative language, meaning that you tell the database what you want, and it figures out how to do it.  SQL is a standard, and there are many different implementations of it with various features.

### Popular Relational Databases

* SQLite - A lightweight database that is stored in a single file. It's the most popular database for small applications, and is used all over the place.  Unlike other databases, it doesn't have a separate server process, it's just a library that you link into your application.  Python includes a built in `sqlite3` library for interacting with SQLite databases.

* PostgreSQL - A full-featured database that is used in many large applications. It's a server process that you can connect to from your application. It has a lot of features that SQLite doesn't, and is a terrific choice for larger applications. It has a robust set of available column types including JSON, arrays, text vectors, and geospatial data types.

* MySQL/MariaDB - Another full-featured database that is used in many large applications, was the most popular for a time but has been overtaken by PostgreSQL in the last few years.

* Oracle / MS SQL Server - Two popular commercial databases, typically only used in larger corporate environments.  Unlike the above, not open source.

### SQL

SQL is a declarative language, quite different from Python.  In Python or similar languages, you tell the computer the steps to perform. In a declarative language like SQL, you tell the database what you want, and it figures out how to do it.

SQL has a few different types of statements:

* **Data Definition Language (DDL)** - Statements that define the structure of the database.  These are used to create tables, add columns, and add indexes.
* **Data Manipulation Language (DML)** - Statements that manipulate the data in the database.  These are used to insert, update, and delete records.
* **Data Query Language (DQL)** - Statements that query the data in the database.  These are used to select records from the database.

We'll mostly be focusing on querying the database today, and a bit of DDL. You'll be learning a lot more SQL next quarter, so don't feel like you need to leave this module a SQL expert.

### SQLite

Invoke `sqlite3` from the command line to start the shell, you can pass it a filename to open a database. Note that if the file doesn't exist, it will be created.  (This can cause issues if you mistype the path, so be mindful of it.)

```sql
$ sqlite3 fec.db
SQLite version 3.37.0 2021-12-09 01:34:53
Enter ".help" for usage hints.
sqlite> 
```

`sqlite>` is the SQLlite prompt, you can type commands there, **be sure to end them with a semicolon**.

#### Dot Commands

SQLite has a few special commands that are not part of the SQL standard, but are very useful.  These are:

* `.tables` - List all the tables in the database
* `.schema <table>` - Show the schema for a table
* `.header on` - Show column names in query results
* `.mode column` - Show query results in columns. This is the default, you can also set mode to `line` or `list` to alter how output is shown.
* `.quit` - Exit the SQLite shell

Note: all of these commands start with a `.`, `.help` will list all of them.

```sql
sqlite> .tables
```

```sql
sqlite> .schema candidate
```

## SELECT Statements

By convention, SQL keywords are written in all caps, and table and column names are written in lowercase.  This is not required, but it's a good convention to follow as it makes queries a bit more readable as you can more easily separate keywords from your table & column names.

To retrieve data from a table, you use a `SELECT` statement.  The basic syntax resembles:

```sql
SELECT <columns> FROM <table> [WHERE <condition>] [LIMIT <count>];
```

(Actually, a lot more than this <https://www.sqlite.org/syntaxdiagrams.html#select-stmt>)

The square brackets are a convention often used in documentation to indicate that something is optional.
As we'll see, the `WHERE` and `LIMIT` clauses are optional, and there are quite a few others that exist as well.

### SELECT *

The `*` character is a wildcard that can be used in place of a list of columns.  It means "all columns".  So the following two queries are equivalent:

```sql
SELECT * FROM candidate;
SELECT committee_id, lastname, firstname, party, city, state, zip, cand_id, district FROM candidate;
```

```sql
SELECT * FROM candidate;
```

### Operators

SQL has many operators that can be used in the `WHERE` clause:

* `=` - Equal to
* `<>` - Not equal to
* `>` - Greater than
* `<` - Less than
* `>=` - Greater than or equal to
* `<=` - Less than or equal to
* `LIKE` - Matches a pattern.  The pattern can contain the `%` character, which matches any number of characters.  The `_` character matches a single character.  The pattern is case insensitive.
* `IN` - Matches any of a list of values.  For example, `WHERE party IN ('REP', 'DEM')` would match any record where the party is either `REP` or `DEM`.
* AND - Logical AND.  For example, `WHERE party = 'REP' AND state = 'CA'` would match any record where the party is `REP` and the state is `CA`.
* OR - Logical OR.  For example, `WHERE party = 'REP' OR party = 'DEM'` would match any record where the party is either `REP` or `DEM`.

```sql
SELECT lastname, firstname FROM candidate WHERE party = 'REP';
```

```sql
SELECT lastname, firstname FROM candidate WHERE lastname > 'Z';
```

### Column Names

Can of course specify a list of columns to return:

```sql
SELECT lastname, firstname, party FROM candidate;
```

### LIMIT

That's a lot of candidates, let's limit the results to 5:

```sql
SELECT lastname, firstname, party FROM candidate LIMIT 5;
```

(You can also use `LIMIT <offset>, <count>` to skip the first `<offset>` rows, and return `<count>` rows after that.)

### WHERE

The `WHERE` clause is used to filter the results of a query.  It's a condition that must be true for a record to be returned.

```sql
SELECT lastname, firstname, party FROM candidate WHERE party = 'REP';
```

### Functions & Aliases

You can use functions in the `SELECT` clause to transform the data.

* `COUNT` - Returns the number of rows in the result set
* `SUM` - Returns the sum of the values in a column
* `AVG` - Returns the average of the values in a column
* `MIN` - Returns the minimum value in a column
* `MAX` - Returns the maximum value in a column

The most common function is `COUNT`, which returns the number of rows in the result set.

```sql
SELECT COUNT(*) FROM candidate WHERE party = 'REP';
```

The resulting column name will be the function name (e.g. `count`), so you can use an `AS` clause to give it a more meaningful name.

```sql
SELECT COUNT(*) AS rep_count FROM candidate WHERE party = 'REP';
```

### GROUP BY

The `GROUP BY` clause is used for aggregating multiple rows into a single row. It's often used with aggregate functions like `COUNT` and `SUM`.

```sql
SELECT party, COUNT(*) AS count FROM candidate GROUP BY party;
```

### ORDER BY

The `ORDER BY` clause is used to sort the results of a query.  By default, the results are sorted in ascending order.  To sort in descending order, use `DESC` after the column name.  You can sort by column name, or by the result of a function by refering to its alias.

```sql
SELECT party, COUNT(*) AS count FROM candidate GROUP BY party ORDER BY count DESC;
```

We can combine these clauses to get the top 5 parties by number of candidates:

```sql
SELECT party, COUNT(*) AS count FROM candidate GROUP BY party ORDER BY count DESC LIMIT 5;
```

### HAVING

The `HAVING` clause is used to filter the results of a `GROUP BY` query.  It's similar to the `WHERE` clause, but it's used to filter the results of a `GROUP BY` query.

```sql
SELECT party, COUNT(*) AS count FROM candidate GROUP BY party HAVING count > 50 ORDER BY count DESC;
```

### Demo: Run Some Queries on Contribution

1) Total amount of contributions made by residents of each state.
2) Which state made the most contributions?
3) Min contribution , reveals issue w/ -1 in amount

## Joins

What if we have two tables and we want to query data across both of them?

**Employee**

| id | salary |
| --- | --- |
| 1 | 100000 |
| 2 | 85000 |
| 4 | 120000 |

**Paychecks**

| check_id | employee_id | amount |
| --- | --- | --- |
| 1001 | 1 | 8333.33 |
| 1002 | 2 | 7083.33 |
| 1003 | 4 | 10000.00 |
| 1004 | 1 | 8333.33 |

If we add both columns to the SELECT statement, we get:

| id | salary | check_id | employee_id | amount |
| --- | --- | --- | --- | --- |
| 1 | 100000 | 1001 | 1 | 8333.33 |
| 1 | 100000 | 1002 | 2 | 7083.33 |
| 1 | 100000 | 1003 | 4 | 10000.00 |
| 1 | 100000 | 1004 | 1 | 8333.33 |
| 2 | 85000 | 1001 | 1 | 8333.33 |
| 2 | 85000 | 1002 | 2 | 7083.33 |
| 2 | 85000 | 1003 | 4 | 10000.00 |
| 2 | 85000 | 1004 | 1 | 8333.33 |
| 4 | 120000 | 1001 | 1 | 8333.33 |
| 4 | 120000 | 1002 | 2 | 7083.33 |
| 4 | 120000 | 1003 | 4 | 10000.00 |
| 4 | 120000 | 1004 | 1 | 8333.33 |

This is the **cross product** of the two tables.  It's the result of multiplying the number of rows in each table.  It's not very useful.

### Inner Join

The `JOIN` keyword is used to compute the intersection of two tables along some criteria.  This depends on them having a common column or columns.

```sql
> SELECT * FROM employee JOIN paycheck ON employee.id = paycheck.employee_id;
```

| id | salary | check_id | employee_id | amount |
| --- | --- | --- | --- | --- |
| 1 | 100000 | 1001 | 1 | 8333.33 |
| 1 | 100000 | 1004 | 1 | 8333.33 |
| 2 | 85000 | 1002 | 2 | 7083.33 |
| 4 | 120000 | 1003 | 4 | 10000.00 |

It is common in practice for column names to overlap in tables.  If you need to disambiguate, you can refer to columns like we did above `table.column` (e.g. `employee.id`), you can also use the `AS` keyword to rename tables & columns.

```
> SELECT e.id, e.salary, p.check_id, p.amount FROM employee AS e JOIN paycheck AS p ON e.id = p.id;
```

| id | salary | check_id | amount |
| --- | --- | --- | --- |
| 1 | 100000 | 1001 | 8333.33 |
| 1 | 100000 | 1004 | 8333.33 |
| 2 | 85000 | 1002 | 7083.33 |
| 4 | 120000 | 1003 | 10000.00 |

(We also dropped the redundant `employee_id` column from our output.)

### Left Join

The `LEFT JOIN` keyword returns all rows from the left table, and the matching rows from the right table.  If there is no match, the right table columns will be `NULL`.

```sql
> SELECT * FROM employee LEFT JOIN paycheck ON employee.id = paycheck.employee_id;
```

| id | salary | check_id | employee_id | amount |
| --- | --- | --- | --- | --- |
| 1 | 100000 | 1001 | 1 | 8333.33 |
| 1 | 100000 | 1004 | 1 | 8333.33 |
| 2 | 85000 | 1002 | 2 | 7083.33 |
| 3 | 75000 | NULL | NULL | NULL |
| 4 | 120000 | 1003 | 4 | 10000.00 |

There is also a `RIGHT JOIN` which is the same as a `LEFT JOIN` but with the tables reversed, and a `FULL JOIN` which returns all rows from both tables. These are less common and not supported by SQLite.

### Demo: Run Some Joins on Contribution

```sql
SELECT * from candidate, contribution ON candidate.cand_id = contribution.cand_id;
```

Lots of unnecessary information, let's use projection to get the columns we want.

```sql
SELECT cand.lastname, cand.firstname, cand.state AS cand_state, cont.state AS cont_state, cont.amount  
   FROM candidate AS cand JOIN contribution AS cont 
   ON cand.cand_id = cont.cand_id;
```

Top 3 by contributions:

```sql
SELECT candidate.cand_id, lastname, firstname, SUM(amount) AS total 
   FROM candidate JOIN contribution 
   ON candidate.cand_id = contribution.cand_id
   GROUP BY candidate.cand_id 
   ORDER BY total DESC
   LIMIT 3;
```

Top 3 in state:

```sql
SELECT candidate cand.id_lastname, firstname, SUM(amount) AS total 
    FROM candidate, contribution ON candidate.cand_id = contribution.cand_id
    WHERE candidate.state = contribution.state
    GROUP BY candidate.cand_id
    ORDER BY total DESC
    LIMIT 3;
```

## DDL

Let's take a look at how to create a table:

### Creating Tables

Each table has a schema that defines the columns and their types.  The schema is created using the `CREATE TABLE` statement.

```sql
CREATE TABLE candidate
  (committee_id varchar(10),
   lastname varchar(50),
   firstname varchar(50),
   party varchar(6),
   city varchar(20),
   state varchar(2),
   zip integer,
   cand_id varchar(10),
   district varchar(2),
   constraint pk_candidate primary key (committee_id));
CREATE TABLE contribution
  (cand_id varchar(10),
   amount integer,
   city varchar(20),
   state varchar(10),
   zip integer,
   month integer,
   year integer,
   constraint fk_contribution foreign key (cand_id)
    references candidate (cand_id));
```

Each table is a tuple of named types as well as any constraints on the data.

Types:

* `varchar(n)` - a string that can be up to length `n` characters.
* `text` - a string of arbitrary length
* `integer` - an integer
* `real` - a floating point number

**Major Caveat**

SQLite doesn't really care much about types, for instance, it doesn't actually enforce varchar lengths, and will happily store non-numeric data in integer columns.  It's up to you to make sure your data is valid.

In newer versions of SQLite you can add the `STRICT` qualifier to the end of a `CREATE TABLE` statement to make SQLite enforce types. Every other major database (Postgres, MySQL, etc.) will enforce types.

<https://www.sqlite.org/stricttables.html>

### Indexes

Indexes tell the database to use additional space to help speed up queries. When an indexed column is used in a query, the database can use the index to quickly find the rows that match the query.

Another DDL statement lets us create an index:

```sql
CREATE INDEX idx_name ON candidate (lastname, firstname);
```

This would speed up queries that use both `lastname` and `firstname` in a `WHERE` clause.  (Some databases may also be able to use the index for queries that use only one of the columns, but this isn't guaranteed.)

### Primary Keys

Every table should have a primary key. This is an indexed column that should uniquely identify the data. It is common to use an auto-incrementing integer as the primary key.

### Foreign Keys

Foreign keys are used to link data across tables. They are indexed columns that should match the primary key of another table.

### NOT NULL

The `NOT NULL` constraint tells the database that a column cannot be `NULL`.  This is useful for columns that should always have a value.  (Note that the default is to allow NULL values everywhere except primary keys.)

## DML

### Inserting Data

The `INSERT` statement is used to add new rows to a table.

```sql
INSERT INTO candidate (committee_id, lastname, firstname, party, city, state, zip, cand_id, district)
VALUES ('C00999999', 'Wayne', 'Bruce', 'Independent', 'Gotham', 'IL', '60606', 'P80009999', '03');
```

### Updating Data

The `UPDATE` statement is used to change the values of existing rows.

```sql
UPDATE candidate SET party = 'Republican' WHERE cand_id = 'P80003338';
```

**Warning**

Like `SELECT`, you can leave a `WHERE` clause off of `UPDATE` and `DELETE` statements.  This will update or delete all rows in the table.

Many people like to add a `LIMIT` clause to `UPDATE` and `DELETE` statements to make sure they don't accidentally delete or update too many rows.

Another tip is to write your WHERE clause first, so you don't forget it.

### Deleting Data

The `DELETE` statement is used to remove rows from a table.

```sql
DELETE FROM candidate WHERE cand_id = 'P80003338';
```

If there is related data and you have proper constraints, this will fail until those rows are deleted first.
There are a number of ways to handle this, but the most common is to use `ON DELETE CASCADE` in the foreign key constraint if desired.

## SQL From Python

### `sqlite3`

```python
>>> import sqlite3

>>> conn = sqlite3.connect('fec.db')
>>> cur = conn.cursor()
>>> cur.execute('SELECT * FROM candidate LIMIT 3')
>>> for row in cur.fetchall():
...     print(row)
('H0AK00089', 'CRAWFORD', ' HARRY T JR', 'DEM', 'ANCHORAGE', 'AK', 99504, 'C00466698', '00')
('H0AK00097', 'COX', ' JOHN R.', 'REP', 'ANCHOR POINT', 'AK', 99556, '', '00')
('H0AK01038', 'FISHER', ' SHELDON ALLRED', 'REP', 'ANCHORAGE', 'AK', 99517, 'C00474783', '01')
```

This returns tuples, you can get the column names from cur.description.
It is generally easier to use the `row_factory` to return `Row` objects instead of tuples.

```python
>>> import sqlite3
>>> conn = sqlite3.connect('fec.db')
>>> conn.row_factory = sqlite3.Row
>>> cur = conn.cursor()
>>> cur.execute('SELECT * FROM candidate LIMIT 3')
>>> for row in cur.fetchall():
...     print(row['firstname'], row['lastname'])
HARRY T JR CRAWFORD
JOHN R. COX
SHELDON ALLRED FISHER
```

These objects work like dictionaries, and you can access the columns by name.

### Injection & Placeholders

It is common to use some user input to build a query, such as in a search form.
Doing this naively can lead to SQL injection attacks.

```python
>>> import sqlite3
>>> conn = sqlite3.connect('fec.db')
>>> cur = conn.cursor()
>>> search_string = "Jane"
>>> query = "SELECT * FROM candidate WHERE firstname = '" + search_string + "'"
>>> cur.execute(query)
```

This is vulnerable to SQL injection attacks.
If the user enters `'; DROP TABLE candidate; --` as the search string, the query will be:

```sql
SELECT * FROM candidate WHERE firstname = ''; DROP TABLE candidate; --'
```

This will drop the candidate table.
The `--` at the end of the string is a comment, so the rest of the query is ignored.

To avoid this, you should use placeholders in your query, and pass the values as a tuple to `execute`.

```python
>>> import sqlite3
>>> conn = sqlite3.connect('fec.db')
>>> cur = conn.cursor()
>>> search_string = "Jane"
>>> query = "SELECT * FROM candidate WHERE firstname = ?"
>>> cur.execute(query, (search_string,))
```

This will pass the value as a tuple, and the database will escape it properly, ensuring that special characters like `'` and `;` are escaped and not parsed as part of the query itself.

This has the added benefit of making your code more readable with a prepared statement working as a sort of function where you can plug in necessary parameters.

## Database Design

**Normalization** - Structuring data to reduce duplication.

**Denormalization** - Structuring data to reduce joins.

Let's imagine a fictional company database.

In our company, every employee has a first & last name, an email, salary, and works for a department, where they have a title.

We could try to model this with one table:

* employee ( id, first_name, last_name, email, salary, department_name, title )

We decide we want each department to have a manager, so we add a manager_id column.

* employee ( id, first_name, last_name, email, salary, department_name, title, manager_id )

This data is now redundant.  If we have 100 employees in the "Research & Development" department, we're storing that name 100 times and the manager ID as well. A subtle bug in our code could also lead to these getting out of sync with one another since they always need to be updated together.

We can fix this by creating a separate table for departments:

* department ( id, name, manager_id )
* employee ( id, first_name, last_name, email, salary, department_id, title )
  * foreign key ( department_id ) references department ( id )

This is a step in the direction of normalization. We've removed the redundant data, but we've also added a new table and a new column.  We've also added a new foreign key constraint.

Hooray! This seems fantastic, let's keep doing it!
We can continue to normalize this data by creating a separate table for titles and salaries:

* department ( id, name, manager_id )
* employee ( id, first_name, last_name, email, department_id )
  * foreign key ( department_id ) references department ( id )
* employee_title ( employee_id, title )
  * foreign key ( employee_id ) references employee ( id )
* employee_salary ( employee_id, salary )
  * foreign key ( employee_id ) references employee ( id )

This may seem like we've gone too far. Querying our data is now much more complicated, we'll typically need 3-4 joins to get the data we want.

Here's an example of listing all employees in a department, with their title and salary:

```sql
SELECT e.first_name, e.last_name, t.title, s.salary
FROM employee e
JOIN employee_title t ON t.employee_id = e.id
JOIN employee_salary s ON s.employee_id = e.id
JOIN department d ON d.id = e.department_id
WHERE d.name = 'Research & Development';
```

But we've also made our data more flexible. We can now store multiple titles for an employee, we could also add additional fields to the employee_salary table such as the date the salary was effective, or the date the salary was changed.

* department ( id, name, manager_id )
* employee ( id, first_name, last_name, email, department_id )
  * foreign key ( department_id ) references department ( id )
* employee_title ( employee_id, title, effective_date )
  * foreign key ( employee_id ) references employee ( id )
* employee_salary ( employee_id, salary, effective_date )
  * foreign key ( employee_id ) references employee ( id )

### Design Issues

We want to make a table for students & activities:

#### Step One

**student_activities**

name | activity1 | cost1 | activity2 | cost2 |
-----|-----------|-------|-----------|-------|
John | Soccer    |  10   | Baseball  |  20   |
Jane | Baseball    |  10   | Soccer  |  20   |
Alex | Golf |  30   | NULL | NULL |
Jane | Hockey    |  30   | NULL | NULL |

Problems:

* Non-unique records

#### Step Two

Could split into two tables:

**student**

id | name
---|-----
1  | John
2  | Jane
3  | Alex
4  | Jane

(we now know this is a different Jane)

**student_activities**

id | activity1 | cost1 | activity2 | cost2
---|-----------|-------|-----------|-------
1  | Soccer    |  10   | Baseball  |  20
2  | Baseball    |  10   | Soccer  |  20
3  | Golf |  30   | NULL | NULL
4  | Hockey    |  30   | NULL | NULL

Problems:

* [x] Non-unique records~
* [ ] Wasted space (NULLs)
* [ ] Limited number of activity spots
* [ ] How to find all students who play soccer?  Search both columns

#### Step Three

**student**

id | name
---|-----
1  | John
2  | Jane
3  | Alex
4  | Jane

**student_activity**

student_id | activity | cost
---|----------|------
1  | Soccer   | 10
1  | Baseball | 20
2  | Baseball | 10
2  | Soccer   | 20
3  | Golf     | 30
4  | Hockey   | 30

Issues:

* [x] Non-unique records~
* [x] Wasted space (NULLs)
* [x] Limited number of activity spots
* [x] How to find all students who play soccer?  Search both columns
* [ ] Prices are not guaranteed to be consistent
* [ ] How to update prices?
* [ ] If student drops golf, we can lose the price.
* [ ] No way to make new activities visible.

#### Step Four

**students**

id | name
---|-----
1  | John
2  | Jane
3  | Alex
4  | Jane

**activities**

id | name | cost
---|------|------
1  | Soccer | 10
2  | Baseball | 20
3  | Golf | 30
4  | Hockey | 30

**student_activity**

student_id | activity_id
---|----------
1  | 1
1  | 2
2  | 2
2  | 1
3  | 3
4  | 4

### Tips

**One table per entity** - The major **nouns** in your application should be represented by tables.

**One-to-many relationships** - When you have a relationship that is one-to-many (e.g. a user has many photos), the many side should have a foreign key to the one side.

A user has many photos.
This can be thought of as a one-to-many relationship, since each photo was uploaded by *one* user, but a user can have as many photos as they want.

* user ( id, name, email )
* photo ( id, user_id, url )
  * foreign key ( user_id ) references user ( id )

**Many-to-many relationships** - Require an intermediate join table like `student_activity` above.

A user can belong to many groups, and a group of course has multiple users.

* user ( id, name, email )
* group ( id, name, description )
* group_membership ( user_id, group_id )
  * foreign key ( user_id ) references user ( id )
  * foreign key ( group_id ) references group ( id )

Note: It is possible to have additional data on the join table, such as the date the user joined the group.

**One-to-one relationships** - When you have a relationship that is one-to-one (e.g. a user has one profile), the one side should have a foreign key to the other side.

These are less common, since it often makes sense to just store the data in a 1:1 relationship on a single table.

## Non-Relational Databases

An old concept that had mostly fallen out of favor until ~2009, when it was rediscovered and became popular again.

**Document databases** like MongoDB and CouchDB allow you to store "documents" (JSON objects) in a database.  These documents can be nested, and can contain arrays.

* Highly-flexible schemas (for better or worse)
* Easy to store nested data & arrays
* Often used for storing JSON data, which is common in web applications as we've seen.

**Key-value stores** like Redis allow you to store key-value pairs in a database.  These are often used for caching, or for storing configuration data.  They are very fast but much less flexible than other databases.

* Very fast
* Very limited operations (often just get/set/count)
* Often used for caching

**Graph databases** like Neo4j allow you to store nodes and relationships between them.  These are often used for social networks, or for storing data that is naturally represented as a graph. They are highly specialized, but excellent for their particular use cases.

**Wide-column stores** like Cassandra allow you to store data in a column-oriented fashion.  This is often used for storing large amounts of data, or for storing data that is naturally represented in a columnar fashion.

**Search databases** like ElasticSearch allow you to store data and then do full text search on it.  This is often used for storing large amounts of data that needs to be searched.

## PostgreSQL

In the last few years PostgreSQL has become dominant among open-source relational databases.  It is a very powerful, mature, and flexible database.

It has some terrific features we don't have time to go over, but that make it a great choice for many applications:

* **Full-text search** - support for special indexes that allow optimized full text search (much more flexible and faster than using LIKE).
* **JSON support** - this allows you to have columns that are JSON objects, essentially allowing a document database inside of your relational database.
* **Geospatial support** - this allows you to store latitude/longitude coordinates, polygons, etc. and do geospatial queries on them.
* **Foreign data wrappers** - this allows you to connect to other databases and query them as if they were tables in your database.

## ORMs

**Object-relational mapping** (ORM) is a technique that allows you to write code in an object-oriented language (e.g. Ruby, Python, Java, C#, etc.) and have it automatically translate to SQL queries.

```python
# SQLalchemy
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    grade = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)

    
class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    students = db.relationship('Student', secondary='student_classroom')


class StudentClassroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    

# get all students named Jane
for student in Student.query.filter_by(name='Jane').all():
    print(student.name)

        
# get all students in "Chemistry 101"
Student.query.join(StudentClassroom).join(Classroom).filter(Classroom.name == 'Chemistry 101').all()
```

```python
# Django ORM
class Student(models.Model):
    name = models.CharField(max_length=80, unique=True)
    grade = models.IntegerField()
    email = models.EmailField()

    
class Classroom(models.Model):
    name = models.CharField(max_length=80, unique=True)
    students = models.ManyToManyField(Student)
    

# get all students named Jane
for student in Student.objects.filter(name='Jane'):
    print(student.name)

    
# get all students in "Chemistry 101"
Student.objects.filter(classroom__name='Chemistry 101')
```

**Common pitfalls**

* **Bad Design** - A poorly designed database isn't saved by using an ORM. (In fact, it can make it worse.)
  * Understanding normalization & denormalization tradeoffs is important.
* **Python Performance** - ORMs typically spend a lot of time converting between objects and underlying data, which can be very slow.
  * Most ORMs have a way to deal in tuples/dictionaries instead of objects, which can be much faster for larger queries.
* **Complex Queries** - If you have a complex query, it can be hard to write it in an ORM and keep track of the decisions the ORM has made.  
  * SQL is a powerful language, and it is often more efficient to write a query in SQL than to try to write it in an ORM and hope it does what you're expecting.
* **N+1 Queries** - When you have a list of objects, and you want to get some related data for each of them, you often end up with a query for each object.
  * `select_related` or `prefetch_related` in Django, or `joinedload` in SQLAlchemy can help with this, but require an understanding of when the ORM is doing JOINs.
