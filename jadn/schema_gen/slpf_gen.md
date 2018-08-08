<!-- Generated from schema\slpf.jadn, Mon Jul 23 15:14:16 2018-->
## Schema
 .  | .
 ---:|:---
title: |Stateless Packet Filtering
module: |oasis-open.org/openc2/v1.0/ap-slpf
version: |wd02
description: |Data definitions for Stateless Packet Filtering (SLPF) functions
exports: |Target, Specifiers, Args, Results

## 3.2 Structure Types

### 3.2.1 Target
SLPF targets

**Target (Choice)**

ID|Name|Type|Description
---:|:---|:---|:---
1|access_rules|Rules|Return the requested access rules in the response

### 3.2.2 Rules
Specifiers for the access_rules target

**Rules (Map)**

ID|Name|Type|#|Description
---:|:---|:---|---:|:---
1|allow_rules|Rule-Target|0..1|Return specified allow rules
2|deny_rules|Rule-Target|0..1|Return specified deny rules

### 3.2.3 Rule-Target
Specifier for an access rule

**Rule-Target (Choice)**

ID|Name|Type|Description
---:|:---|:---|:---
1|all|Null|Any rules
2|ip_addr|..:IP-Addr|Rules affecting the specified address
3|ip_connection|..:IP-Connection|Rules affecting the specified 5-tuple

### 3.2.4 Specifiers
SLPF actuator specifiers

**Specifiers (Map)**

ID|Name|Type|#|Description
---:|:---|:---|---:|:---
1|nfv_id|String|1|Identifier of a virtualized packet filter

### 3.2.5 Args
SLPF command arguments

**Args (Map)**

ID|Name|Type|#|Description
---:|:---|:---|---:|:---
1|block-method|Block-Method|1|How to handle denied packets
2|insert|Integer|1|Position of a rule in access list

### 3.2.6 Block-Method


**Block-Method (Enumerated)**

ID|Name|Description
---:|:---|:---
1|drop|
2|reject|
3|deceive|

### 3.2.7 Results
SLPF results

**Results (Map)**

ID|Name|Type|#|Description
---:|:---|:---|---:|:---
1|access_rules|Rule-Item|0..1|Access rules matching a query

### 3.2.8 Rule-Item


**Rule-Item (Array)**

ID|Type|#|Description
---:|:---|---:|:---
1|Integer|1|"id": Rule identifier within a ruleset
2|Rule-Action|1|"action": Allow or Deny
3|Rule-Target|1|"rule": Matching criterion

### 3.2.9 Rule-Action


**Rule-Action (Enumerated)**

ID|Name|Description
---:|:---|:---
1|allow|Matching packets are permitted
2|deny|Matching packets are blocked

## 3.3 Primitive Types


Name|Type|Description
:---|:---|:---
