# Data Pipelines

We've discussed various techniques for collecting and cleaning data, as well as how to store data in a database.

These three steps are together known as the ETL process, which stands for Extract, Transform, and Load.

It can be useful to think of these as different steps in a pipeline, where the output of one step is the input to the next step. Dividing the process into steps makes it easier to understand and debug.

## Unix Philosophy

In the late 1970s, Ken Thompson and Dennis Ritchie developed the Unix operating system.

Unix was designed to be modular, and to have a small number of tools that could be combined to do more complex tasks.

Modern MacOS and Linux systems are largely based on Unix and inherit this philosophy.

One summary of the philosophy is:

* Write programs that do one thing and do it well.
* Write programs to work together.
* Write programs to handle text streams, because that is a universal interface.

(<https://en.wikipedia.org/wiki/Unix_philosophy>)

Let's take a look at some command line tools that follow this philosophy.

### grep

The `grep` command searches for a pattern in a file.

For example, to search for the word "data" in a file called `data.txt`, we can run:

```bash
grep Rafi courses.txt
```

The `re` in `grep` stands for regular expression.

```bash
grep -E 'Unix|Python' data.txt
```

### cut

The `cut` command extracts columns from a file.

Extract columns 1 and 2 from a file called `courses.txt`:

```bash
cut -f1,2 courses.txt
```

You can use different delimiters (e.g. commas) by specifying the `-d` option.

### sort

The `sort` command sorts the input it is given.

By default it sorts alphabetically.

```bash
sort numbers.txt
```

You can sort numerically by using the `-n` option.

```bash
sort -n numbers.txt
```

What does this command do if you don't give it a filename?

```bash
sort
```

### manual pages / man pages

Every command has a manual page that describes how to use it.   Access these with the `man` command.

```bash
man sort
```

## stdin, stdout, stderr

You'll notice these files output to the terminal. This is because they are writing to a special file called `stdout`.

We can redirect the output to a file by using the `>` operator.

```bash
cut -f2 courses.txt > course_names.txt
cat course_names.txt   # cat outputs a file, you can also use head or tail to get just some of the file
```

If you have a command that is expecting input, you can provide it by using the `<` operator.

```bash
sort < course_names.txt
```

If you want to redirect both the input and output, you can use the `|` operator.

```bash
cut -f2 courses.txt | sort
```

This takes the output of `cut` and uses it as the input to `sort`.

You can chain multiple commands together using `|`.

```bash
cut -f2 courses.txt | sort | uniq
```

Note: `uniq` only removes adjacent duplicates, so you should always sort before using `uniq`.

Some commands write errors to a special file called `stderr`. This is useful for debugging, so that you can separate the output from the errors.

To redirect stderr to a file, you can use the `2>` operator.

Composing commands in this way is known as a pipeline. It is a powerful way to combine tools to do more complex tasks.

## shell scripting

When you're on a Unix machine you're using a shell, typically `bash` or `zsh`.

Shells allow you to run commands by typing them into the terminal, but they also allow you to write scripts that run commands.

A shell script is a text file that contains a series of commands.

Writing a shell script takes three steps:

* Write the commands you want to run in a text file.
* Add a shebang line to the top of the file.
* Make the file executable by running `chmod +x script.sh`.  Where `script.sh` is the name of your file.

### shebang line

The shebang line is the first line of the file, and it tells the shell which program to use to run the script.

```bash
#!/bin/bash
#!/usr/bin/env python3
#!/bin/zsh
```

*#!* is the "shebang" character sequence.

### Example Shell Script

Let's write a shell script that runs the commands we've been using in this section.

```bash
#!/bin/bash

cut -f2 courses.txt | sort | uniq > course_names.txt
```

Save this as `courses.sh` and make it executable.

### Advanced Scripting

Shells like `bash` and `zsh` support features like variables, conditionals, and loops.

The typical advice given is that if your shell script is more than 50-100 lines long, you should probably rewrite it in a "real" programming language.

I'm personally of the belief this number might better be set at 5-10 lines.  Shell scripting languages are filled with traps for the unwary, and it's easy to write a script that is hard to debug. There's also nothing you can do in a shell script that you can't do in a language like Python.

```
LOGINS=`w -h | wc -l`
if [ $LOGINS -gt 10 ]; then
    echo "There are too many people logged in."
fi
```

### Environment Variables

Shells have the concept of environment variables which can typically be set with the `export` command.

Environment variables are useful for storing configuration information.  It can be useful to set environment variables from the command line, which can then be accessed in your scripts (regardless of what language they are written in).

This is a common way to avoid storing sensitive information in your code.

Database credentials and API keys are often stored in environment variables, instead of written in code that is then checked into version control.

```bash
export DB_PASSWORD="abc123"
```

```python
import os
print(os.environ['DB_PASSWORD'])
```

In Python all environment variables are stored in the `os.environ` dictionary. This allows values set on the command line or by other shell scripts to be read by Python programs.

A common pattern is to have an `env.sh` file that sets environment variables, and then to source this file from other scripts.

**env.sh**

```bash
#!/bin/bash

export DB_USERNAME="jason"
export DB_PASSWORD="abc123"
export TWITTER_API_KEY="39082klsjd9022lkja90322z"
```

Then access these variables via `os.environ` in your Python programs.

## Python Programs

We can write Python programs that follow the Unix philosophy.

Instead of a single program that does everything, we can write a series of programs that each do one thing.

It is fine for these to all live within the same Python package, but you'd want separate submodules for each program.

For your project you may want to write a series of programs that each do one thing.

```bash
python -m project.scrape_world_bank      # scrapes the World Bank & saves data to world_bank.csv
python -m project.clean_world_bank       # cleans the World Bank data & loads it into a database world_bank.db
python -m project.generate_report        # generates a report from the data in world_bank.db and saves some seaborn plots to the reports/ directory
```

This is a good start, but we may find it would be nice to be able to run `clean_world_bank` and `generate_report` on smaller subsets of the data.

Perhaps we alter our scripts to take a command line argument that specifies the input or output files:

```bash
python -m project.scrape_world_bank --output world_bank.csv
python -m project.clean_world_bank --input world_bank.csv --output world_bank.db
python -m project.generate_report --input world_bank.db --output reports/test_image.png
```

This makes it possible to run the scripts on smaller subsets of the data.

Remember, you can accomplish this by using positional arguments by using `sys.argv` as we've seen before,
or using the `argparse` or `click` modules to define more complete interfaces.  Look at your assignments
for examples of how to use command line arguments.

`argparse`: <https://docs.python.org/3/library/argparse.html>

`click`: <https://click.palletsprojects.com/en/7.x/>

### Interacting with other programs

If you want your Python program to work the way that the built in Unix programs work, you'll need to interact with them in a specific way.

For example, if you want your program to read data from `stdin` and write data to `stdout`, you'll need to use `sys.stdin` and `sys.stdout`.

**spongebob.py**

```python
import sys

def alt_case(text):
    result = ""
    for i, char in enumerate(text):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()
    return result

# stdin is a file-like object that we can read from
for line in sys.stdin:
    print(alt_case(line))
```

```bash
./spongebob.py
```

```bash
./spongebob.py < courses.txt
```

`print` will write to `stdout` by default.

You can control this by passing the `file` argument to `print`.

```python
print("an error occurred", file=sys.stderr)
```

### `subprocess`

The `subprocess` module allows you to run other programs from within your Python program.

```python
import subprocess

subprocess.run(["echo", "hello world"])
```

You can also capture the output of the program.

```python
result = subprocess.run(["ls", "-l"], capture_output=True)
print(result.stdout)
```

And you can pass the output of one program to another.

```python
result = subprocess.run(["ls", "-l"], capture_output=True)
subprocess.run(["wc", "-l"], input=result.stdout)
```

This is more verbose than pipes, but allows you to use Python features you already know to interact with other programs.

`subprocess`: <https://docs.python.org/3/library/subprocess.html>

`shutil`: <https://docs.python.org/3/library/shutil.html>

`os`: <https://docs.python.org/3/library/os.html>

## Pipeline Automation

If your program is broken down into a series of programs that each do one thing, you might write a simple bash script to run them in sequence.

```bash
#!/bin/bash

python -m project.scrape_world_bank --output world_bank.csv
python -m project.clean_world_bank --input world_bank.csv --output world_bank.db
python -m project.generate_report --input world_bank.db --output reports/test_image.png
```

This is a good start, but you might discover that `scrape_world_bank` doesn't need to run if you already have a file called `world_bank.csv`. You could write a more complex bash script to check for the existence of the file, but there are tools that can do this for you.

### make

The `make` command is a tool for automating pipelines.

The `make` command reads a file called `Makefile` and runs the commands specified in that file.

The `Makefile` is a text file that contains a series of rules.

For example, here is a `Makefile` that would work with our example above:

```make
world_bank.csv:
    python -m project.scrape_world_bank --output world_bank.csv

world_bank.db: world_bank.csv
    python -m project.clean_world_bank --input world_bank.csv --output world_bank.db

reports/test_image.png: world_bank.db
    python -m project.generate_report --input world_bank.db --output reports/test_image.png
```

A makefile consists of targets, dependencies, and commands.

This file contains three rules:

* `world_bank.csv` is the target, and it depends on nothing.
* `world_bank.db` is the target, and it depends on `world_bank.csv`.
* `reports/test_image.png` is the target, and it depends on `world_bank.db`.

Under each rule, we have a list of commands that are executed if the target does not exist or if any of the dependencies are newer than the target.

You can then run commands like

```bash
make world_bank.csv
```

and the `make` command will run the commands specified in the `Makefile` to generate the target.

If you try to make a target that has dependencies, then `make` will first make the dependencies if they don't exist.

```bash
make reports/test_image.png
```

This would first make `world_bank.csv`, then `world_bank.db`, and then `reports/test_image.png`.

## New CLI Tools

You can count on commands like `cat`, `uniq`, `make`, and `grep` being available on any Unix system.

That doesn't mean they are the end all be all of command line tools.

Many newer tools exist that are very powerful and can be used to accomplish tasks that would be difficult to do with the built in tools.

Quite a few are improvements on the built in tools, and some are completely new tools that do things that the built in tools can't do.

### `jq`

`jq` is a command line tool for working with JSON data.

<https://stedolan.github.io/jq/>
<https://stedolan.github.io/jq/tutorial/>

```bash
# select a field
jq '.name' data.json

# select multiple fields
jq '.name, .age' data.json

# chaining JQ commands
jq .results[] data.json | jq 'select(.name | test("^[a-z]{3}$"))'
```

### `csvkit` & `xsv`

`csvkit` and `xsv` are command line tools for working with CSV data.

<https://csvkit.readthedocs.io/en/latest/>

<https://github.com/BurntSushi/xsv>

XSV Examples:

```bash
# select columns
xsv select name,age data.csv

# filter rows by regex
xsv search --select name,age --regex --fixed-strings --case-insensitive '^[a-z]{3}$' data.csv
```

### `ag` / `ripgrep`

`ag` and `ripgrep` are command line tools for searching files that are faster & easier to use than `grep`

`ag`: <https://github.com/ggreer/the_silver_searcher>
`ripgrep`: <https://github.com/BurntSushi/ripgrep>

```bash
# search for a string
ag "hello world"

# search for a regex (no need for flags)
ag "hello.*world"

# search just specific file types
ag "hello world" --html --css --js
```

### `just`

`just` is a command line tool for running commands in a `justfile`.

It is similar to `make`, but has a more modern syntax and a lot of quality of life improvements.

<https://github.com/casey/just>

### Conclusion

The command line interface is a powerful tool for interacting with data.

By chaining together commands, you can automate tasks that would be difficult to do with a GUI without writing much (any) code.

Getting familiar with these tools pays dividends in the long run, and can also inspire you to write your own simple tools
to automate common tasks.

The fact that any Unix-based system has these tools available means that you can use them on any system, and you can also use them to interact with remote systems. This means if you find yourself working in an unfamiliar environment, you can still use the tools you know to get the job done.
