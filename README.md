# Super Lazy Boot

Create JSON model file which can generate spring boot app with controllers, services, entites, anotations, mappers, dtos, imports

## Installation

Super Lazy Boot requires [Python](https://www.python.org/) v3+ to run.
- Install Python and clone repository.
```
> git clone https://github.com/ToStefan/Super-Lazy-Boot.git
```

- Start application.
```
> python3 super-lazy-boot.py YOUR-MODEL-FILE-NAME.json
```

### Rules & Model File Example

- `All Settings values are required`
- Model file must be properly formated JSON
- `ID with "type": Long and "field_type": id must be specified otherwise, project will not be generated fully`
- "field_type" in attributes must be specified (possible values):
	- `"normal", "id", "enum", "class", "list", "set" `
- fields with default values and possible values (don't need to specify in some cases):
	- "nullable": "false"
		- `"true", "false"`
	- "fetch_type": "lazy"
		- `"lazy", "eager"`
	- "cascade_type": "all",
		- `"persist", "merge", "refresh", "remove", "detach", "all"`


```json
[
	{
	"type": "Class",
	"classes": [
		{
			"name": "User",
			"atributes": [
				{
					"field": "id",
					"type": "Long",
					"field_type": "id"
				},
				{
					"field": "userName",
					"type": "String",
					"field_type": "normal"
				},
				{
					"field": "roles",
					"type": "List<Role>",
					"field_type": "list",
					"nullable": "true",
					"relation": "n:n",
					"fetch_type": "eager",
					"cascade_type": "all"
				},
				{
					"field": "job",
					"type": "Job",
					"field_type": "class",
					"nullable": "true",
					"relation": "1:1"
				},
				{
					"field": "images",
					"type": "List<Image>",
					"nullable": "true",
					"field_type": "list",
					"relation": "1:n"
				}
			]
		},
		{
			"name": "Job",
			"atributes": [
				{
					"field": "id",
					"type": "Long",
					"field_type": "normal"
				},
				{
					"field": "title",
					"type": "String",
					"field_type": "normal"
				},
				{
					"field": "workType",
					"type": "WorkType",
					"field_type": "enum"
				}
			]
		},
		{
			"name": "Role",
			"atributes": [
				{
					"field": "id",
					"type": "Long",
					"field_type": "id"
				},
				{
					"field": "name",
					"type": "RoleName",
					"field_type": "enum"
				}
			]
		},
		{
			"name": "Image",
			"atributes": [
				{
					"field": "id",
					"type": "Long",
					"field_type": "id"
				},
				{
					"field": "user",
					"type": "User",
					"field_type": "class",
					"nullable": "true",
					"fetch_type": "eager",
					"cascade_type": "all",
					"relation": "n:1"

				}
			]
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
		"lombok": false,
		"rootPackage": "tflc.stefan.test",
		"serviceCollection": "Set:HashSet"
	}}
]

```
