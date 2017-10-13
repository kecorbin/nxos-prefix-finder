# nxos-prefix-finder

## Introduction

This utility provides a flask based website which allows a user to input a IPv4 prefix.  The utility will then establish a NetConf session with an NX-OS device, and report back which VRF(s) the prefix was found in.

## Screenshot

![screenshot](/static/img/screenshot.png)

## Installation

```
git clone https://github.com/kecorbin/nxos-prefix-finder
cd nxos-prefix-finder
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

```
Note: If you do not have virtualenv installed use pip to install

`pip install virtualenv`

## Configuration

Modify [config.yaml](./config.yaml) with the appropriate values for your environment

## Running

Execute the script

`python app.py`

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
