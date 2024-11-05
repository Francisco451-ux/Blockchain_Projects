from scripts.helpful_scripts import get_account
from brownie import interface, config, network
from scripts.get_weth import get_weth
from web3 import Web3

# 0.1

amount = Web3.toWei(0.1, "ether")


def main():
    """
    Mints WETH by depositing ETH

    """
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # get_weth()
    # ABI
    # Address
    lending_pool = get_lending_pool()
    print(lending_pool)
    # Approve sending out ERC20 tokens
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited")
    # ... how much?

    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    # borrowable_eth -> borrowable_dai * 95%
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    dai_address = config["networks"][network.show_active()]["dai_token"]
    try:
        borrow_tx = lending_pool.borrow(
            dai_address,
            Web3.toWei(amount_dai_to_borrow, "ether"),
            1,
            0,
            account.address,
            {"from": account},
        )
    except Exception as e:
        print(f"Transaction reverted with reason: {str(e)}")
    borrow_tx.wait(1)
    print(f"We borrow same Dai")
    get_borrowable_data(lending_pool, account)
    replay_all(amount, lending_pool, account)
    print("You just deposited, and repayed with Aave, Brownie, and Chainlink")


def replay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Repay")


def get_asset_price(price_feed_address):
    # ABI
    # Address
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(latest_price)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth if ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH")
    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved")
    return tx


def get_lending_pool():
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_address_provider"]
    )
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    # ABI
    # Address - check!
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
