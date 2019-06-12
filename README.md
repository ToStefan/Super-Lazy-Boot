# Easy Spring Boot

Generate controllers, services, mappers, anotations and much more for spring boot with just writting simple model file.

## Installation

+ Easy Spring Boot requires [Python](https://www.python.org/) v2.7 to run.
+ Install Python and clone repository.

```sh
> git clone https://github.com/ToStefan/Easy-Spring-Boot.git
```

+ Start application.

```sh
> python easy-spring-boot.py YOUR-MODEL-FILE
```

### Model file example & syntax explain

```sh
Demo -> Long:id:primary -> String:text -> Integer:count
Test -> Long:id:primary -> String:about
```

This model will create you all basic CRUD operations for controllers for two entity "Demo" and "Test" also will generate mappers and services and automatically will autowire everything.

keyword "primary" is for primary key collumn.

The script will generate the most import commands, but some you need to mannualy like a package declaration and all the imports based on the project package.

### Future features

+ Generating whole spring boot project 
+ Generating on web platform
+ Exception handling
+ Spring Security
