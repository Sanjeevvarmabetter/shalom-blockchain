from django.shortcuts import render
import datetime
import hashlib
import json
# Create your views here.

#blockchain logic goes here

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(nonce = 1,previous_hash = '0')

    def create_block(self,nonce,previous_hash):
        #block is a dict
        block = {'index':len(self.chain)+1,
                 'timestamp':str(datetime.datetime.now()),
                 'nonce':nonce,
                 'previous_hash':previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]        

    def proof_of_work(self,previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**3 - previous_nonce**3).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1 #we have to increment the new nonce {trail and error}
            return new_nonce


    #hashing function
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        
        
    

#for mining the blockchain
def mine_block()
    


#for getting the full blockchain
def get_chain()
    

#for checking if the block is valid or not
def is_valid()

    