#!/bin/bash

: $(git -c credential.helper= -c core.quotepath=false -c log.showSignature=false checkout $1)