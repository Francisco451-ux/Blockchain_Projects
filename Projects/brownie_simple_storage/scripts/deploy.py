from brownie import accounts, config, SimpleStorage
import brownie.network as network
import os


def deploy_simple_storage():
    # default method with ganache
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)
    # transc
    # Call
    # make accounts:
    # encrypted method with brownie
    # account = accounts.load("freecodecamp-account")
    # os method
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # wallets method
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(os.getenv("PRIVATE_KEY"))


def main():
    deploy_simple_storage()
