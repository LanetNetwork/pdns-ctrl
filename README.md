pdns-ctrl
=========

Description
-----------

Daemon to control PowerDNS Recursor via HTTP.

Basics
------

pdns-ctrl is built on top of pure Python 2.7 with BaseHTTPServer and back-ported
python-ipaddress library. Currently it allows wiping DNS cache only.

pdns-ctrl could be queried by any HTTP client, for example, cURL.

Usage
-----

### Configuration

pdns-ctrl use one config: pdns-ctrl.ini. It describes global parameters like listening socket
as well as ACLs for different users.

#### pdns-ctrl.ini

```ini
[global]
host=example.com
port=9000
helper=/usr/bin/rec_control

[admin]
ip=10.0.0.0/8
token=somehugeandsecrettoken
```

* `global` section specifies listening socket and path to PowerDNS Recursor helper;
* other sections describe user access (see below).

User section's name corresponds to client ID, and the section itself consists of:

* `ip` is permitted client subnet;
* `token` is client secret token.

### Querying

To query pdns-ctrl daemon client must send GET request to it as shown below:

`curl http://example.com:9000/wipe-cache\?id\=admin\&token\=somehugeandsecrettoken\&host\=kernel.org`

This query will wipe DNS cache for kernel.org domain. One domain per request is permitted.

Runtime prerequisites
---------------------

* python (tested with 2.7.5)
* python-ipaddress (tested with 1.0.7)

Distribution and Contribution
-----------------------------

Distributed under terms and conditions of GNU GPL v3 (only).

The following people are involved in development:

* Oleksandr Natalenko &lt;o.natalenko@lanet.ua&gt;

Mail them any suggestions, bugreports and comments.
