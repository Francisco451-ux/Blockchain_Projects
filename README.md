# Blockchain Projects

This repository contains a collection of blockchain and decentralized finance (DeFi) demos, primarily using Python frameworks like [Brownie](https://eth-brownie.readthedocs.io/en/stable/) and [web3.py](https://web3py.readthedocs.io/en/stable/). Each project demonstrates key aspects of smart contract development, interaction with the Ethereum blockchain, and integration with external services like Chainlink.

## Project List

1. **aave_brownie_py**  
   Demonstrates integration with the Aave protocol using Brownie. It includes scripts to interact with Aave's lending pool, deposit assets, and borrow against collateral. This project provides a foundational understanding of DeFi lending and borrowing mechanics.

2. **brownie_fund_me**  
   A contract allowing users to fund a contract and withdraw funds. This project showcases a simple example of managing funds in a contract with deposit and withdrawal functions, including tests and deployment scripts.

3. **brownie_simple_storage**  
   A minimalistic smart contract example focusing on storage interactions. It allows users to store and retrieve values, introducing key concepts of state variables, transaction handling, and interaction with Brownie scripts.

4. **erc20-brownie**  
   Implements an ERC-20 token standard contract, which includes minting and transferring tokens. This project is ideal for learning about token creation and management on Ethereum, as well as how ERC-20 contracts integrate with wallets and other dApps.

5. **mixes/chainlink**  
   A set of projects demonstrating Chainlink's oracle functionalities, including:
   - **APIConsumer.sol**: Uses Chainlink to fetch external API data.
   - **Counter.sol**: A simple counter for learning basic interactions.
   - **PriceFeedConsumer.sol**: Integrates Chainlink price feeds to retrieve real-time asset prices.
   - **VRFConsumerV2.sol**: Implements Chainlink VRF (Verifiable Random Function) to get random numbers for use in smart contracts.
   These demos are ideal for learning about oracles and randomness on blockchain.

6. **nft-demo**  
   A basic NFT (Non-Fungible Token) contract implementation that follows the ERC-721 standard. This project introduces the fundamentals of minting, transferring, and managing NFTs.

7. **nft-mix**  
   Expands on `nft-demo` by integrating with external data sources or additional functionalities, such as metadata storage and randomized token traits. It’s perfect for understanding complex NFT applications and metadata management.

8. **smartcontract-lottery**  
   A decentralized lottery system using Brownie and Chainlink VRF. Participants can enter by sending funds, and the contract randomly selects a winner. This project covers random selection, fund pooling, and automated payouts.

9. **web3_py_simple_storage**  
   Similar to `brownie_simple_storage`, but using `web3.py` instead of Brownie. This project demonstrates the basics of interacting with smart contracts using web3.py, including deployment, function calling, and event listening.

## Requirements

Each project may have specific dependencies listed in its `requirements.txt`. Generally, you will need:
- Python 3.8+
- Brownie
- web3.py