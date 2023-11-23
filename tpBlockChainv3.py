import hashlib
longueur_block = 3;

# Classe Transaction pour représenter une transaction
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None

    def sign_transaction(self, private_key):
        # Simulation de la génération de signature à l'aide de la clé privée
        self.signature = generate_signature(private_key, self.sender + self.recipient + str(self.amount))

# Classe Block pour représenter un bloc dans la blockchain
class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Concaténation des données des transactions, du hash précédent et du nonce
        data = ''.join([str(transaction.__dict__) for transaction in self.transactions]) + self.previous_hash + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Preuve de travail : itération jusqu'à obtenir un hash satisfaisant la difficulté
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

# Classe Blockchain pour gérer la chaîne de blocs
class Blockchain:
    def __init__(self):
        self.transactions = []  # Liste des transactions en attente
        self.blocks = []  # Liste des blocs validés
        self.difficulty = 1

    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        # transaction.sign_transaction(private_key)  # À remplacer par la logique de génération de clé privée
        self.transactions.append(transaction)

        if len(self.transactions) % longueur_block == 0:
            self.create_block()

    def create_block(self):
        previous_hash = '0' if not self.blocks else self.blocks[-1].hash
        block = Block(self.transactions, previous_hash)
        block.mine_block(self.difficulty)
        self.blocks.append(block)
        self.transactions = []

    def check_transaction(self, id_transaction):
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.id == id_transaction:
                    return transaction

    def show_last_transactions(self):
        last_transactions = []
        for block in reversed(self.blocks):
            last_transactions.extend(block.transactions)
            if len(last_transactions) >= longueur_block:
                break
        for transaction in reversed(last_transactions):
            print(transaction)

    def tamper_transaction(self, id_transaction):
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.id == id_transaction:
                    # Modifier les détails de la transaction ici
                    break

    def validate(self):
        for block in self.blocks:
            if block.hash[:2] != '0x':
                return False
            if int(block.hash[2], 16) > 0:
                return False
        return True

    def save_blocks_to_file(self, filename):
        with open(filename, 'w') as file:
            for block in self.blocks:
                file.write(f"Block Hash: {block.hash}\n")
                file.write(f"Previous Hash: {block.previous_hash}\n")
                file.write(f"Nonce: {block.nonce}\n")
                file.write("Transactions:\n")
                for transaction in block.transactions:
                    file.write(f"Sender: {transaction.sender}\n")
                    file.write(f"Recipient: {transaction.recipient}\n")
                    file.write(f"Amount: {transaction.amount}\n")
                    file.write(f"Signature: {transaction.signature}\n")
                file.write("\n")

    def get_recent_transactions(self):
        recent_transactions = []
        num_transactions = min(len(self.transactions), longueur_block)
        for i in range(len(self.transactions) - 1, len(self.transactions) - num_transactions - 1, -1):
            recent_transactions.append(self.transactions[i])
        return recent_transactions

# Boucle principale du programme
blockchain = Blockchain()

while True:
    sender = input("Expéditeur: ")
    recipient = input("Destinataire: ")
    amount = float(input("Montant: "))

    blockchain.add_transaction(sender, recipient, amount)

    if len(blockchain.blocks) > 0 and len(blockchain.blocks[-1].transactions) % longueur_block == 0:
        print("Effectuer la preuve de travail (Proof of Work) pour le bloc courant...")
        blockchain.create_block()

    choice = input("Voulez-vous effectuer une autre transaction ? (Oui/Non): ")
    if choice.lower() != "oui":
        break

print("Dernières transactions:")
recent_transactions = blockchain.get_recent_transactions()
for transaction in recent_transactions:
    print(transaction.sender, "->", transaction.recipient, ":", transaction.amount)
