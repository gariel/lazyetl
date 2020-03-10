# Lazy ETL

-----

# > For now this is work in progress <
> Not working on master at the moment.  
> For a working POC version, see branch [first_implementation](https://github.com/gariel/lazyetl/tree/first_implementation)

-----

## Extract Transform Load

At this time virtual env is only used for the editor.

To run:
``` bash
python etl
```

To run specifying the job xml:
``` bash
python etl simple.xml
```

To run tests:
``` bash
python tests
```

The `simple.xml` example has 4 steps:
1. Print "Hello World"
2. Ask for a name (user input)
3. Change the inserted name to upper case
4. Print the message with insert name in upper case

Execution:
```
$ python etl
Hello World
Insert a name: test
The inserted name in upper case is: TEST
```
