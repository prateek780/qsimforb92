#!/usr/bin/env python3
"""
Create sample topologies for the simulation UI
"""

import json
import os

def create_sample_topologies():
    """Create sample topologies for testing"""
    
    # Create saved_topologies directory
    if not os.path.exists('saved_topologies'):
        os.makedirs('saved_topologies')
    
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
    
    # Sample topology 3: simple_network
    simple_network_topology = {
        "name": "simple_network",
        "size": [800, 800],
        "zones": [
            {
                "name": "SimpleZone",
                "position": [0, 0],
                "size": [400, 400],
                "networks": [
                    {
                        "name": "SimpleQuantumNetwork",
                        "hosts": [
                            {
                                "name": "Alice",
                                "position": [100, 100],
                                "type": "InteractiveQuantumHost"
                            },
                            {
                                "name": "Bob", 
                                "position": [300, 300],
                                "type": "InteractiveQuantumHost"
                            }
                        ],
                        "channels": [
                            {
                                "name": "Alice-Bob",
                                "from_host": "Alice",
                                "to_host": "Bob",
                                "length": 200.0,
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
    
    # Save all topologies
    topologies = [
        ("test1", test1_topology),
        ("myworld", myworld_topology),
        ("simple_network", simple_network_topology)
    ]
    
    for name, topology in topologies:
        filename = f"saved_topologies/{name}.json"
        
        with open(filename, 'w') as f:
            json.dump(topology, f, indent=2)
        
        print(f"✅ Created {filename}")
    
    print(f"\n🎉 Created {len(topologies)} sample topologies!")
    print("These should now appear in the simulation UI")

if __name__ == "__main__":
    create_sample_topologies()
