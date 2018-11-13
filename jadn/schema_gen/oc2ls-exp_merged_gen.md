<!-- Generated from schema\oc2ls-exp_merged.jadn, Tue Nov 13 13:34:54 2018-->
## Schema
| . | . |
| ---: | :--- |
| **title:** | OpenC2 Language with experimental elements |
| **module:** | oasis-open.org/openc2/v1.0/oc2ls-exp |
| **patch:** | 0-wd01+merged |
| **description:** | Datatypes that define the content of OpenC2 commands and responses. |
| **exports:** | OpenC2-Command, OpenC2-Response, Message-Type, Status-Code, Request-Id, Date-Time |

**_Type: Message (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Message-Type | 1 | msg_type -- message element |
| 2 | String | 1 | content_type -- message element |
| 3 | Null | 1 | content -- message element |
| 4 | Status-Code | 0..1 | status -- message element |
| 5 | Request-Id | 0..1 | request_id -- message element |
| 6 | String | 0..n | to -- message element |
| 7 | String | 0..1 | from -- message element |
| 8 | Date-Time | 0..1 | created -- message element |

**_Type: OpenC2-Command (Record)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **action** | Action | 1 | The task or activity to be performed (i.e., the 'verb'). |
| 2 | **target** | Target | 1 | The object of the action. The action is performed on the target. |
| 3 | **args** | Args | 0..1 | Additional information that applies to the command. |
| 4 | **actuator** | Actuator | 0..1 | The subject of the action. The actuator executes the action on the target. |

**_Type: Action (Enumerated)_**

| ID | Name | Description |
| ---: | --- | :--- |
| 1 | **scan** | Systematic examination of some aspect of the entity or its environment in order to obtain information. |
| 2 | **locate** | Find an object physically, logically, functionally, or by organization. |
| 3 | **query** | Initiate a request for information. |
| 6 | **deny** | Prevent a certain event or action from completion, such as preventing a flow from reaching a destination or preventing access. |
| 7 | **contain** | Isolate a file, process, or entity so that it cannot modify or access assets or processes. |
| 8 | **allow** | Permit access to or execution of a target. |
| 9 | **start** | Initiate a process, application, system, or activity. |
| 10 | **stop** | Halt a system or end an activity. |
| 11 | **restart** | Stop then start a system or activity. |
| 14 | **cancel** | Invalidate a previously issued action. |
| 15 | **set** | Change a value, configuration, or state of a managed entity. |
| 16 | **update** | Instruct a component to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update. |
| 18 | **redirect** | Change the flow of traffic to a destination other than its original destination. |
| 19 | **create** | Add a new entity of a known type (e.g., data, files, directories). |
| 20 | **delete** | Remove an entity (e.g., data, files, flows. |
| 22 | **detonate** | Execute and observe the behavior of a target (e.g., file, hyperlink) in an isolated environment. |
| 23 | **restore** | Return a system to a previously known state. |
| 28 | **copy** | Duplicate a file or data flow. |
| 30 | **investigate** | Task the recipient to aggregate and report information as it pertains to a security event or incident. |
| 32 | **remediate** | Task the recipient to eliminate a vulnerability or attack point. |

**_Type: Target (Choice)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **artifact** | Artifact | 1 | An array of bytes representing a file-like object or a link to that object. |
| 2 | **command** | Request-Id | 1 | A reference to a previously issued OpenC2 command. |
| 3 | **device** | Device | 1 | The properties of a hardware device. |
| 7 | **domain_name** | Domain-Name | 1 | A network domain name. |
| 8 | **email_addr** | Email-Addr | 1 | A single email address. |
| 16 | **features** | Features | 1 | A set of items used with the query action to determine an actuator's capabilities |
| 10 | **file** | File | 1 | Properties of a file. |
| 11 | **ip_addr** | IP-Addr | 1 | The representation of one or more IP addresses (either version 4 or version 6). |
| 15 | **ip_connection** | IP-Connection | 1 | A network connection that originates from a source and is addressed to a destination. |
| 13 | **mac_addr** | MAC-Addr | 1 | A single Media Access Control (MAC) address. |
| 17 | **process** | Process | 1 | Common properties of an instance of a computer program as executed on an operating system. |
| 25 | **properties** | Properties | 1 | Data attribute associated with an actuator |
| 19 | **uri** | URI | 1 | A uniform resource identifier (URI). |
| 1099 | **exp** | exp:Target | 1 | Targets defined in the Experimental Schema Features Profile |

**_Type: Actuator (Choice)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1099 | **exp** | exp:Specifiers | 1 | Specifiers defined in Experimental Schema Features profile. |

**_Type: Args (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **start_time** | Date-Time | 0..1 | The specific date/time to initiate the action |
| 2 | **stop_time** | Date-Time | 0..1 | The specific date/time to terminate the action |
| 3 | **duration** | Duration | 0..1 | The length of time for an action to be in effect |
| 4 | **response_requested** | Response-Type | 0..1 | The type of response required for the action |

**_Type: OpenC2-Response (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **status** | Status-Code | 0..1 | An integer status code (Duplicates message status code) |
| 2 | **status_text** | String | 0..1 | A free-form human-readable description of the response status |
| 3 | **strings** | String | 0..n | Generic set of string values |
| 4 | **ints** | Integer | 0..n | Generic set of integer values |
| 5 | **kvps** | KVP | 0..n | Generic set of key:value pairs |
| 6 | **versions** | Version | 0..n | Supported OpenC2 Language versions |
| 7 | **profiles** | jadn:Uname | 0..n | List of profiles supported by this actuator |
| 8 | **schema** | jadn:Schema | 0..1 | Syntax of the OpenC2 language elements supported by this actuator |
| 9 | **pairs** | Action-Targets | 0..n | List of targets applicable to each supported action |
| 10 | **rate_limit** | Number | 0..1 | Maximum number of requests per minute supported by design or policy |
| 1099 | **exp** | exp:Results | 0..1 | Response data defined in Experimental Schema Features profile |

**_Type: Status-Code (Enumerated.ID)_**

| ID | Description |
| ---: | :--- |
| 102 | Processing -- an interim response used to inform the client that the server has accepted the request but not yet completed it. |
| 200 | OK -- the request has succeeded. |
| 301 | Moved Permanently -- The target resource has been assigned a new permanent URI |
| 400 | Bad Request -- the consumer cannot process the request due to something that is perceived to be a client error (e.g., malformed request syntax.) |
| 401 | Unauthorized -- the request lacks valid authentication credentials for the target resources or authorization has been refused for the submitted credentials. |
| 403 | Forbidden -- the consumer understood the request but refuses to authorize it. |
| 404 | Not Found -- the consumer has not found anything matching the request. |
| 500 | Internal Error -- the consumer encountered an unexpected condition that prevented it from fulfilling the request. |
| 501 | Not Implemented -- the consumer does not support the functionality required to fulfill the request. |
| 503 | Service Unavailable -- the consumer is currently unable to handle the request due to a temporary overloading or maintenance. |

**_Type: Artifact (Record)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **mime_type** | String | 0..1 | Permitted values specified in the IANA Media Types registry |
| 2 | **payload** | Payload | 0..1 | choice of literal content or URL to obtain content |
| 3 | **hashes** | Hashes | 0..1 | Specifies a dictionary of hashes for the contents of the payload |

**_Type: Device (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **hostname** | Hostname | 1 | A hostname that can be used to connect to this device over a network |
| 2 | **description** | String | 0..1 | A human-readable description of the purpose, relevance, and/or properties of the device |
| 3 | **device_id** | String | 0..1 | An identifier that refers to this device within an inventory or management system |

**_Type: Domain-Name_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Domain-Name | String (hostname) | RFC 1034, section 3.5 |

**_Type: Email-Addr_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Email-Addr | String (email) | Email address, RFC 5322, section 3.4.1 |

**_Type: Features_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Features | ArrayOf(Feature) [0..n] | A target used to query Actuator for its supported capabilities |

**_Type: File (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **name** | String | 0..1 | The name of the file as defined in the file system |
| 2 | **path** | String | 0..1 | The absolute path to the location of the file in the file system |
| 3 | **hashes** | Hashes | 0..1 | One or more cryptographic hash codes of the file contents |

**_Type: IP-Addr_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| IP-Addr | Binary (ip-addr) | 32 bit IPv4 address or 128 bit IPv6 address |

**_Type: IP-Connection (Record)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **src_addr** | IP-Addr | 0..1 | source address |
| 2 | **src_port** | Port | 0..1 | source TCP/UDP port number |
| 3 | **dst_addr** | IP-Addr | 0..1 | destination address |
| 4 | **dst_port** | Port | 0..1 | destination TCP/UDP port number |
| 5 | **protocol** | L4-Protocol | 0..1 | Protocol (IPv4) / Next Header (IPv6) |

**_Type: MAC-Addr_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| MAC-Addr | Binary | Media Access Code / Extended Unique Identifier - 48 or 64 bit address |

**_Type: Process (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **pid** | Integer | 0..1 | Process ID of the process |
| 2 | **name** | String | 0..1 | Name of the process |
| 3 | **cwd** | String | 0..1 | Current working directory of the process |
| 4 | **executable** | File | 0..1 | Executable that was executed to start the process |
| 5 | **parent** | Process | 0..1 | Process that spawned this one |
| 6 | **command_line** | String | 0..1 | The full command line invocation used to start this process, including all arguments |

**_Type: Properties_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Properties | ArrayOf(String) | A list of names that uniquely identify properties of an actuator |

**_Type: URI_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| URI | String (uri) | Uniform Resource Identifier |

**_Type: Message-Type (Enumerated)_**

| ID | Name | Description |
| ---: | --- | :--- |
| 0 | **notification** | A message that does not solicit a response |
| 1 | **request** | A message for which a response is requested |
| 2 | **response** | A message containing a response to a request |

**_Type: Request-Id_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Request-Id | Binary | A value of up to 128 bits that uniquely identifies a particular command |

**_Type: Date-Time_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Date-Time | Integer | Milliseconds since 00:00:00 UTC, 1 January 1970. |

**_Type: Duration_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Duration | Integer | Milliseconds |

**_Type: Hashes (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **md5** | Binary | 0..1 | MD5 hash as defined in RFC3121 |
| 4 | **sha1** | Binary | 0..1 | SHA1 hash as defined in RFC3174 |
| 6 | **sha256** | Binary | 0..1 | SHA256 as defined in RFC6234 |

**_Type: Hostname_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Hostname | String | A legal Internet host name as specified in RFC 1123 |

**_Type: L4-Protocol (Enumerated)_**

| ID | Name | Description |
| ---: | --- | :--- |
| 1 | **icmp** | Internet Control Message Protocol - RFC 792 |
| 6 | **tcp** | Transmission Control Protocol - RFC 793- |
| 17 | **udp** | User Datagram Protocol - RFC 768 |
| 132 | **sctp** | Stream Control Transmission Protocol - RFC 4960 |

**_Type: Payload (Choice)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **bin** | Binary | 1 | Specifies the data contained in the artifact. |
| 2 | **url** | URI | 1 | MUST be a valid URL that resolves to the un-encoded content |

**_Type: Port_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Port | Integer [0..65535] | Transport Protocol Port Number, RFC 6335 |

**_Type: Feature (Enumerated)_**

| ID | Name | Description |
| ---: | --- | :--- |
| 1 | **versions** | List of OpenC2 language versions supported by this actuator |
| 2 | **profiles** | List of profiles supported by this actuator |
| 3 | **schema** | Definition of the command syntax supported by this actuator |
| 4 | **pairs** | List of supported actions and applicable targets |
| 5 | **rate_limit** | Maximum number of supported requests per minute |

**_Type: Response-Type (Enumerated)_**

| ID | Name | Description |
| ---: | --- | :--- |
| 0 | **none** | No response |
| 1 | **ack** | Respond when command received |
| 2 | **status** | Respond with progress toward command completion |
| 3 | **complete** | Respond when all aspects of command completed |

**_Type: Version_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Version | String | Major.Minor version number |

**_Type: KVP (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | String | 1 | key -- name of this item |
| 2 | String | 1 | value -- string value of this item |

**_Type: Action-Targets (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Action | 1 | action -- An action supported by this actuator |
| 2 | Target.* | 1..n | targets -- List of targets applicable to this action |

**_Type: exp:Target (Choice)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **date_time_rfc3339** | exp:DT-RFC3339 | 1 | Time value serialized in RFC3339 format. |
| 2 | **data_time_rfc822** | exp:DT-RFC822 | 1 | Time value serialized in email format. |
| 3 | **ipv4_addr_x** | exp:IPv4-Hex | 1 | IPv4 address serialized as hex: 'C0A800FE' |
| 4 | **ipv4_addr_b64** | exp:IPv4-Base64url | 1 | IPv4 address serialized as Base64-url: 'wKgA_g' |
| 5 | **ipv4_addr_s** | exp:IPv4-String | 1 | IPv4 address as type-specific string (dotted-decimal): '192.168.0.254' |

**_Type: exp:DT-RFC3339_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| exp:DT-RFC3339 | Integer.s:rfc3339 (date_time) |  |

**_Type: exp:DT-RFC822_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| exp:DT-RFC822 | Integer.s:rfc822 (date_time) |  |

**_Type: exp:IPv4-Hex_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| exp:IPv4-Hex | Binary.x (ipv4) |  |

**_Type: exp:IPv4-Base64url_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| exp:IPv4-Base64url | Binary (ipv4) |  |

**_Type: exp:IPv4-String_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| exp:IPv4-String | Binary.s:ipv4 (ipv4) |  |

**_Type: exp:Args (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |

**_Type: exp:Specifiers (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |

**_Type: exp:Results (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **knps** | exp:KNP | 0..n | Generic set of key:number pairs. |

**_Type: exp:KNP (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | String | 1 | key -- name of this item |
| 2 | Number | 1 | value -- numeric value of this item |

**_Type: jadn:Schema (Record)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **meta** | jadn:Meta | 1 | Information about this schema module |
| 2 | **types** | jadn:Type | 1..n | Types defined in this schema module |

**_Type: jadn:Meta (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **module** | jadn:Uname | 1 | Schema unique name/version |
| 2 | **patch** | String | 0..1 | Patch version |
| 3 | **title** | String | 0..1 | Title |
| 4 | **description** | String | 0..1 | Description |
| 5 | **imports** | jadn:Import | 0..n | Imported schema modules |
| 6 | **exports** | jadn:Identifier | 0..n | Data types exported by this module |
| 7 | **bounds** | jadn:Bounds | 0..1 | Schema-wide upper bounds |

**_Type: jadn:Import (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | jadn:Nsid | 1 | nsid -- A short local identifier (namespace id) used within this module to refer to the imported module |
| 2 | jadn:Uname | 1 | uname -- Unique name of imported module |

**_Type: jadn:Bounds (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Integer | 1 | max_msg -- Maximum serialized message size in octets or characters |
| 2 | Integer | 1 | max_str -- Maximum string length in characters |
| 3 | Integer | 1 | max_bin -- Maximum binary length in octets |
| 4 | Integer | 1 | max_fields -- Maximum number of elements in ArrayOf |

**_Type: jadn:Type (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | jadn:Identifier | 1 | tname -- Name of this datatype |
| 2 | jadn:JADN-Type.* | 1 | btype -- Base type.  Enumerated value derived from list of JADN data types |
| 3 | jadn:Option | 1..n | opts -- Type options |
| 4 | String | 1 | desc -- Description of this data type |
| 5 | jadn:JADN-Type | 1..n | fields -- List of fields for compound types.  Not present for primitive types |

**_Type: jadn:JADN-Type (Choice)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **Binary** | Null | 1 | Octet (binary) string |
| 2 | **Boolean** | Null | 1 | True or False |
| 3 | **Integer** | Null | 1 | Whole number |
| 4 | **Number** | Null | 1 | Real number |
| 5 | **Null** | Null | 1 | Nothing |
| 6 | **String** | Null | 1 | Character (text) string |
| 7 | **Array** | jadn:FullField | 1..n | Ordered list of unnamed fields |
| 8 | **ArrayOf** | Null | 1 | Ordered list of fields of a specified type |
| 9 | **Choice** | jadn:FullField | 1..n | One of a set of named fields |
| 10 | **Enumerated** | jadn:EnumField | 1..n | One of a set of id:name pairs |
| 11 | **Map** | jadn:FullField | 1..n | Unordered set of named fields |
| 12 | **Record** | jadn:FullField | 1..n | Ordered list of named fields |

**_Type: jadn:EnumField (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Integer | 1 | Item ID |
| 2 | String | 1 | Item name |
| 3 | String | 1 | Item description |

**_Type: jadn:FullField (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Integer | 1 | Field ID or ordinal position |
| 2 | jadn:Identifier | 1 | Field name |
| 3 | jadn:Identifier | 1 | Field type |
| 4 | jadn:Options | 1 | Field options |
| 5 | String | 1 | Field description |

**_Type: jadn:Identifier_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| jadn:Identifier | String [1..32] | A string starting with an alpha char followed by zero or more alphanumeric / underscore / dash chars |

**_Type: jadn:Nsid_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| jadn:Nsid | String [1..8] | Namespace ID - a short identifier |

**_Type: jadn:Uname_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| jadn:Uname | String [1..100] | Unique name (e.g., of a schema) - typically a set of Identifiers separated by forward slashes |

**_Type: jadn:Options_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| jadn:Options | ArrayOf(jadn:Option) [0..10] | Options list may be empty but may not be omitted |

**_Type: jadn:Option_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| jadn:Option | String [1..100] | Option string: 1st char = option id |
