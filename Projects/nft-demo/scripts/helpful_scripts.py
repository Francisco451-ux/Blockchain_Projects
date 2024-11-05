from brownie import (
    network,
    accounts,
    config,
    LinkToken,
    MockV3Aggregator,
    VRFCoordinatorMock,
    interface,
    Contract,
    web3,
)
from brownie.network import chain


# Set a default gas price
from brownie.network import priority_fee

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache", "mainnet-fork"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
# NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        try:
            contract_address = config["networks"][network.show_active()][contract_name]
            contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
            )
        except KeyError:
            print(
                f"{network.show_active()} address not found, perhaps you should add to the config or deploy mocks"
            )
            print(
                f"brownie run scripts/deploy_mock.py --network {network.show_active()}"
            )
            return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=1000000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = interface.LinkTokenInterface(link_token).transfer(
        contract_address, amount, {"from": account}
    )
    print(f"Funded {contract_address}")
    return tx


def deploy_mocks(decimals=18, initial_value=2000):
    """
    Use this script if you want to deploy mocks to a testnet
    """
    # Set a default gas price
    priority_fee("1 gwei")
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print(f"Deployed to {mock_price_feed.address}")
    print("Deploying Mock VRFCoordinator...")
    mock_vrf_coordinator = VRFCoordinatorMock.deploy(
        link_token.address, {"from": account, "gas_price": chain.base_fee}
    )
    print(f"Deployed to {mock_vrf_coordinator.address}")

    print("Deploying Mock Oracle...")
    mock_oracle = MockOracle.deploy(link_token.address, {"from": account})
    print(f"Deployed to {mock_oracle.address}")
    print("Mocks Deployed!")
