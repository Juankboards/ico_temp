from boa.interop.Neo.Runtime import CheckWitness
from boa.builtins import concat
from boa.interop.Neo.Storage import *
from xqt.common import *
from xqt.serialization import deserialize_bytearray, serialize_array
from xqt.user_service import USER_PROP_KEY, get_properties_user

PROP_INFO_KEY = b'prop_info'
PROP_OWNER_KEY = b'prop_owner'

def handle_prop(ctx, operation, args):
    if operation == 'prop_info':
        return get_prop_info(ctx,args[0])
    elif operation == 'prop_owner':
        return get_prop_owner(ctx,args[0])
    elif operation == 'register_prop':
        return prop_info_registration(ctx, args[0],args[1],args[2])
    elif operation == 'update_prop':
        return prop_info_registration(ctx, args[0],args[1],args[2])
    elif operation == 'delete_prop':
        return prop_deletion(ctx, args[0],args[1])
    return False

def get_prop_info(ctx, id):
    key = operation_key(PROP_INFO_KEY,id)
    return Get(ctx,key)

def get_prop_owner(ctx, id):
    key = operation_key(PROP_OWNER_KEY,id)
    return Get(ctx,key)

def prop_info_registration(ctx, id,hash,address):
    isOwner = CheckWitness(address)
    prop_owner = get_prop_owner(ctx,id)

    if isOwner == False:
        print('Contract caller different from address')
        return False

    if prop_owner != b'':
        if prop_owner == address:
            prop_info = get_prop_info(ctx, id)
            if prop_info == hash:
                print('The property is already registered to caller address')
                return False
        else:
            print('The property is already registered to another address')
            return False

    prop_ownership_key = operation_key(PROP_OWNER_KEY,id)
    prop_info_key = operation_key(PROP_INFO_KEY,id)
    user_key = operation_key(USER_PROP_KEY,address)

    Put(ctx,prop_info_key,hash)
    Put(ctx,prop_ownership_key,address)
    add_prop_to_user(ctx,address,hash,user_key)

    return True

def prop_deletion(ctx, id,address):
    isOwner = CheckWitness(address)
    prop_owner = get_prop_owner(ctx,id)
    prop_info = get_prop_info(ctx, id)

    if isOwner == False:
        print('Contract caller different from address')
        return False

    if prop_owner == b'':
        print('Property is not registered')
        return False

    if prop_owner != address:
        return False

    prop_ownership_key = operation_key(PROP_OWNER_KEY,id)
    prop_info_key = operation_key(PROP_INFO_KEY,id)
    user_key = operation_key(USER_PROP_KEY,address)

    Delete(ctx,prop_info_key)
    Delete(ctx,prop_ownership_key)
    delete_prop_from_user(ctx,address,prop_info,user_key)

    return True

def delete_prop_from_user(ctx,address,hash,key):
    user_prop_array = get_user_props_array(ctx,address)
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

def add_prop_to_user(ctx,address,hash,key):
    user_prop_array = get_user_props_array(ctx,address)
    user_prop_array = add_item(user_prop_array,hash)
    user_props_serialized = serialize_array(user_prop_array)

    Put(ctx,key,user_props_serialized)

    return True

def get_user_props_array(ctx,address):
    user_prop_array = get_properties_user(ctx,address)

    if user_prop_array == b'':
        user_prop_array = []
    else:
        user_prop_array = deserialize_bytearray(user_prop_array)

    return user_prop_array
