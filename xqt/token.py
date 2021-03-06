"""
Basic settings for an NEP5 Token and crowdsale
"""

from boa.interop.Neo.Storage import *

TOKEN_NAME = 'Quarteria Token'

TOKEN_SYMBOL = 'XQTA'

TOKEN_DECIMALS = 8

# This is the script hash of the address for the owner of the token
# This can be found in ``neo-python`` with the walet open, use ``wallet`` command
TOKEN_OWNER = b'\xd9/&\x8b\x9b\xd6\x13<\x9am\xc5\x0c\x04\xe7\xdd\xd1\xf0\xae\xe1\x0b'

TOKEN_CIRC_KEY = b'in_circulation'

PUBLIC_SALE_SOLD_KEY = b'pub_sale_sold'

NEO_CONTRIBUTION_KEY = b'neo_contributed'

GAS_CONTRIBUTION_KEY = b'gas_contributed'

TOKEN_TOTAL_SUPPLY = 100000000 * 100000000  # 100m total supply * 10^8 ( decimals)

TOKEN_INITIAL_AMOUNT = 31015045 * 100000000  # 26.5m to owners plus 4.325m private sale * 10^8

PUBLIC_SALE_TOKEN_LIMIT = 68984955 * 100000000 # 69.175m to public sale * 10^8

# maximum amount you can mint in the limited round
MAX_EXCHANGE_LIMITED_ROUND = 68984955 * 100000000

# when to start the crowdsale: 22-April
DATE_SALE_START = 1524402000

# when to end the initial limited round: 17-June
DATE_SALE_STOP = 1529240400

def crowdsale_available_amount(ctx):
    """

    :return: int The amount of tokens left for sale in the crowdsale
    """

    public_tokens_sold = Get(ctx,PUBLIC_SALE_SOLD_KEY)

    # keep track of sold tokens on public sale
    available = PUBLIC_SALE_TOKEN_LIMIT - public_tokens_sold

    if available < 0:
        return 0

    return available


def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circlulation

    :param amount: int the amount to add to circulation
    """

    current_supply = Get(ctx, TOKEN_CIRC_KEY)

    current_supply += amount
    Put(ctx, TOKEN_CIRC_KEY, current_supply)
    return True


def get_circulation(ctx):
    """
    Get the total amount of tokens in circulation

    :return:
        int: Total amount in circulation
    """
    return Get(ctx, TOKEN_CIRC_KEY)
