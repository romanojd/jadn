<!-- Generated from schema\exp.jadn, Tue Nov 13 14:36:02 2018-->
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
| 1 | **hashes** | Hashes | 1 | Hash values serialized as hex |
| 2 | **ipv4_addr_s** | IPv4-String | 1 | IPv4 address as type-specific string (dotted-decimal): '192.168.0.254' |
| 3 | **ipv4_addr_x** | IPv4-Hex | 1 | IPv4 address serialized as hex: 'C0A800FE' |
| 4 | **ipv4_addr_b64** | IPv4-Base64url | 1 | IPv4 address serialized as Base64-url: 'wKgA_g' |
| 5 | **ipv6_addr_s** | IPv6-String | 1 | IPv6 address as type-specific string (dotted-decimal): '' |
| 6 | **ipv6_addr_x** | IPv6-Hex | 1 | IPv6 address serialized as hex: '' |
| 7 | **ipv6_addr_b64** | IPv6-Base64url | 1 | IPv6 address serialized as Base64-url: '' |

**_Type: Hashes (Map)_**

| ID | Name | Type | # | Description |
| ---: | --- | :--- | ---: | :--- |
| 1 | **md5** | Bin-128 | 0..1 | MD5 hash as defined in RFC3121 |
| 4 | **sha1** | Bin-160 | 0..1 | SHA1 hash as defined in RFC3174 |
| 6 | **sha256** | Bin-256 | 0..1 | SHA256 as defined in RFC6234 |

**_Type: Bin-128_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Bin-128 | Binary.x [16..16] | 128 bit value, hex display |

**_Type: Bin-160_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Bin-160 | Binary.x [20..20] | 160 bit value, hex display |

**_Type: Bin-256_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| Bin-256 | Binary.x [32..32] | 256 bit value, hex display |

**_Type: IPv4-Hex_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| IPv4-Hex | Binary.x (ipv4) | Value must be 32 bits (ipv4).  Value displayed in hex (Binary.x) |

**_Type: IPv4-Base64url_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| IPv4-Base64url | Binary (ipv4) | Value must be 32 bits (ipv4).  Value displayed in base64url (Binary) default |

**_Type: IPv4-String_**

| Type Name | Base Type | Description |
| :--- | :--- | :--- |
| IPv4-String | Binary.s:ipv4 (ipv4) | Value must be 32 bits (ipv4).  Value displayed in ipv4 dotted decimal (Binary.s:ipv4) |

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
