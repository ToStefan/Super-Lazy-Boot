# Super Lazy Boot

Generate controllers, services, mappers, anotations and much more for spring boot with just writting simple model file.

## Installation

+ Super Lazy Boot requires [Python](https://www.python.org/) v3+ to run.
+ Install Python and clone repository.
```sh
    > git clone https://github.com/ToStefan/Super-Lazy-Boot.git
```

+ Start application.
```sh
    > python3 super-lazy-boot.py YOUR-MODEL-FILE-NAME.json
```

### Model file example & syntax explain

```sh
[
	{
	"type": "Class",
	"classes": [
		{
			"name": "User",
			"atributes": {
				"id": "Long",
				"username": "String",
				"password": "String",
				"roles": "CLASS_List<Role>"
			},
			"primaryKey": "id"
		},
		{
			"name": "Job",
			"atributes": {
				"id": "Long",
				"title": "String",
				"workType": "ENUM_WorkType"
			},
			"primaryKey": "id"
		},
		{
			"name": "Role",
			"atributes": {
				"id": "Long",
				"name": "ENUM_RoleName"
			},
			"primaryKey": "id"
		}
	]},
	{
	"type": "Enum",
	"enums": [
		{
			"name": "WorkType",
			"values": ["FULL_TIME", "PART_TIME"]
		},
		{
			"name": "RoleName",
			"values": ["ROLE_ADMIN", "ROLE_USER"]
		}
	]},
	{
	"type": "Settings",
	"settings": {
		"lombok": true, (default: false)
		"rootPackage": "test.demo" (rootPackage must be specified or will throw error)
	}}
]
```

This model will create you all basic CRUD operations for controllers also will generate mappers and services and automatically will autowire everything.

If attribute type is custom class or enum you need to specify "CLASS_" or "ENUM_" before type.

If you don't specify settings value, default values will be used.

Model file must be JSON.

### Future features

+ Generating on web platform
+ Exception handling
+ Spring Security
+ Pagination
+ Better annotation generator