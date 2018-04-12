from boa.interop.Neo.Runtime import CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.builtins import concat
from boa.interop.Neo.Storage import *
from xqt.common import *
from xqt.serialization import deserialize_bytearray, serialize_array
from xqt.user_service import USER_PROP_KEY, get_properties_user, get_user_info

OnPropRegist = RegisterAction('prop_registration', 'prop_id')
OnPropUpdate = RegisterAction('prop_update', 'prop_id')
OnPropDeletion = RegisterAction('prop_delete', 'prop_id')

PROP_INFO_KEY = b'prop_info'
PROP_OWNER_KEY = b'prop_owner'

args_incorrect_len = 'incorrect args length'

def handle_prop(ctx, operation, args):
    if operation == 'prop_info':
        if len(args) == 1:
            return get_prop_info(ctx,args[0])
        return args_incorrect_len
    elif operation == 'prop_owner':
        if len(args) == 1:
            return get_prop_owner(ctx,args[0])
        return args_incorrect_len
    elif operation == 'register_prop':
        if len(args) == 3:
            if len(args[2]) != 20:
                return 'Incorrect address format'
            return prop_info_registration(ctx, args[0],args[1],args[2])
        return args_incorrect_len
    elif operation == 'update_prop':
        if len(args) == 3:
            if len(args[2]) != 20:
                return 'Incorrect address format'
            return prop_info_update(ctx, args[0],args[1],args[2])
        return args_incorrect_len
    elif operation == 'delete_prop':
        if len(args) == 1:
            return prop_deletion(ctx, args[0])
        return args_incorrect_len
    return False

def get_prop_info(ctx, id):
    key = operation_key(PROP_INFO_KEY,id)
    return Get(ctx,key)

def get_prop_owner(ctx, id):
    key = operation_key(PROP_OWNER_KEY,id)
    return Get(ctx,key)

def prop_info_registration(ctx, id,hash,address):
    user_info = get_user_info(ctx,address)

    if user_info == b'':
        print('Create a Quarteria account before register a property')
        return False

    isOwner = CheckWitness(address)
    prop_owner = get_prop_owner(ctx,id)
    prop_info = get_prop_info(ctx, id)

    if isOwner == False:
        print('Contract caller different from address')
        return False

    if prop_owner != b'':
        if prop_owner != address:
            print('The property is registered to another address')
            return False
        else:
            print('The property is already registered to caller address')
            return False

    print('user_props_serialized')
    store_prop(ctx,id,hash,address)

    OnPropRegist(id)

    return True

def prop_info_update(ctx,id,hash,address):
    isOwner = CheckWitness(address)
    prop_owner = get_prop_owner(ctx,id)
    prop_info = get_prop_info(ctx, id)

    if prop_info == b'':
        print('The property is not registered yet')
        return False

    if isOwner == False:
        print('Contract caller different from address')
        return False

    if prop_owner != b'':
        if prop_owner != address:
            print('The property is registered to another address')
            return False
    if prop_info == hash:
        print('The property is already registered to caller address')
        return False

    delete_prop_from_user(ctx,prop_owner,prop_info)
    store_prop(ctx,id,hash,prop_owner)

    OnPropUpdate(id)

    return True

def store_prop(ctx,id,hash,address):

    store_prop_owner(ctx,id,address)
    store_prop_info(ctx,id,hash)
    add_prop_to_user(ctx,address,hash)

    return True

def store_prop_owner(ctx,id,address):
    key = operation_key(PROP_OWNER_KEY,id)
    return Put(ctx,key,address)

def store_prop_info(ctx,id,hash):
    key = operation_key(PROP_INFO_KEY,id)
    return Put(ctx,key,hash)

def prop_deletion(ctx, id):
    prop_owner = get_prop_owner(ctx,id)
    prop_info = get_prop_info(ctx, id)

    if prop_info == b'':
        print('Property is not registered')
        return False

    isOwner = CheckWitness(prop_owner)

    if isOwner == False:
        print('You are not the owner of the property')
        return False

    prop_ownership_key = operation_key(PROP_OWNER_KEY,id)
    prop_info_key = operation_key(PROP_INFO_KEY,id)
    user_key = operation_key(USER_PROP_KEY,prop_owner)

    Delete(ctx,prop_info_key)
    Delete(ctx,prop_ownership_key)
    delete_prop_from_user(ctx,prop_owner,prop_info,user_key)

    OnPropDeletion(id)

    return True

def delete_prop_from_user(ctx,address,hash):
    user_prop_array = get_user_props_array(ctx,address)
    key = operation_key(USER_PROP_KEY,address)
    if len(user_prop_array) == 1:
        Delete(ctx,key)
        return True
    elif len(user_prop_array) == 0:
        print('The user do not own any property')
        return False

    user_prop_array = remove_item(user_prop_array,hash)
    user_props_serialized = serialize_array(user_prop_array)

    Put(ctx,key,user_props_serialized)

    return True

def add_prop_to_user(ctx,address,hash):
    user_prop_array = get_user_props_array(ctx,address)
    user_prop_array = add_item(user_prop_array,hash)
    user_props_serialized = serialize_array(user_prop_array)

    print('user_props_serialized')
    print(user_props_serialized)
    key = operation_key(USER_PROP_KEY,address)

    Put(ctx,key,user_props_serialized)

    return True

def get_user_props_array(ctx,address):
    user_prop_array = get_properties_user(ctx,address)

    if user_prop_array == b'':
        user_prop_array = []
    else:
        user_prop_array = deserialize_bytearray(user_prop_array)

    return user_prop_array
