#!/bin/bash

ABS_PATH=`readlink -f "$1"`
EMAIL=$2

if [[ $ABS_PATH != /home/* ]] && [[ $ABS_PATH != /groups/* ]] && [[ $ABS_PATH != /omaha-beach/* ]] ;
then
    echo "Destination dir is invalid. Aborting."
    exit 1
fi

if [ ! -f $ABS_PATH ]; then
    echo "$ABS_PATH not found. Aborting."
    exit 1
fi

current_owner=$(ls -l $ABS_PATH | awk '{print $3}')
if [[ $current_owner != "galaxy" ]] && [[ $current_owner != "milky" ]]
then
    echo "Unexpected current owner. Aborting."
    exit 1
fi

# Find login from ldap server. Adapt with your server
uid=`ldapsearch -H ldap://ldapaddress -b 'dc=organization,dc=org' -x mail="$2" uid | grep "uid:" | cut -f2 -d' '`
if [ -z "$uid" ]; then
    echo "Could not find uid for $2. Aborting."
    exit 1
fi

chown $uid: $ABS_PATH

