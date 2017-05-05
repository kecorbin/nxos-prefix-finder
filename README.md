# nxos-prefix-finder

## Introduction

This utility provides a flask based website which allows a user to input a IPv4 prefix.  The utility will then establish a NetConf session with an NX-OS device, and report back which VRF(s) the prefix was found in.

## API

The utility also provides a REST API to get this information as well

### Request
```
curl 127.0.0.1:5000/api/prefix?prefix=192.168.3.0/24
```
### Response
```
{
    "vrfs": [
        "vrf3"
    ]
}
```
