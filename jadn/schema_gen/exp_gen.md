<!-- Generated from schema\exp.jadn, Tue Nov 13 13:21:11 2018-->
## Schema
| . | . |
| ---: | :--- |
| **title:** | Experimental Schema Features |
| **module:** | oasis-open.org/openc2/oc2ls/v1.0/experimental |
| **patch:** | 0 |
| **description:** | Profile used to test schema features not used in existing language or profiles |
| **exports:** | Target, Specifiers, Args, Results |

**_Type: Target (Choice)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **ipv4_addr_s** | IPv4-String | 1 | IPv4 address as type-specific string (dotted-decimal): '192.168.0.254' |
| 2 | **ipv4_addr_x** | IPv4-Hex | 1 | IPv4 address serialized as hex: 'C0A800FE' |
| 3 | **ipv4_addr_b64** | IPv4-Base64url | 1 | IPv4 address serialized as Base64-url: 'wKgA_g' |
| 4 | **ipv4_addr_s** | IPv6-String | 1 | IPv6 address as type-specific string (dotted-decimal): '192.168.0.254' |
| 5 | **ipv4_addr_x** | IPv6-Hex | 1 | IPv6 address serialized as hex: 'C0A800FE' |
| 6 | **ipv4_addr_b64** | IPv6-Base64url | 1 | IPv6 address serialized as Base64-url: 'wKgA_g' |

**_Type: IPv4-Hex_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| IPv4-Hex | Binary.x (ipv4) |  |

**_Type: IPv4-Base64url_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| IPv4-Base64url | Binary (ipv4) |  |

**_Type: IPv4-String_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| IPv4-String | Binary.s:ipv4 (ipv4) |  |

**_Type: Args (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |

**_Type: Specifiers (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |

**_Type: Results (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **knps** | KNP | 0..n | Generic set of key:number pairs. |

**_Type: KNP (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | String | 1 | key -- name of this item |
| 2 | Number | 1 | value -- numeric value of this item |
