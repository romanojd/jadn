<!-- Generated from schema\jadn-csdpr02.jadn, Mon Mar 18 17:59:50 2019-->
## Schema
| . | . |
| ---: | :--- |
| **title:** | JADN Syntax |
| **module:** | oasis-open.org/openc2/jadn/v1.0 |
| **patch:** | 0-csdpr02 |
| **description:** | Syntax of a JSON Abstract Data Notation (JADN) module. |
| **exports:** | Schema, Uname |

**_Type: Schema (Record)_**

| ID | Name | Type | # | Description |
| ---: | :--- | :--- | ---: | :--- |
| 1 | **meta** | Meta | 1 | Information about this schema module |
| 2 | **types** | Type | 1..* | Types defined in this schema module |

**_Type: Meta (Map)_**

| ID | Name | Type | # | Description |
| ---: | :--- | :--- | ---: | :--- |
| 1 | **module** | Uname | 1 | Schema unique name/version |
| 2 | **patch** | String | 0..1 | Patch version |
| 3 | **title** | String | 0..1 | Title |
| 4 | **description** | String | 0..1 | Description |
| 5 | **imports** | Import | 0..* | Imported schema modules |
| 6 | **exports** | Identifier | 0..* | Data types exported by this module |
| 7 | **bounds** | Bounds | 0..1 | Schema-wide upper bounds |

**_Type: Import (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Nsid | 1 | **nsid** - A short local identifier (namespace id) used within this module to refer to the imported module |
| 2 | Uname | 1 | **uname** - Unique name of imported module |

**_Type: Bounds (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Integer | 1 | **max_msg** - Maximum serialized message size in octets or characters |
| 2 | Integer | 1 | **max_str** - Maximum string length in characters |
| 3 | Integer | 1 | **max_bin** - Maximum binary length in octets |
| 4 | Integer | 1 | **max_fields** - Maximum number of elements in ArrayOf |

**_Type: Type (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Identifier | 1 | **tname** - Name of this datatype |
| 2 | Enumerated.* | 1 | **btype** - Base type.  Enumerated value derived from list of JADN data types |
| 3 | Options | 1 | **opts** - Type options |
| 4 | String | 1 | **desc** - Description of this data type |
| 5 | JADN-Type | 0..* | **fields** - List of fields for compound types.  Not present for primitive types |

**_Type: JADN-Type (Choice)_**

| ID | Name | Type | # | Description |
| ---: | :--- | :--- | ---: | :--- |
| 1 | **Binary** | Null | 1 | Octet (binary) string |
| 2 | **Boolean** | Null | 1 | True or False |
| 3 | **Integer** | Null | 1 | Whole number |
| 4 | **Number** | Null | 1 | Real number |
| 5 | **Null** | Null | 1 | Nothing |
| 6 | **String** | Null | 1 | Character (text) string |
| 7 | **Array** | FullField | 1 | Ordered list of unnamed fields |
| 8 | **ArrayOf** | Null | 1 | Ordered list of fields of a specified type |
| 9 | **Choice** | FullField | 1 | One of a set of named fields |
| 10 | **Enumerated** | EnumField | 1 | One of a set of id:name pairs |
| 11 | **Map** | FullField | 1 | Unordered set of named fields |
| 12 | **Record** | FullField | 1 | Ordered list of named fields |

**_Type: EnumField (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Integer | 1 | ****Item ID |
| 2 | String | 1 | ****Item name |
| 3 | String | 1 | ****Item description |

**_Type: FullField (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Integer | 1 | ****Field ID or ordinal position |
| 2 | Identifier | 1 | ****Field name |
| 3 | Identifier | 1 | ****Field type |
| 4 | Options | 1 | ****Field options |
| 5 | String | 1 | ****Field description |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **Identifier** | String [0..32] | A string starting with an alpha char followed by zero or more alphanumeric / underscore / dash chars |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **Nsid** | String [1..8] | Namespace ID - a short identifier |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **Uname** | String [1..100] | Unique name (e.g., of a schema) - typically a set of Identifiers separated by forward slashes |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **Options** | ArrayOf(Option) [0..10] | Options list may be empty but may not be omitted |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **Option** | String [1..100] | Option string: 1st char = option id |
