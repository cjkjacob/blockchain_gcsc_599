import requests
from .blockchain import Block
from .chain import blockchain

peer_nodes = set()
broadcast_logs = []  # Optional: to expose later

def add_node(address):
    if address and address != self_url:
        peer_nodes.add(address)

def get_nodes():
    return list(peer_nodes)

def broadcast_block(block):
    global broadcast_logs
    broadcast_logs = []

    for node in peer_nodes:
        try:
            res = requests.post(f"{node}/api/receive-block", json={"block": block.to_dict()})

            # Default values in case response is empty
            status = res.status_code
            content_type = res.headers.get('Content-Type', '')

            # Try to extract JSON message
            if 'application/json' in content_type:
                try:
                    message = res.json().get("message") or res.json().get("error") or "[no message]"
                except Exception as e:
                    message = f"JSON decode error: {str(e)}"
            else:
                # Fallback to raw response text (could be HTML, plain text, etc.)
                message = res.text or "[empty response]"

            broadcast_logs.append({
                "node": node,
                "status": status,
                "message": message.strip()
            })

        except Exception as e:
            broadcast_logs.append({
                "node": node,
                "status": "error",
                "message": str(e)
            })

def get_broadcast_logs():
    return broadcast_logs

def fetch_chain_from_node(node):
    try:
        response = requests.get(f"{node}/api/chain")
        if response.status_code == 200:
            return response.json().get("chain", [])
    except Exception as e:
        print(f"Error fetching chain from {node}: {e}")
    return []

def sync_chain():
    global peer_nodes
    longest_chain = blockchain.chain

    for node in peer_nodes:
        peer_chain_data = fetch_chain_from_node(node)

        # Rebuild the chain as list of Block instances
        peer_chain = [Block.from_dict(b) for b in peer_chain_data]

        if len(peer_chain) > len(longest_chain) and is_valid_chain(peer_chain):
            longest_chain = peer_chain

    if longest_chain != blockchain.chain:
        blockchain.chain = longest_chain
        return True
    return False

def is_valid_chain(chain):
    for i in range(1, len(chain)):
        prev = chain[i - 1]
        curr = chain[i]
        if curr.previous_hash != prev.hash or curr.hash != curr.compute_hash():
            return False
    return True

self_url = None

def fetch_peers_from_node(node):
    try:
        res = requests.get(f"{node}/api/peers")
        if res.status_code == 200:
            return res.json().get("peers", [])
    except Exception:
        pass
    return []

def auto_discover_peers():
    discovered = set()
    for peer in list(peer_nodes):
        others = fetch_peers_from_node(peer)
        for node in others:
            if node != self_url:
                add_node(node)
                discovered.add(node)
    return list(discovered)

def bootstrap(bootstrap_nodes, self_node_url):
    global self_url
    self_url = self_node_url

    for node in bootstrap_nodes:
        if node == self_node_url:
            continue

        add_node(node)

        try:
            # Tell other node to add us
            requests.post(f"{node}/api/connect-node", json={"nodes": [self_node_url]})

            # Fetch its peers and sync
            others = fetch_peers_from_node(node)
            for peer in others:
                add_node(peer)

        except Exception as e:
            print(f"Failed to connect to bootstrap node {node}: {e}")

    newly_discovered = auto_discover_peers()
    print(f"Discovered {len(newly_discovered)} new peers")
    sync_chain()