"""
File storage fallback for topologies when Redis is not available
"""

import json
import os
from typing import List, Dict, Any, Optional
from data.models.topology.world_model import WorldModal

TOPOLOGY_DIR = "saved_topologies"

def ensure_topology_dir():
    """Ensure the topology directory exists"""
    if not os.path.exists(TOPOLOGY_DIR):
        os.makedirs(TOPOLOGY_DIR)

def save_topology_to_file(world: WorldModal) -> bool:
    """Save topology to file"""
    try:
        ensure_topology_dir()
        
        # Convert to dict and save
        world_data = world.model_dump()
        filename = f"{world.name.replace(' ', '_')}.json"
        filepath = os.path.join(TOPOLOGY_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(world_data, f, indent=2)
        
        print(f"✅ Topology saved to {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving topology to file: {e}")
        return False

def load_topology_from_file(filename: str) -> Optional[WorldModal]:
    """Load topology from file"""
    try:
        filepath = os.path.join(TOPOLOGY_DIR, filename)
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return WorldModal(**data)
        
    except Exception as e:
        print(f"❌ Error loading topology from file: {e}")
        return None

def load_all_topologies_from_file(temporary_world: bool = False, owner: str = None) -> List[Dict[str, Any]]:
    """Load all topologies from files"""
    try:
        ensure_topology_dir()
        
        topologies = []
        for filename in os.listdir(TOPOLOGY_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(TOPOLOGY_DIR, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    # Filter by temporary_world and owner if specified
                    if temporary_world is not None and data.get('temporary_world') != temporary_world:
                        continue
                    if owner is not None and data.get('owner') != owner:
                        continue
                    
                    # Add filename as pk for compatibility
                    data['pk'] = filename.replace('.json', '')
                    topologies.append(data)
                    
                except Exception as e:
                    print(f"⚠️ Error loading {filename}: {e}")
                    continue
        
        print(f"✅ Loaded {len(topologies)} topologies from files")
        return topologies
        
    except Exception as e:
        print(f"❌ Error loading topologies from files: {e}")
        return []

def create_sample_topologies():
    """Create sample topologies for testing"""
    ensure_topology_dir()
    
    # Sample topology 1: test1
    test1_topology = {
        "name": "test1",
        "size": [1000, 1000],
        "zones": [
            {
                "name": "Zone1",
                "position": [0, 0],
                "size": [500, 500],
                "networks": [
                    {
                        "name": "QuantumNetwork1",
                        "hosts": [
                            {
                                "name": "Alice",
                                "position": [100, 100],
                                "type": "InteractiveQuantumHost"
                            },
                            {
                                "name": "Bob", 
                                "position": [200, 200],
                                "type": "InteractiveQuantumHost"
                            }
                        ],
                        "channels": [
                            {
                                "name": "Alice-Bob",
                                "from_host": "Alice",
                                "to_host": "Bob",
                                "length": 100.0,
                                "loss_per_km": 0.1
                            }
                        ]
                    }
                ]
            }
        ],
        "temporary_world": False,
        "lab_world": False,
        "owner": "Default"
    }
    
    # Sample topology 2: myworld
    myworld_topology = {
        "name": "myworld",
        "size": [1200, 1200],
        "zones": [
            {
                "name": "MainZone",
                "position": [0, 0],
                "size": [600, 600],
                "networks": [
                    {
                        "name": "QuantumNetwork2",
                        "hosts": [
                            {
                                "name": "Alice",
                                "position": [150, 150],
                                "type": "InteractiveQuantumHost"
                            },
                            {
                                "name": "Bob", 
                                "position": [300, 300],
                                "type": "InteractiveQuantumHost"
                            },
                            {
                                "name": "Eve",
                                "position": [450, 150],
                                "type": "InteractiveQuantumHost"
                            }
                        ],
                        "channels": [
                            {
                                "name": "Alice-Bob",
                                "from_host": "Alice",
                                "to_host": "Bob",
                                "length": 150.0,
                                "loss_per_km": 0.1
                            },
                            {
                                "name": "Bob-Eve",
                                "from_host": "Bob",
                                "to_host": "Eve",
                                "length": 150.0,
                                "loss_per_km": 0.1
                            }
                        ]
                    }
                ]
            }
        ],
        "temporary_world": False,
        "lab_world": False,
        "owner": "Default"
    }
    
    # Save both topologies
    for name, topology in [("test1", test1_topology), ("myworld", myworld_topology)]:
        filename = f"{name}.json"
        filepath = os.path.join(TOPOLOGY_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(topology, f, indent=2)
        
        print(f"✅ Created {filename}")

if __name__ == "__main__":
    print("🔧 Creating sample topologies...")
    create_sample_topologies()
    
    print("\n🔍 Testing file storage...")
    topologies = load_all_topologies_from_file()
    print(f"Found {len(topologies)} topologies:")
    for topo in topologies:
        print(f"  - {topo['name']} (owner: {topo.get('owner', 'Unknown')})")
