magicpacket
===========

WOL magic packet sender command by Python.

Download Windows binary from `/dist`.


Usage
-----
    
    usage: magicpacket.py [-h] [--version] [--verbose]
                          [--destination hostname[:port]] [--count COUNT]
                          [--interval SECONDS]
                          MAC address
    
    Sending WOL magic packet library
    
    positional arguments:
      MAC address
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --verbose, -v         increase log level
      --destination hostname[:port], --dest hostname[:port], -d hostname[:port]
                            destination address (default=255.255.255.255:7)
      --count COUNT, -c COUNT
                            repeat count (default=1)
      --interval SECONDS, -i SECONDS
                            interval of repeat (default=1.0 sec)
