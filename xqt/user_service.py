from boa.interop.Neo.Runtime import CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.builtins import concat
from boa.interop.Neo.Storage import *
from xqt.common import operation_key

OnUserRegistration = RegisterAction('user_registration', 'address')
OnUserUpdate = RegisterAction('user_update', 'address')
OnUserDeletion = RegisterAction('user_delete', 'address')


USER_INFO_KEY = b'user_info'
USER_PROP_KEY = b'user_props'

args_incorrect_len = 'incorrect args length'

def handle_user(ctx, operation, args):
    if operation == 'user_info':
        if len(args) == 1:
            if len(args[0]) != 20:
                return 'Incorrect address format'
            return get_user_info(ctx,args[0])
        return args_incorrect_len

    elif operation == 'user_properties':
        if len(args) == 1:
            if len(args[0]) != 20:
                return 'Incorrect address format'
            return get_properties_user(ctx,args[0])
        return args_incorrect_len

    elif operation == 'register_user':
        if len(args) == 2:
            if len(args[0]) != 20:
                return 'Incorrect address format'
            return user_info_registration(ctx, args[0],args[1])
        return args_incorrect_len

    elif operation == 'update_user':
        if len(args) == 2:
            if len(args[0]) != 20:
                return 'Incorrect address format'
            return user_info_update(ctx, args[0],args[1])
        return args_incorrect_len

    elif operation == 'delete_user':
        if len(args) == 1:
            if len(args[0]) != 20:
                return 'Incorrect address format'
            return user_deletion(ctx, args[0])
        return args_incorrect_len
        
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

    if user_info:
        print('The user is already registered')
        return False

    key = operation_key(USER_INFO_KEY,address)

    Put(ctx,key,user_hash)

    OnUserRegistration(address)

    return True

def user_info_update(ctx, address, user_hash):
    isOwner = CheckWitness(address)
    user_info = get_user_info(ctx,address)

    if isOwner == False:
        print('Contract caller different from address')
        return False

    if user_info == b'':
        print('The user is not registered')
        return False

    if user_info == user_hash:
        print('The user is already registered')
        return False

    key = operation_key(USER_INFO_KEY,address)

    Put(ctx,key,user_hash)

    OnUserDeletion(address)

    return True

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

    OnUserDeletion(address)

    return True
