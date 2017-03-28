# Kerberos 471

A Python implementation of the Kerberos Authentication Protocol

* Authors: 
  * Nathaniel Christianson ([natetc95@email.arizona.edu](mailto:natetc95@email.arizona.edu))
* University of Arizona
* ECE 471

## Description

Written in Python 2.7.11

A lot of my knowledge of the protocol stems from this [site](http://www.zeroshell.org/kerberos/Kerberos-operation/)

Uses a lot of function from the pyCrypto library [link](https://www.dlitz.net/software/pycrypto/)

## Use

Navigate to the directory where the project was unzipped, then in the command line, run:

    python runproject.py
    
This will spawn four command lines:

 * Client
 * Authentication Server (AS)
 * Ticket Granting Server (TGS)
 * Principal Service


## License (MIT)

Copyright 2017 Nathaniel Christianson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
