# Hadcoin 💰

A Python-based cryptocurrency implementation featuring core blockchain functionality, secure wallet management, and a RESTful API interface. Built with a focus on educational purposes and blockchain fundamentals.

[![Apache License 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.x-green.svg)](https://flask.palletsprojects.com/)

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Documentation](#documentation)
- [License](#license)

## ✨ Features

- **Blockchain Core**: Complete implementation of blockchain fundamentals
- **Wallet Management**: Secure cryptocurrency wallet implementation using ECDSA
- **Node Network**: Distributed node network with peer-to-peer communication
- **RESTful API**: Comprehensive API for blockchain interaction
- **Mining System**: Proof-of-work mining implementation
- **Transaction Processing**: Secure transaction handling and verification

## 🗂️ Project Structure

```
Hadcoin/
├── .vscode/
│   └── settings.json
├── Blockchain/
│   ├── Block.py                 # Block class implementation
│   ├── Blockchain.py           # Core blockchain logic
│   ├── node.py                 # Node networking code
│   ├── Resources/
│   │   └── Module 2 - Create a Cryptocurrency/
│   │       ├── hadcoin_node_5001.py
│   │       ├── hadcoin_node_5002.py
│   │       ├── hadcoin_node_5003.py
│   │       ├── hadcoin.py
│   │       ├── nodes.json
│   │       └── transaction.json
│   ├── Reward.py               # Mining reward system
│   ├── tests/
│   │   ├── blockchain_test.py
│   │   └── chain.json
│   ├── Transaction.py          # Transaction handling
│   └── Wallet.py               # Wallet management
├── Documentation/
│   ├── Bibliography.docx
│   ├── Research Overview.docx
│   ├── Specification.docx
│   └── TurnItIn Report.docx
├── LICENSE
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Required Libraries

```bash
Flask>=2.0.0
requests>=2.25.1
ecdsa>=0.17.0
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hadcoin.git
cd hadcoin
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Node Network

Start multiple nodes to create a distributed network:

```bash
# Terminal 1 - Node 5001
python Blockchain/Resources/Module\ 2\ -\ Create\ a\ Cryptocurrency/hadcoin_node_5001.py

# Terminal 2 - Node 5002
python Blockchain/Resources/Module\ 2\ -\ Create\ a\ Cryptocurrency/hadcoin_node_5002.py

# Terminal 3 - Node 5003
python Blockchain/Resources/Module\ 2\ -\ Create\ a\ Cryptocurrency/hadcoin_node_5003.py
```

## 🔌 API Reference

### Blockchain Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/blockchain` | GET | Retrieve the entire blockchain |
| `/blockchain/length` | GET | Get the current chain length |
| `/blockchain/last_block` | GET | Get the most recent block |
| `/blockchain/block/<index>` | GET | Get block at specific index |

### Transaction Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/add_transaction` | POST | Submit new transaction |
| `/get_pending_transactions` | GET | List pending transactions |

### Mining Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mine_block` | GET | Mine a new block |

### Node Network

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/connect_node` | POST | Add node to network |
| `/leave` | POST | Remove node from network |

## 🧪 Testing

Run the test suite using:

```bash
python -m unittest discover -s Blockchain/tests
```

## 📚 Documentation

Comprehensive documentation is available in the `Documentation` folder:

- **Research Overview**: Background and theoretical foundations
- **Specification**: Technical requirements and system architecture
- **Bibliography**: Reference materials and citations

## 🛠️ Implementation Details

### Block Structure

```python
class Block:
    def __init__(self, 
                 index, 
                 timestamp, 
                 previous_hash, 
                 transaction, 
                 difficulty, 
                 nonce):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.transaction = transaction
        self.difficulty = difficulty
        self.nonce = nonce
        self.reward = None
        self.hash = self.hash_block()
```

### Transaction Format

```json
{
    "sender": "wallet_address_1",
    "recipient": "wallet_address_2",
    "amount": 10.0,
    "timestamp": 1635724800,
    "signature": "...",
    "hash": "..."
}
```
