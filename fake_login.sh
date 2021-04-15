#!/bin/bash
set -e

PASSWORD="123"

##################################################################
# A User Wants to Create a LOGIN
##################################################################

# Generate a v.key and s.key for a new user
echo "New User: Creating v.key and s.key"
cardano-cli address key-gen --normal-key --verification-key-file 'v.key' --signing-key-file 's.key'

# Store v.key in the DB
# Locally store an encrypted s.key on the user's computer with user's password
echo "Encrypting the s.key"
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -salt -in 's.key' -out 's.key.enc' -k ${PASSWORD}
rm 's.key'


##################################################################
# A User Wants to Use Their LOGIN
##################################################################


# Ask for password -> decrypt s.key -> create test.key -> if test.key == v.key then login else deny

echo "Decrypting the s.key"
# openssl enc -aes-256-cbc -d -in 's.key.enc' -out 's.key' -k ${PASSWORD}
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -salt -d -in 's.key.enc' -out 's.key' -k ${PASSWORD}

# The password decrypts the locally stored s.key and attempts to recreate v.key
echo "Attempting to recreate the v.key"
cardano-cli key verification-key --signing-key-file 's.key' --verification-key-file 'test.key'
rm 's.key'

original=$(jq  '.cborHex' 'v.key')
tester=$(jq  '.cborHex' 'test.key')

if [ "${original}" == "${tester}" ]; then
    echo "Log in"
else
    echo "Deny"
fi