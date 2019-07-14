# Super Lazy Boot

Generate controllers, services, mappers, anotations and much more for spring boot with just writting simple model file.

## Installation

+ Super Lazy Boot requires [Python](https://www.python.org/) v2.7 to run.
+ Install Python and clone repository.
```sh
    > git clone https://github.com/ToStefan/Super-Lazy-Boot.git
```

+ Start application.
```sh
    > python super-lazy-boot.py YOUR-MODEL-FILE
```

### Model file example & syntax explain

```sh
Class {
	User -> Long:id:primary -> String:username -> String:password -> Role:role,
	Job -> Long:id:primary -> String:title -> WorkType:workType
}

Settings {
	lombok:true (default: false)
	rootPackage: / (rootPackage must be specified or will throw error)
}


Enum {
	WorkType -> FULL_TIME -> PART_TIME,
	Role -> ROLE_ADMIN -> ROLE_USER
}
```

This model will create you all basic CRUD operations for controllers also will generate mappers and services and automatically will autowire everything.

keyword "primary" is for primary key column.

If you don't specify settings value, default values will be used.

Model file can be with any extension.

### Future features

+ Generating on web platform
+ Exception handling
+ Spring Security
+ Nested resources
+ Pagination