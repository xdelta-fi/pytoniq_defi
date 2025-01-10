# pytoniq-core

[![PyPI version](https://badge.fury.io/py/pytoniq-defi.svg)](https://badge.fury.io/py/pytoniq-defi) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytoniq-defi)](https://pypi.org/project/pytoniq-defi/)
![](https://pepy.tech/badge/pytoniq-defi) 
[![Downloads](https://static.pepy.tech/badge/pytoniq-defi)](https://pepy.tech/project/pytoniq-defi) 
[![](https://img.shields.io/badge/%F0%9F%92%8E-TON-grey)](https://ton.org)

`pytoniq_defi` is an extension of the [pytoniq](https://github.com/yungwine/pytoniq) library that focuses on DeFi (Decentralized Finance) operations in the TON network. It helps parse and compose various messages related to Jetton transfers, liquidity provision, staking, and more.

## Features
- Parse Jetton messages like transfers, burn, notifications, and internal transfers.
- Compose valid TON messages for DEX operations, liquidity deposits, and staking.
- Offers typed classes (e.g., `JettonTransfer`, `DedustMessageSwap`) that serialize/deserialize seamlessly to/from TON cells.

## Installation
```bash
pip install pytoniq_defi
```
## Usage
```python
from pytoniq_code import Address
from pytoniq_defi import Jetton, Dedust, Stonfi, StonfiV2

# Example: Creating a Jetton Transfer message
transfer = Jetton.Transfer(query_id=1, amount=1000, destination=Address("UQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKZ"))
cell = transfer.serialize()

# Example: Deserializing Dedust Swap
deserialized_swap = Dedust.Swap.deserialize(cell.begin_parse())
```

## Contributing

1. Fork the repository.
2.  Create a new branch.
3.  Submit a pull request with details on your changes.

## License

This project is licensed under the MIT License. See LICENSE for details.
