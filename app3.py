import streamlit as st
import hashlib
import json
from time import time

# --- BLOCKCHAIN LOGIC ---
class InsuranceBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # Create Genesis Block
        self.create_block(proof=100, previous_hash='1')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount, policy_details):
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'policy_details': policy_details
        })
        return self.get_last_block()['index'] + 1

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_last_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current['previous_hash'] != self.hash(previous):
                return False
        return True

# --- STREAMLIT UI ---
st.set_page_config(page_title="Insurance Blockchain", page_icon="🏦", layout="wide")

# SAFE INITIALIZATION: Overwrites old session state if methods are missing
if 'blockchain' not in st.session_state or not hasattr(st.session_state.blockchain, 'is_chain_valid'):
    st.session_state.blockchain = InsuranceBlockchain()

st.title("🛡️ Financial Insurance Blockchain Ledger")
st.info("This ledger tracks policy issuances and claims using cryptographic hashing.")

# Sidebar
st.sidebar.header("Control Panel")
menu = st.sidebar.radio("Navigation", ["New Policy", "Audit Ledger", "System Security"])

if menu == "New Policy":
    st.subheader("✍️ Issue Insurance Policy")
    with st.form("policy_form"):
        col1, col2 = st.columns(2)
        with col1:
            client = st.text_input("Policy Holder Name")
            p_type = st.selectbox("Policy Type", ["Flight Delay", "Crop Insurance", "Crypto Theft"])
        with col2:
            premium = st.number_input("Premium Amount ($)", min_value=10.0)
            
        if st.form_submit_button("Seal & Add to Block"):
            if client:
                st.session_state.blockchain.add_transaction(
                    sender="Insurance_Vault",
                    receiver=client,
                    amount=premium,
                    policy_details={"type": p_type, "status": "Active"}
                )
                # Auto-mining for the demo
                prev_hash = st.session_state.blockchain.hash(st.session_state.blockchain.get_last_block())
                st.session_state.blockchain.create_block(proof=200, previous_hash=prev_hash)
                st.success(f"Successfully added Block #{len(st.session_state.blockchain.chain)}")
            else:
                st.error("Please enter a client name.")

elif menu == "Audit Ledger":
    st.subheader("📑 Immutable Transaction History")
    for block in reversed(st.session_state.blockchain.chain):
        with st.expander(f"Block #{block['index']} (Hash: {st.session_state.blockchain.hash(block)[:16]}...)"):
            st.write(f"**Timestamp:** {block['timestamp']}")
            st.write(f"**Prev Hash:** {block['previous_hash']}")
            st.write("**Data:**")
            st.table(block['transactions'])

elif menu == "System Security":
    st.subheader("🔍 Blockchain Integrity Audit")
    
    is_valid = st.session_state.blockchain.is_chain_valid()
    
    if is_valid:
        st.success("✅ INTEGRITY VERIFIED: All block hashes match their predecessors.")
    else:
        st.error("🚨 ALERT: Data Inconsistency detected! The blockchain has been tampered with.")

    if st.button("Reset Blockchain"):
        st.session_state.blockchain = InsuranceBlockchain()
        st.rerun()
