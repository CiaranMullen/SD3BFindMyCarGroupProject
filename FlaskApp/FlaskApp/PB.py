from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

server_UUID = "bd10e0c6-354a-11eb-adc1-0242ac120002"
cipherKey = "myCipherKey"
myChannel = "SD3B"

############################
pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-a673c30e-2430-11eb-af2a-72ba4a3d8762'
pnconfig.publish_key = 'pub-c-2bdeaffe-3be4-4af2-9b37-1b2e73389ef6'
pnconfig.secret_key = "sec-c-YmM2YzhkZmUtZmJiOC00Y2M3LTg4YTQtY2QwYTA0ZWFlMjJk"
pnconfig.uuid = server_UUID
pnconfig.cipher_key = cipherKey
pubnub = PubNub(pnconfig)



def grantAccess(auth_key, read, write):
    if read is True and write is True:
        grantReadAndWriteAccess(auth_key)
    elif read is True:
        grantReadAccess(auth_key)
    elif write is True:
        grantWriteAccess(auth_key)
    else:
        revokeAccess(auth_key)


def grantReadAndWriteAccess(auth_key):
    v = pubnub.grant() \
        .read(True) \
        .write(True) \
        .channels(myChannel) \
        .auth_keys(auth_key) \
        .ttl(6000) \
        .sync()
    print("------------------------------------")
    print("--- Granting Read & Write Access ---")
    for key, value in v.status.original_response.items():
        print(key, ":", value)
    print("------------------------------------")


def grantReadAccess(auth_key):
    v = pubnub.grant() \
        .read(True) \
        .channels(myChannel) \
        .auth_keys(auth_key) \
        .ttl(6000) \
        .sync()
    print("------------------------------------")
    print("--- Granting Read Access ---")
    for key, value in v.status.original_response.items():
        print(key, ":", value)
    print("------------------------------------")


def grantWriteAccess(auth_key):
    v = pubnub.grant() \
        .write(True) \
        .channels(myChannel) \
        .auth_keys(auth_key) \
        .ttl(6000) \
        .sync()
    print("------------------------------------")
    print("--- Granting Write Access ---")
    for key, value in v.status.original_response.items():
        print(key, ":", value)
    print("------------------------------------")


def revokeAccess(auth_key):
    v = pubnub.revoke() \
        .channels(myChannel) \
        .auth_keys(auth_key) \
        .sync()
    print("------------------------------------")
    print("--- Revoking Access ---")
    for key, value in v.status.original_response.items():
        print(key, ":", value)
    print("------------------------------------")
