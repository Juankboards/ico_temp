from boa.interop.Neo.Runtime import CheckWitness
from boa.builtins import concat
from boa.interop.Neo.Storage import *
from xqt.common import operation_key

USER_INFO_KEY = b'user_info'
USER_PROP_KEY = b'user_props'

def handle_user(ctx, operation, args):
    if operation == 'user_info':
        return get_user_info(ctx,args[0])
    elif operation == 'user_properties':
        return get_properties_user(ctx,args[0])
    elif operation == 'register_user':
        return user_info_registration(ctx, args[0],args[1])
    elif operation == 'update_user':
        return user_info_registration(ctx, args[0],args[1])
    elif operation == 'delete_user':
        return user_deletion(ctx, args[0])
    return False

def get_user_info(ctx, address):
    key = operation_key(USER_INFO_KEY,address)
    return Get(ctx,key)

def get_properties_user(ctx, address):
    key = operation_key(USER_PROP_KEY,address)
    return Get(ctx,key)

def user_info_registration(ctx, address, user_hash):
    isOwner = CheckWitness(address)
    user_info = get_user_info(ctx,address)

    if isOwner == False:
        print('Contract caller different from address')
        return False

    if user_info == user_hash:
        print('The user is already registered')
        return False

    key = operation_key(USER_INFO_KEY,address)
    return Put(ctx,key,user_hash)

def user_deletion(ctx, address):
    isOwner = CheckWitness(address)

    if isOwner == False:
        print('Contract caller different from address')
        return False

    user_props = get_properties_user(ctx,address)

    if user_props != b'':
        print('Delete properties first')
        return False

    key = operation_key(USER_INFO_KEY,address)
    Delete(ctx, key)

    return True
