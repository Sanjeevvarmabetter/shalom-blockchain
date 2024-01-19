from django.shortcuts import render
import datetime
import hashlib
import json
from django.http import JsonResponse
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
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
              return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**3 - previous_nonce**3).encode()).hexdigest()

            if hash_operation[:4] == '0000':
                return False
            previous_block = block
            block_index += 1

        return True

        

blockchain = Blockchain()

#for mining the blockchain
def mine_block(request):
    if request.method == 'GET':
        previous_block= blockchain.get_previous_block()
        previous_nonce = previous_block['nonce']

        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(nonce,previous_hash)
        response = {'message':'You mined a block!',
                    'index':block['index'],
                    'timestamp': block['timestamp'],
                    'nonce':block['nonce'],
                    'previous_hash': block['previous_hash']}
    return JsonResponse(response)

#for getting the full blockchain
def get_chain(request):
    if request.method == 'GET':
        response = {'chain':blockchain.chain,
                    'length': len(blockchain.chain)}
    return JsonResponse(response)

#for checking if the block is valid or not
def is_valid(request):
    if request.method == 'GET':
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message' : 'it ok bro the blockchain is good to go'}
        else:
            response = {'message' : 'we have a problem hero'}

    return JsonResponse(response)
    