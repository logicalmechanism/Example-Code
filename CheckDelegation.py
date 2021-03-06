import requests
import os
headers = {'Project_id': "blockfrost_id_here}
base = 'https://cardano-mainnet.blockfrost.io/api/v0/'
pool_id = 'pool_id_here'

def CheckUserStatus(addr):
    """
    addr - String - This is any public address associated with a stake key.
    
    This checks if a public addressed is delegated to a pool id in some epoch.
    
    This returns the stake address, the amount staked, and a boolean flag.
    """
    # Default values.
    verified = False
    amt_ada = 0
    # get the current epoch number
    last_epoch = 'epochs/latest'
    last_epoch_resp = requests.get(base+last_epoch, headers=headers)
    epoch_no = last_epoch_resp.json()['epoch_no']
    # Get the stake address of the public address
    address = 'addresses/{}'
    address = address.format(addr)
    address_resp = requests.get(base+address, headers=headers)
    stake_address = address_resp.json()['stake_address']
    # Get current delegators to pool and cross reference
    stake_distribution = "epochs/{}/stakes/{}".format(epoch_no, pool_id)
    stake_distro_resp = requests.get(base+stake_distribution, headers=headers)
    # Cross check the stake address with current delegations.
    for stake in stake_distro_resp.json():
        if stake['stake_address'] == stake_address:
            amt_ada = int(stake['amount'])/1000000
            verified = True
    # return the user pub stake, amt, verify
    return stake_address, amt_ada, verified
