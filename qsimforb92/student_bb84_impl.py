# coding: utf-8
# %%
import random


class StudentQuantumHost:
    """
    Your personal BB84 implementation!
    This class will be used by the quantum network simulation.
    """

    # PROMPT FOR CONSTRUCTOR:
    """
    Implement a constructor for the StudentQuantumHost class using the provided skeleton function.
    The constructor should accept a name for the host, such as 'Alice' or 'Bob', and store it so it
    can be used in log messages. It should also create empty lists to keep track of random classical bits 
    generated, measurement bases chosen, quantum states encoded, measurement bases used when 
    receiving qubits, and measurement outcomes obtained. After initializing these lists, 
    the constructor must print a welcome message that dynamically includes the host's name, 
    for example: 🔹 StudentQuantumHost '<host name>' initialized successfully!
    All lists must start empty, and the host name handling must be dynamic so that
    it works for any name passed in.
    """

    def __init__(self, name):
        """
        Initialize a StudentQuantumHost instance.

        Args:
            name (str): The name of the quantum host (e.g., 'Alice', 'Bob')
        """
        # Store the host name for use in log messages
        self.name = name

        # Initialize empty lists to track quantum communication data
        self.random_bits = []              # Random classical bits generated
        self.measurement_bases = []        # Measurement bases chosen for encoding
        self.quantum_states = []           # Quantum states encoded
        self.received_bases = []           # Measurement bases used when receiving qubits
        self.measurement_outcomes = []     # Measurement outcomes obtained

        # Print dynamic welcome message
        print(f"🔹 StudentQuantumHost '{self.name}' initialized successfully!")

    # PROMPT FOR BB84_SEND_QUBITS METHOD:
    """
    Implement the bb84_send_qubits method for the StudentQuantumHost class using the
    provided skeleton function. The method should begin by displaying a message that mentions
    the identity of the sender and the total number of qubits to be processed.
    It should then reinitialize any internal storage structures that will hold preparation data. 
    For each qubit, the method must create a random classical value, choose a random preparation setting, 
    transform the classical value into a quantum state using the chosen setting, and store the results
    in the internal collections. After all qubits are processed, the method should display a summary 
    that includes how many qubits were prepared, a preview of the generated values, and a preview of the chosen settings. 
    Finally, the method should return the collection of prepared quantum states.
    """

    def bb84_send_qubits(self, num_qubits):
        """
        Alice's BB84 implementation: Prepare and send qubits

        Args:
            num_qubits: Number of qubits to prepare

        Returns:
            List of encoded qubits
        """
        import random

        # Display initial message with sender identity and total qubits
        print(f"🔹 {self.name} is preparing {num_qubits} qubits for BB84 transmission...")

        # Reinitialize internal storage structures for preparation data
        self.random_bits = []
        self.measurement_bases = []
        self.quantum_states = []

        # Process each qubit
        for i in range(num_qubits):
            # Create a random classical value (0 or 1)
            classical_bit = random.randint(0, 1)

            # Choose a random preparation setting (basis: 0 for rectilinear, 1 for diagonal)
            preparation_basis = random.randint(0, 1)

            # Transform classical value into quantum state using chosen setting
            if preparation_basis == 0:  # Rectilinear basis (Z-basis)
                if classical_bit == 0:
                    quantum_state = "|0⟩"  # |0⟩ state
                else:
                    quantum_state = "|1⟩"  # |1⟩ state
            else:  # Diagonal basis (X-basis)
                if classical_bit == 0:
                    quantum_state = "|+⟩"  # |+⟩ state = (|0⟩ + |1⟩)/√2
                else:
                    quantum_state = "|-⟩"  # |-⟩ state = (|0⟩ - |1⟩)/√2

            # Store results in internal collections
            self.random_bits.append(classical_bit)
            self.measurement_bases.append(preparation_basis)
            self.quantum_states.append(quantum_state)

        # Display summary after all qubits are processed
        print(f"📊 Summary for {self.name}:")
        print(f"   • Prepared {len(self.quantum_states)} qubits")
        print(f"   • Random bits preview: {self.random_bits[:min(10, len(self.random_bits))]}{'...' if len(self.random_bits) > 10 else ''}")
        print(f"   • Preparation bases preview: {self.measurement_bases[:min(10, len(self.measurement_bases))]}{'...' if len(self.measurement_bases) > 10 else ''}")
        print(f"   • Quantum states preview: {self.quantum_states[:min(10, len(self.quantum_states))]}{'...' if len(self.quantum_states) > 10 else ''}")

        # Return the collection of prepared quantum states
        return self.quantum_states

    # PROMPT FOR PROCESS_RECEIVED_QBIT METHOD:
    """
    Implement the process_received_qbit method for the StudentQuantumHost class using the provided skeleton function.
    The method should select a random measurement setting to determine how the incoming quantum state will be observed and 
    record this chosen setting in the appropriate internal collection. It must then perform a measurement of the received
    quantum state using the chosen setting and store the resulting outcome in the internal collection of measurement results. 
    The method should indicate successful processing by returning a confirmation value.
    """

    def process_received_qbit(self, qbit, from_channel):
        """
        Bob's BB84 implementation: Receive and measure qubits

        Args:
            qbit: The received quantum state
            from_channel: The quantum channel (not used in this implementation)

        Returns:
            True if successful
        """
        import random

        # Select a random measurement setting (0 for rectilinear, 1 for diagonal)
        measurement_basis = random.randint(0, 1)

        # Record the chosen setting in the appropriate internal collection
        self.received_bases.append(measurement_basis)

        # Perform measurement of the received quantum state using the chosen setting
        if measurement_basis == 0:  # Rectilinear basis (Z-basis) measurement
            if qbit == "|0⟩":
                outcome = 0  # Measuring |0⟩ in Z-basis always gives 0
            elif qbit == "|1⟩":
                outcome = 1  # Measuring |1⟩ in Z-basis always gives 1
            elif qbit == "|+⟩":
                outcome = random.randint(0, 1)  # |+⟩ in Z-basis: 50% chance of 0 or 1
            elif qbit == "|-⟩":
                outcome = random.randint(0, 1)  # |-⟩ in Z-basis: 50% chance of 0 or 1
            else:
                # Handle unexpected quantum state
                outcome = random.randint(0, 1)

        else:  # Diagonal basis (X-basis) measurement
            if qbit == "|+⟩":
                outcome = 0  # Measuring |+⟩ in X-basis always gives 0
            elif qbit == "|-⟩":
                outcome = 1  # Measuring |-⟩ in X-basis always gives 1
            elif qbit == "|0⟩":
                outcome = random.randint(0, 1)  # |0⟩ in X-basis: 50% chance of 0 or 1
            elif qbit == "|1⟩":
                outcome = random.randint(0, 1)  # |1⟩ in X-basis: 50% chance of 0 or 1
            else:
                # Handle unexpected quantum state
                outcome = random.randint(0, 1)

        # Store the resulting outcome in the internal collection of measurement results
        self.measurement_outcomes.append(outcome)

        # Return confirmation value indicating successful processing
        return True

    # PROMPT FOR BB84_RECONCILE_BASES METHOD:
    """
    Implement the bb84_reconcile_bases method for the StudentQuantumHost class using the provided skeleton function.
    The method should start by displaying a message that indicates the participant is comparing basis choices. 
    It must create two empty collections: one for indices where the bases align and another for the corresponding bit values. 
    The method should iterate through both sets of basis choices simultaneously with their positions, and for each position,
    if the two bases are the same, it should record the index, and if a corresponding measurement result exists,
    it should also record the measured value. After completing the comparison, the method must display a summary that shows 
    how many matches were found and the proportion of matches relative to the total comparisons.
    Finally, it should return both the list of matching indices and the list of corresponding bit values.
    """

    def bb84_reconcile_bases(self, alice_bases, bob_bases):
        """
        BB84 basis reconciliation: Find matching measurement bases

        Args:
            alice_bases: List of Alice's preparation bases
            bob_bases: List of Bob's measurement bases

        Returns:
            Tuple of (matching_indices, corresponding_bits)
        """
        # Display message indicating basis comparison
        print(f"🔹 {self.name} is comparing basis choices for reconciliation...")

        # Create empty collections for matching indices and corresponding bit values
        matching_indices = []
        corresponding_bits = []

        # Iterate through both sets of basis choices simultaneously with their positions
        for position, (alice_basis, bob_basis) in enumerate(zip(alice_bases, bob_bases)):
            # Check if the two bases are the same
            if alice_basis == bob_basis:
                # Record the index where bases align
                matching_indices.append(position)

                # If a corresponding measurement result exists, record the measured value
                if position < len(self.measurement_outcomes):
                    corresponding_bits.append(self.measurement_outcomes[position])
                elif position < len(self.random_bits):
                    # For Alice, use the original random bits
                    corresponding_bits.append(self.random_bits[position])

        # Display summary after completing the comparison
        total_comparisons = min(len(alice_bases), len(bob_bases))
        matches_found = len(matching_indices)
        match_proportion = matches_found / total_comparisons if total_comparisons > 0 else 0

        print(f"📊 Basis Reconciliation Summary for {self.name}:")
        print(f"   • Matches found: {matches_found}")
        print(f"   • Total comparisons: {total_comparisons}")
        print(f"   • Match proportion: {match_proportion:.3f} ({match_proportion*100:.1f}%)")
        print(f"   • Matching indices: {matching_indices[:min(10, len(matching_indices))]}{'...' if len(matching_indices) > 10 else ''}")

        # Return both the list of matching indices and corresponding bit values
        return matching_indices, corresponding_bits

    # PROMPT FOR BB84_ESTIMATE_ERROR_RATE METHOD:
    """
    Implement the bb84_estimate_error_rate method for the StudentQuantumHost class using the provided skeleton function.
    The method should begin by showing a message that indicates the participant is calculating the error rate.
    It must set up counters to track how many comparisons are made and how many discrepancies are found.
    The method should then iterate through the provided sample of reference bits along with their positions, and for each entry,
    if the position is valid relative to this host's recorded outcomes, it should increase the comparison count,
    and if the recorded outcome does not match the provided bit, it should increase the error count. 
    After processing all samples, the method should calculate the error rate as the ratio of errors to comparisons,
    defaulting to zero if no comparisons were made. The method must display a summary that includes 
    the calculated error rate and the raw error/total comparison counts. Finally, it should return the computed error rate.
    """

    def bb84_estimate_error_rate(self, sample_positions, reference_bits):
        """
        BB84 error rate estimation: Compare sample bits to detect eavesdropping

        Args:
            sample_positions: List of positions to sample for error checking
            reference_bits: List of reference bit values to compare against

        Returns:
            Float representing the estimated error rate (0.0 to 1.0)
        """
        # Display message indicating error rate calculation
        print(f"🔹 {self.name} is calculating the error rate from sample comparison...")

        # Set up counters to track comparisons and discrepancies
        comparison_count = 0
        error_count = 0

        # Iterate through the provided sample positions and reference bits
        for position, reference_bit in zip(sample_positions, reference_bits):
            # Check if the position is valid relative to this host's recorded outcomes
            if position < len(self.measurement_outcomes):
                # Increase the comparison count for valid positions
                comparison_count += 1

                # Get the recorded outcome for this position
                recorded_outcome = self.measurement_outcomes[position]

                # If the recorded outcome does not match the provided reference bit, increase error count
                if recorded_outcome != reference_bit:
                    error_count += 1
            elif position < len(self.random_bits):
                # For Alice's case, compare against original random bits
                comparison_count += 1
                recorded_outcome = self.random_bits[position]

                if recorded_outcome != reference_bit:
                    error_count += 1

        # Calculate error rate as ratio of errors to comparisons, defaulting to zero if no comparisons
        error_rate = error_count / comparison_count if comparison_count > 0 else 0.0

        # Display summary with calculated error rate and raw counts
        print(f"📊 Error Rate Estimation Summary for {self.name}:")
        print(f"   • Total comparisons: {comparison_count}")
        print(f"   • Errors detected: {error_count}")
        print(f"   • Calculated error rate: {error_rate:.4f} ({error_rate*100:.2f}%)")

        # Interpret the error rate
        if error_rate == 0.0:
            print(f"   • Status: No errors detected - channel appears secure")
        elif error_rate <= 0.11:  # Typical threshold for BB84
            print(f"   • Status: Low error rate - likely due to noise")
        else:
            print(f"   • Status: High error rate - possible eavesdropping detected!")

        # Return the computed error rate
        return error_rate


def main():
    print("=" * 70)
    print("🚀 BB84 QUANTUM KEY DISTRIBUTION PROTOCOL DEMONSTRATION")
    print("=" * 70)
    print()

    # Step 1: Create quantum hosts (this will trigger __init__ messages)
    print("📡 STEP 1: Initializing Quantum Hosts")
    print("-" * 40)
    alice = StudentQuantumHost("Alice")
    bob = StudentQuantumHost("Bob")
    charlie = StudentQuantumHost("Charlie")  # Extra host to show dynamic behavior
    print()

    # Step 2: Alice prepares and sends qubits
    print("📡 STEP 2: Quantum Transmission Phase")
    print("-" * 40)
    num_qubits = 15
    quantum_states = alice.bb84_send_qubits(num_qubits)
    print()

    # Step 3: Bob receives and measures each qubit
    print("📡 STEP 3: Quantum Measurement Phase")
    print("-" * 40)
    print(f"🔹 {bob.name} is receiving and measuring {len(quantum_states)} qubits...")
    for i, qbit in enumerate(quantum_states):
        success = bob.process_received_qbit(qbit, None)
        if i < 5:  # Show first 5 measurements in detail
            print(f"   • Qubit {i+1}: {qbit} → Measured with basis {bob.received_bases[-1]} → Result: {bob.measurement_outcomes[-1]}")
        elif i == 5:
            print("   • ... (remaining measurements processed)")
    print(f"✅ {bob.name} completed measuring all {len(quantum_states)} qubits!")
    print()

    # Step 4: Basis reconciliation
    print("📡 STEP 4: Basis Reconciliation Phase")
    print("-" * 40)
    matching_indices, alice_bits = alice.bb84_reconcile_bases(alice.measurement_bases, bob.received_bases)
    matching_indices, bob_bits = bob.bb84_reconcile_bases(alice.measurement_bases, bob.received_bases)
    print()

    # Step 5: Error rate estimation
    print("📡 STEP 5: Error Rate Estimation Phase")
    print("-" * 40)
    # Sample some positions for error checking
    if len(matching_indices) > 5:
        sample_positions = matching_indices[:5]  # Use first 5 matching positions
        alice_sample_bits = [alice_bits[i] for i in range(min(5, len(alice_bits)))]
        bob_sample_bits = [bob_bits[i] for i in range(min(5, len(bob_bits)))]

        # Alice estimates error rate
        alice_error_rate = alice.bb84_estimate_error_rate(sample_positions, bob_sample_bits)
        print()

        # Bob estimates error rate  
        bob_error_rate = bob.bb84_estimate_error_rate(sample_positions, alice_sample_bits)
        print()
    else:
        print("⚠️ Not enough matching bases for error rate estimation")
        print()

    # Step 6: Demonstrate with different host (Charlie)
    print("📡 STEP 6: Demonstrating Dynamic Host Names")
    print("-" * 40)
    charlie_states = charlie.bb84_send_qubits(8)

    # Charlie does basis reconciliation with Alice
    charlie_indices, charlie_bits = charlie.bb84_reconcile_bases(charlie.measurement_bases, alice.measurement_bases)

    # Charlie estimates error rate
    if len(charlie_indices) > 2:  
        sample_pos = charlie_indices[:3]
        sample_bits = [charlie_bits[i] for i in range(min(3, len(charlie_bits)))]
        charlie_error_rate = charlie.bb84_estimate_error_rate(sample_pos, sample_bits)
    print()

    print("=" * 70)
    print("✅ BB84 PROTOCOL DEMONSTRATION COMPLETE!")
    print("All methods successfully called and messages displayed!")
    print("=" * 70)


# Run the demonstration
if __name__ == "__main__":
    main()
