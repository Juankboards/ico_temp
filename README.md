# Quarteria Smart Contract
Quarteria's NEO Token Sale Smart Contract for NEP-5 XQT Token Distribution

### Python Smart Contract

`ico_quarteria.py` is the smart contract entry point
`token.py` is the Basic settings for an NEP5 Token and crowdsale
`neo5.py` is the Basic settings for generalized interaction of the tokens
`user_service.py` defines the user operations for listing (register user, update, get info, get properties, delete)
`property_service.py` defines the property operations for listing (register property, update, get info, get owner, set owner, add to a user's properties array, delete)
`serialization.py` util functions to bytearray-array and array-bytearray conversion
`common.py` util functions (add item to array, remove item from array, concat key, get last block time, get token rate for crowdsale tiers)
`txio.py` Gets information about NEO and Gas attached to an invocation TX
