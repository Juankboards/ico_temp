from xqt.txio import get_asset_attachments
from xqt.token import *
from xqt.crowdsale import *
from xqt.nep5 import *
from xqt.user_service import *
from xqt.property_service import *
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import *
from boa.builtins import substr


ctx = GetContext()

NEP5_METHODS = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']
USER_METHODS = ['user_info', 'user_properties', 'register_user', 'update_user', 'delete_user']
PROPERTIES_METHODS = ['prop_info', 'prop_owner', 'register_prop', 'update_prop', 'delete_prop']

def Main(operation, args):
    """

    :param operation: str The name of the operation to perform
    :param args: list A list of arguments along with the operation
    :return:
        bytearray: The result of the operation
    """

    trigger = GetTrigger()

    # This is used in the Verification portion of the contract
    # To determine whether a transfer of system assets ( NEO/Gas) involving
    # This contract's address can proceed
    if trigger == Verification():

        # check if the invoker is the owner of this contract
        owner = TOKEN_OWNER
        is_owner = CheckWitness(owner)

        # If owner, proceed
        if is_owner:

            return True

        # Otherwise, we need to lookup the assets and determine
        # If attachments of assets is ok
        attachments = get_asset_attachments()
        return check_and_calculate_exchange(ctx, attachments, True)

    elif trigger == Application():

        for op in NEP5_METHODS:
            if operation == op:
                return handle_nep51(ctx, operation, args)

        for op in USER_METHODS:
            if operation == op:
                return handle_user(ctx, operation, args)

        for op in PROPERTIES_METHODS:
            if operation == op:
                return handle_prop(ctx, operation, args)

        if operation == 'deploy':
            return deploy()

        elif operation == 'circulation':
            return get_circulation(ctx)

        # the following are handled by crowdsale

        elif operation == 'mintTokens':
            return perform_exchange(ctx)

        elif operation == 'crowdsale_register':
            return kyc_register(ctx, args)

        elif operation == 'crowdsale_status':
            return kyc_status(ctx, args)

        elif operation == 'crowdsale_available':
            return crowdsale_available_amount(ctx)

        elif operation == 'neo_contribution':
            return get_contribution(ctx,'neo',args)

        elif operation == 'gas_contribution':
            return get_contribution(ctx,'gas',args)

        elif operation == 'get_attachments':
            return get_asset_attachments()

        return 'unknown operation'

    return False


def deploy():
    """

    :param token: Token The token to deploy
    :return:
        bool: Whether the operation was successful
    """
    owner = TOKEN_OWNER
    is_owner = CheckWitness(owner)

    if not is_owner:
        print("Must be owner to deploy")
        return False

    if not Get(ctx, 'initialized'):
        # do deploy logic
        Put(ctx, 'initialized', 1)
        Put(ctx, TOKEN_OWNER, TOKEN_INITIAL_AMOUNT)
        return add_to_circulation(ctx, TOKEN_INITIAL_AMOUNT)

    return False
