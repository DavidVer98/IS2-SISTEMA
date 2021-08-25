#!/bin/bash

latesttag=$(git describe --tags)


git checkout tags/$latesttag -b tags

