from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Runtime import CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import Get, Put
from boa.builtins import concat
from xqt.token import *
from xqt.common import *
from xqt.txio import get_asset_attachments

# OnInvalidKYCAddress = RegisterAction('invalid_registration', 'address')
OnKYCRegister = RegisterAction('kyc_registration', 'address')
OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnContribution = RegisterAction('contribution', 'from', 'neo', 'gas', 'tokens')
OnRefund = RegisterAction('refund', 'addr_to', 'amount')


OnPreSaleMint = RegisterAction('presale_mint', 'to', 'neo', 'tokens')



KYC_KEY = b'kyc_ok'


def kyc_register(ctx, args):
    """

    :param args:list a list of addresses to register
    :param token:Token A token object with your ICO settings
    :return:
        int: The number of addresses to register for KYC
    """
    ok_count = 0

    if CheckWitness(TOKEN_OWNER):

        for address in args:

            if len(address) == 20:

                kyc_storage_key = concat(KYC_KEY, address)
                Put(ctx, kyc_storage_key, True)

                OnKYCRegister(address)
                ok_count += 1

    return ok_count


def kyc_status(ctx, args):
    """
    Gets the KYC Status of an address

    :param args:list a list of arguments
    :return:
        bool: Returns the kyc status of an address
    """

    if len(args) > 0:
        addr = args[0]

        kyc_storage_key = concat(KYC_KEY, addr)

        return Get(ctx, kyc_storage_key)

    return False


def perform_exchange(ctx):
    """

     :param token:Token The token object with NEP5/sale settings
     :return:
         bool: Whether the exchange was successful
     """

    attachments = get_asset_attachments()  # [receiver, sender, neo, gas]

    # this looks up whether the exchange can proceed
    tokens = check_and_calculate_exchange(ctx, attachments, False)

    if not tokens:
        # This should only happen in the case that there are a lot of TX on the final
        # block before the total amount is reached.  An amount of TX will get through
        # the verification phase because the total amount cannot be updated during that phase
        # because of this, there should be a process in place to manually refund tokens
        if attachments[2] > 0:
            OnRefund(attachments[1], attachments[2])
        # if you want to exchange gas instead of neo, use this
        if attachments[3] > 0:
            OnRefund(attachments[1], attachments[3])
        return False

    min_tokens(ctx,attachments[0],attachments[1],tokens)

    #get the toal tokens sold on public sale
    current_tokens_sold = Get(PUBLIC_SALE_SOLD_KEY)

    current_tokens_sold += tokens

    Put(ctx,PUBLIC_SALE_SOLD_KEY,current_tokens_sold)

    # track contributions as a separate event for token sale account page transaction updates
    OnContribution(attachments[1],attachments[2],attachments[3], tokens)

    return True

def check_and_calculate_exchange(ctx, attachments, verify_only):
    """
    Determines if the contract invocation meets all requirements for the ICO exchange
    of neo or gas into NEP5 Tokens.
    Note: This method can be called via both the Verification portion of an SC or the Application portion

    When called in the Verification portion of an SC, it can be used to reject TX that do not qualify
    for exchange, thereby reducing the need for manual NEO or GAS refunds considerably

    :param attachments:Attachments An attachments object with information about attached NEO/Gas assets
    :return:
        bool: Whether an invocation meets requirements for exchange
    """

    # if you are accepting gas, use this
    if attachments[2] == 0 or attachments[3] == 0:
       print("no neo or gas attached")
       return False

    # the following looks up whether an address has been
    # registered with the contract for KYC regulations
    # this is not required for operation of the contract

    status = get_kyc_status(ctx,attachments[1])
    if not status:
        print("not KYC approved")
        return False

    exchange_ok = calculate_tokens(ctx,attachments[2],attachments[3])

    return exchange_ok


def get_kyc_status(ctx, address):
    """
    Looks up the KYC status of an address

    :param address:bytearray The address to lookup
    :param storage:StorageAPI A StorageAPI object for storage interaction
    :return:
        bool: KYC Status of address
    """
    if len(address) == 20:
        kyc_storage_key = concat(KYC_KEY, address)
        return Get(ctx, kyc_storage_key)

    return False


def calculate_tokens(ctx,neo_attached,gas_attached):
    """
    Perform custom token exchange calculations here.

    :param amount:int Number of tokens to convert from asset to tokens
    :param address:bytearray The address to mint the tokens to
    :return:
        bool: Whether or not an address can exchange a specified amount
    """
    current_time = get_current_time()
    current_tokens_sold = Get(ctx, PUBLIC_SALE_SOLD_KEY)

    tokens = get_token_rate(current_tokens_sold,current_time)

    # calculate the amount requested per neo
    amount_requested = neo_attached * tokens[0] / 100000000

    # calculate the amount requested per gas
    amount_requested += gas_attached * tokens[1] / 100000000

    new_amount = current_tokens_sold + amount_requested

    if new_amount > PUBLIC_SALE_TOKEN_LIMIT:
        print("purchase would exceed token sale limit")
        return False

    if currentTime < DATE_SALE_START:
        print("sale not started")
        return False

    if height > DATE_SALE_STOP:
        print("crowdsale ended")
        return False

    return amount_requested

def min_tokens(ctx,from_address,to_address,tokens):
    """
    Mint tokens for an address
        :param from_address: the address from which the tokens are being minted (should always be the contract address)
        :param to_address: the address to transfer the minted tokens to
        :param tokens: the number of tokens to mint
    """
    # lookup the current balance of the address
    current_balance = Get(ctx,to_address)

    new_total = current_balance + tokens

    #save new balance on the address
    Put(ctx,to_address,new_total)

    # update the in circulation amount
    result = add_to_circulation(ctx, tokens)

    # dispatch transfer event
    OnTransfer(from_address,to_address,tokens)
