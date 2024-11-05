from scripts.helpful_scripts import get_account
from brownie import interface, network, config
import brownie.network as network


def main():
    get_weth()


def get_weth():
    """
    Mints WETH by depositing ETH

    """
    account = get_account()
    print(account.balance())
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10**18})
    tx.wait(1)
    print("Received 0.1 WETH")
    return tx
