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
    current_time = currentBlock.Timestamp

    return current_time

def get_token_rate(current_tokens_sold,current_time):
    date_bonus = get_bonus_by_time()
    cap_bonus = get_bonus_by_cap()

    if date_bonus[0] < cap_bonus[0]:
        return date_bonus
    return cap_bonus

def get_bonus_by_time(current_time):
    bonus = [NEO_NO_BONUS,GAS_NO_BONUS]

    if current_time > 1528030800: #03-jun
        return bonus
    elif current_time > 1526821200: #20-may
        bonus = [NEO_BONUS_5,GAS_NO_BONUS_5]
        return bonus
    elif current_time > 1525611600: #06-may
        bonus = [NEO_BONUS_10,GAS_NO_BONUS_10]
        return bonus
    elif current_time > 1524402000: #22-april
        bonus = [NEO_BONUS_20,GAS_NO_BONUS_20]
        return bonus

    return bonus

def get_bonus_by_cap(current_tokens_sold):
    bonus = [NEO_NO_BONUS,GAS_NO_BONUS]

    if current_tokens_sold > (32375000*100000000): #tier 3
        return bonus
    elif current_tokens_sold > (11500000*100000000): #tier 2
        bonus = [NEO_BONUS_5,GAS_NO_BONUS_5]
        return bonus
    elif current_tokens_sold > (1500000*100000000): #tier1
        bonus = [NEO_BONUS_10,GAS_NO_BONUS_10]
        return bonus
    elif current_tokens_sold >= (0): #pre-sale
        bonus = [NEO_BONUS_20,GAS_NO_BONUS_20]
        return bonus

    return bonus
