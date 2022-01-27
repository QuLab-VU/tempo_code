#!/bin/bash

USER=username

stty -echo
kinit $USER@VUDS.VANDERBILT.EDU | tee >( read -s password )
stty echo
printf "\n"

klist
aklog accre.vanderbilt.edu
tokens
cd /afs/accre.vanderbilt.edu/quaranta
