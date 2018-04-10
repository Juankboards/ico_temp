from boa.interop.Neo.Blockchain import GetHeight, GetHeader
from boa.interop.Neo.Storage import Get
from boa.interop.Neo.Header import *
from xqt.token import TOKEN_CIRC_KEY

NEO_NO_BONUS = 417 * 100000000
NEO_BONUS_5 = 439 * 100000000
NEO_BONUS_10 = 463 * 100000000
NEO_BONUS_20 = 521 * 100000000

GAS_NO_BONUS = 167 * 100000000
GAS_BONUS_5 = 175 * 100000000
GAS_BONUS_10 = 185 * 100000000
GAS_BONUS_20 = 208 * 100000000

def add_item(array,item):
    array_len = len(array)
    new_len = array_len + 1
    new_array = list(length=new_len)

    for i in range(0, array_len):
        new_array[i] = array[i]

    new_array[array_len] = item

    return new_array

def remove_item(array,item):
    array_len = len(array)
    new_len = array_len - 1
    new_array = list(length=new_len)
    found = 0

    for i in range(0, array_len):
        index = i - found
        if item != array[i]:
            new_array[index] = array[i]
        else:
            found = 1

    return new_array

def operation_key(key,value):
    return concat(key,value)

def get_current_time():
    currentHeight = GetHeight()
    currentBlock = GetHeader(currentHeight)
    currentTime = currentBlock.Timestamp

    return currentTime

def get_token_rate(ctx):
    date_bonus = get_bonus_by_time()
    cap_bonus = get_bonus_by_cap(ctx)

    if date_bonus[0] < cap_bonus[0]:
        return date_bonus
    return cap_bonus

def get_bonus_by_time():
    bonus = [NEO_NO_BONUS,GAS_NO_BONUS]

    currentTime = get_current_time()

    if currentTime > 1528030800: #03-jun
        return bonus
    elif currentTime > 1526821200: #20-may
        bonus = [NEO_BONUS_5,GAS_NO_BONUS_5]
        return bonus
    elif currentTime > 1525611600: #06-may
        bonus = [NEO_BONUS_10,GAS_NO_BONUS_10]
        return bonus
    elif currentTime > 1524402000: #22-april
        bonus = [NEO_BONUS_20,GAS_NO_BONUS_20]
        return bonus

    return bonus

def get_bonus_by_cap(ctx):
    bonus = [NEO_NO_BONUS,GAS_NO_BONUS]
    current_in_circulation = Get(ctx, TOKEN_CIRC_KEY)

    if current_in_circulation > (63200000*100000000): #03-jun
        return bonus
    elif current_in_circulation > (42325000*100000000): #20-may
        bonus = [NEO_BONUS_5,GAS_NO_BONUS_5]
        return bonus
    elif current_in_circulation > (32325000*100000000): #06-may
        bonus = [NEO_BONUS_10,GAS_NO_BONUS_10]
        return bonus
    elif current_in_circulation > (30825000*100000000): #22-april
        bonus = [NEO_BONUS_20,GAS_NO_BONUS_20]
        return bonus

    return bonus
