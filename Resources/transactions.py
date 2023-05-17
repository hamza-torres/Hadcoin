import rsa

def send_transaction(sender_private_key, receiver_public_key, amount):
    """Sends a transaction to the receiver.

    Args:
        sender_private_key: The sender's private key.
        receiver_public_key: The receiver's public key.
        amount: The amount of cryptocurrency to send.

    Returns:
        The transaction hash.
    """

    # Generate the transaction data.
    transaction_data = {
        'sender_public_key': sender_public_key,
        'receiver_public_key': receiver_public_key,
        'amount': amount,
    }

    # Sign the transaction data.
    signature = rsa.sign(transaction_data, sender_private_key, 'SHA-256')

    # Add the signature to the transaction data.
    transaction_data['signature'] = signature

    # Encode the transaction data as a JSON string.
    transaction_json = json.dumps(transaction_data)

    # Hash the transaction data.
    transaction_hash = hashlib.sha256(transaction_json.encode()).hexdigest()

    return transaction_hash


def verify_transaction(transaction_hash, receiver_public_key):
    """Verifies a transaction.

    Args:
        transaction_hash: The transaction hash.
        receiver_public_key: The receiver's public key.

    Returns:
        True if the transaction is valid, False otherwise.
    """

    # Decode the transaction data from a JSON string.
    transaction_json = json.loads(transaction_hash)

    # Verify the signature.
    try:
        rsa.verify(transaction_json, transaction_json['signature'], receiver_public_key, 'SHA-256')
    except rsa.InvalidSignatureError:
        return False

    # Check the amount.
    if transaction_json['amount'] < 0:
        return False

    return True
