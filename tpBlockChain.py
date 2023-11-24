a
import time
import hashlib

longueur_block = 10

class Transaction:
    block_counter =0    
    id_counter = 0
    def __init__(self, sender, recipient, amount):
        
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.id = f"{Transaction.block_counter}.{Transaction.id_counter % 10}"
        Transaction.id_counter += 1
        if (Transaction.id_counter % 10) == 1 :
            Transaction.block_counter += 1

class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(f"{self.previous_hash}{self.timestamp}{self.nonce}".encode('utf-8')).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.transactions = {}
        self.blocks = []
        self.difficulty = 2
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_transaction = Transaction("", "", 0)
        self.add_transaction(genesis_transaction)
        self.create_block()

    def add_transaction(self, transaction):
        self.transactions[transaction.id] = transaction
        return True

    def create_block(self):
        previous_hash = '0' if not self.blocks else self.blocks[-1].hash
        block = Block(self.transactions, previous_hash)
        block.mine_block(self.difficulty)
        self.blocks.append(block)
        self.transactions = {}
    
    def get_transactions(self, id_searched):
        for transaction_id in self.transactions:
            if transaction_id == str(id_searched):
                return self.transactions[transaction_id]
        return None

    def save_blockchain(self, filename):
        with open(filename, 'w') as file:
            file.write(f"Blockchain:\n")
            for block in self.blocks:
                file.write(f"Nonce: {block.nonce}\n")
                file.write("Transactions:\n")
                for transaction_id in block.transactions:
                    transaction = block.transactions[transaction_id]
                    file.write(f"Sender: {transaction.sender}\n")
                    file.write(f"Recipient: {transaction.recipient}\n")
                    file.write(f"Amount: {transaction.amount}\n")
                    file.write(f"ID: {transaction.id}\n")
                file.write("\n")

    def get_recent_transactions(self):
        recent_transactions = []
        num_transactions = min(len(self.transactions), longueur_block)
        for transaction_id in sorted(self.transactions, key=lambda x: self.transactions[x].timestamp, reverse=True):
            if len(recent_transactions) == num_transactions:
                break
            recent_transactions.append(self.transactions[transaction_id])
        return recent_transactions
    
def show_transactions():
        print("Dernières transactions:")
        recent_transactions = blockchain.get_recent_transactions()
        for transaction in recent_transactions:
            print(f"{transaction.id} == {transaction.sender} -> {transaction.recipient} : {transaction.amount} ")
            print("\n")

def check_transactions():
    id_searched = input("Entrez l'ID de la transaction que vous voulez regarder : ")
    transaction = blockchain.get_transactions(id_searched)
    if transaction is not None:
        print(f"{transaction.id} == {transaction.sender} -> {transaction.recipient} : {transaction.amount} ")
    else:
        print("La transaction n'a pas été trouvée.")

def classic_run() : 
    sender = input("Expéditeur: ")
    recipient = input("Destinataire: ")
    amount = float(input("Montant: "))

    blockchain.add_transaction(Transaction(sender, recipient, amount))

    if len(blockchain.blocks) > 0 and len(blockchain.blocks[-1].transactions) % longueur_block == 0:
        print("Effectuer la preuve de travail (Proof of Work) pour le bloc courant...")
        blockchain.create_block()
    

blockchain = Blockchain()

while True:
    

    choice = input("Que voulez-vous faire ? \n Ajouter une transaction -> a \n Regarder les 10 dernières transactions-> s \n Regarder une certaine transaction -> c \n Modifier la transaction -> t \n Votre choix :")
    if choice.lower() == "a" :
        classic_run()
    elif choice.lower() == "c" :
        check_transactions()
    elif choice.lower() == "s" :
        show_transactions()
    elif choice.lower() == "t" :
        check_transactions()
    else :
        break



filename = input("Nom du fichier pour enregistrer la chaîne de blocs: ")
blockchain.save_blockchain(filename)

print("La chaîne de blocs a été enregistrée.")




