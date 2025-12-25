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

# --- STREAMLIT UI ---
st.set_page_config(page_title="Insurance Ledger", page_icon="🏦")

# Initialize blockchain
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = InsuranceBlockchain()

st.title("🛡️ Insurance Blockchain Ledger")

# Navigation Sidebar
menu = st.sidebar.selectbox("Select Action", ["Issue New Policy", "View Public Ledger"])

if menu == "Issue New Policy":
    st.header("✍️ Create Insurance Contract")
    
    with st.form("policy_entry"):
        holder = st.text_input("Policy Holder Name")
        coverage = st.selectbox("Coverage Type", ["Life", "Health", "Property", "Auto"])
        premium = st.number_input("Premium Amount ($)", min_value=0.0, step=100.0)
        
        submitted = st.form_submit_button("Sign & Append Block")
        
        if submitted:
            if holder:
                # Add data to transaction pool
                st.session_state.blockchain.add_transaction(
                    sender="Insurance_Provider_Corp",
                    receiver=holder,
                    amount=premium,
                    policy_details={"type": coverage, "status": "Active"}
                )
                
                # Link to previous block and finalize
                last_block = st.session_state.blockchain.get_last_block()
                prev_hash = st.session_state.blockchain.hash(last_block)
                st.session_state.blockchain.create_block(proof=101, previous_hash=prev_hash)
                
                st.success(f"Success! Policy for {holder} is now permanent on the chain.")
            else:
                st.warning("Please provide a policy holder name.")

elif menu == "View Public Ledger":
    st.header("📑 Transaction History")
    st.write("Each card below represents a 'Block' in the chain.")

    for block in reversed(st.session_state.blockchain.chain):
        # Calculate current block hash for display
        current_hash = st.session_state.blockchain.hash(block)
        
        with st.expander(f"📦 Block #{block['index']} | Hash: {current_hash[:16]}..."):
            st.write(f"**Timestamp:** {block['timestamp']}")
            st.write(f"**Previous Block Hash:** `{block['previous_hash']}`")
            st.write("**Transactions In This Block:**")
            if block['transactions']:
                st.table(block['transactions'])
            else:
                st.write("No transactions (Genesis Block)")

    if st.sidebar.button("Clear Chain Data"):
        del st.session_state.blockchain
        st.rerun()
