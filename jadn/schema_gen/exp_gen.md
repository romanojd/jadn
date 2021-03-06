<!-- Generated from schema\exp.jadn, Mon Mar 18 17:59:50 2019-->
## Schema
| . | . |
| ---: | :--- |
| **title:** | Experimental Schema Features |
| **module:** | oasis-open.org/openc2/oc2ls-exp/v1.0 |
| **patch:** | 0 |
| **description:** | Profile used to test schema features not used in existing language or profiles |
| **exports:** | Target, Specifiers, Args, Results |

**_Type: Target (Choice)_**

| ID | Name | Type | # | Description |
| ---: | :--- | :--- | ---: | :--- |
| 1 | **hashes** | Hashes | 1 | Hash values displayed as hex |
| 2 | **ipv4_addr_s** | IPv4-String | 1 | IPv4 address displayed as type-specific string (dotted-decimal): '192.168.0.254' |
| 3 | **ipv4_addr_x** | IPv4-Hex | 1 | IPv4 address displayed as hex: 'C0A800FE' |
| 4 | **ipv4_addr_b64** | IPv4-Base64url | 1 | IPv4 address displayed as Base64-url: 'wKgA_g' |
| 5 | **ipv6_addr_s** | IPv6-String | 1 | IPv6 address displayed as type-specific string (colon-hex): '' |
| 6 | **ipv6_addr_x** | IPv6-Hex | 1 | IPv6 address displayed as hex: '' |
| 7 | **ipv6_addr_b64** | IPv6-Base64url | 1 | IPv6 address displayed as Base64-url: '' |
| 8 | **ipv4_net** | IPv4-Net | 1 | IPv4 Network CIDR string |
| 9 | **ipv6_net** | IPv6-Net | 1 | IPv6 Network CIDR string |

**_Type: Hashes (Map)_**

| ID | Name | Type | # | Description |
| ---: | :--- | :--- | ---: | :--- |
| 1 | **md5** | Bin-128 | 0..1 | MD5 hash as defined in RFC3121 |
| 4 | **sha1** | Bin-160 | 0..1 | SHA1 hash as defined in RFC3174 |
| 6 | **sha256** | Bin-256 | 0..1 | SHA256 as defined in RFC6234 |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **Bin-128** | Binary.x [16..16] | 128 bit value, hex display |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **Bin-160** | Binary.x [20..20] | 160 bit value, hex display |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **Bin-256** | Binary.x [32..32] | 256 bit value, hex display |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **IPv4-Hex** | Binary.x [4..4] | Value must be 32 bits [4..4].  Value displayed in hex (Binary.x) |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **IPv4-Base64url** | Binary [4..4] | Value must be 32 bits [4..4].  Value displayed in base64url (Binary) default |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **IPv4-String** | Binary.ipv4-addr [4..4] | Value must be 32 bits [4..4].  Value displayed in ipv4 dotted-decimal (Binary.ipv4-addr) |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **IPv6-Hex** | Binary.x [16..16] | Value must be 128 bits [16..16].  Value displayed in hex (Binary.x) |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **IPv6-Base64url** | Binary [16..16] | Value must be 128 bits [16..16].  Value displayed in base64url (Binary) default |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **IPv6-String** | Binary.ipv6-addr [16..16] | Value must be 128 bits [16..16].  Value displayed in ipv6 colon-hex (Binary.ipv6-addr) |

**_Type: IPv4-Net (Array.ipv4-net)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Binary | 1 | **address** |
| 2 | Integer | 1 | **prefix_len** |

**_Type: IPv6-Net (Array.ipv6-net)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | Binary | 1 | **address** |
| 2 | Integer | 1 | **prefix_len** |

**_Type: Args (Map)_**

| ID | Name | Type | # | Description |
| ---: | :--- | :--- | ---: | :--- |

**_Type: Specifiers (Map)_**

| ID | Name | Type | # | Description |
| ---: | :--- | :--- | ---: | :--- |

**_Type: Results (Map)_**

| ID | Name | Type | # | Description |
| ---: | :--- | :--- | ---: | :--- |
| 1 | **knps** | KNP | 0..* | Generic set of key:number pairs. |
| 42 | **battery** | Battery-Properties | 0..1 | Set of custom properties defined for an energy storage device |

**_Type: KNP (Array)_**

| ID | Type | # | Description |
| ---: | :--- | ---: | :--- |
| 1 | String | 1 | **key** - name of this item |
| 2 | Number | 1 | **value** - numeric value of this item |

**_Type: Battery-Properties (Map)_**

| ID | Name | Type | # | Description |
| ---: | :--- | :--- | ---: | :--- |
| 7 | **voltage** | Integer | 0..1 | Battery output voltage (millivolts) |
| 18 | **charge** | Percentage | 0..1 | State of charge (percent) |
| 26 | **model** | String | 0..1 | Product name for this device |


| Type Name | Type Definition | Description |
| :--- | :--- | :--- |
| **Percentage** | Number [0..100] | Real number in the range 0.0-100.0 |
