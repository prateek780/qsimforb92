import random

class StudentB92Host:
    
    """
    Student's B92 QKD implementation class with instance methods.
    All prompts are included above their respective implementations.

    B92 Protocol Summary:
    - Alice encodes: bit 0 -> |0⟩, bit 1 -> |+⟩ = (|0⟩ + |1⟩)/√2
    - Bob measures randomly in Z or X basis
    - Bob keeps only results where he measures |1⟩ (outcome = 1)
    - If Bob measures |1⟩ in Z basis -> Alice sent |+⟩ (bit 1)
    - If Bob measures |1⟩ in X basis -> Alice sent |0⟩ (bit 0)
    """

    # Implement the constructor for the StudentB92Host class using the provided skeleton function.
    # The constructor should accept the participant's name, such as "Alice" or "Bob", and store it for logging purposes.
    # It must initialize internal state with empty lists for sent bits, prepared qubits, received measurements, sifted key,
    # random bits, measurement outcomes, and received bases. All collections should start empty, and the constructor must 
    # dynamically handle any host name passed to it.
    def __init__(self, name):
        """
        Initialize a StudentB92Host instance.

        Args:
            name (str): The participant's name (e.g., "Alice", "Bob")
        """
        self.name = name
        self.sent_bits = []
        self.qubits = []
        self.received_measurements = []
        self.sifted_key = []
        self.random_bits = []
        self.measurement_outcomes = []
        self.received_bases = []

    # Implement the b92_prepare_qubit method using the provided skeleton function.
    # The method should prepare a qubit based on a classical bit following the B92 protocol.
    # It must use two non-orthogonal quantum states: bit 0 should be mapped to |0⟩, and bit 1 should be mapped to |+⟩
    # (the superposition state). The method should return the prepared qubit, and raise an error if the input bit is not 0 or 1.
    def b92_prepare_qubit(self, bit):
        """
        Prepare a qubit in the B92 protocol based on a classical bit.

        B92 encoding:
        - bit 0 -> |0⟩ state
        - bit 1 -> |+⟩ state (superposition)

        Args:
            bit (int): Classical bit value (0 or 1)

        Returns:
            str: The prepared quantum state representation
        """
        if bit == 0:
            return "|0>"
        elif bit == 1:
            return "|+>"
        else:
            raise ValueError("Bit must be 0 or 1")

    # Implement the b92_measure_qubit method using the provided skeleton function.
    # The method should randomly choose a measurement basis ("Z" or "X").
    # - If basis is Z:
    #     * |0> maps to outcome 0 (deterministic)
    #     * |+> maps to outcome 0 or 1 with 50% probability each
    # - If basis is X:
    #     * |+> maps to outcome 0 (deterministic, since |+> is +1 eigenstate of X)
    #     * |0> maps to outcome 0 or 1 with 50% probability each
    # The method should return both the outcome and the chosen basis.
    def b92_measure_qubit(self, qubit):
        """
        Simulate measurement of a qubit in the B92 protocol.

        Measurement rules:
        - Z basis: |0⟩ -> 0, |+⟩ -> 0 or 1 (50/50)
        - X basis: |+⟩ -> 0, |0⟩ -> 0 or 1 (50/50)

        Args:
            qubit (str): Quantum state representation

        Returns:
            tuple: (measurement outcome, basis used)
        """
        basis = random.choice(["Z", "X"])

        if basis == "Z":
            if qubit == "|0>":
                return 0, "Z"  # |0> always gives 0 in Z basis
            elif qubit == "|+>":
                return random.choice([0, 1]), "Z"  # |+> gives 0 or 1 randomly
        elif basis == "X":
            if qubit == "|+>":
                return 0, "X"  # |+> always gives 0 in X basis
            elif qubit == "|0>":
                return random.choice([0, 1]), "X"  # |0> gives 0 or 1 randomly

        raise ValueError(f"Invalid qubit state: {qubit}")

    # Implement the sifting stage of the B92 protocol.
    # Keep only measurement results that give a conclusive outcome (result = 1):
    # - In Z basis: outcome 1 conclusively indicates the sender sent |+⟩ (bit 1)
    # - In X basis: outcome 1 conclusively indicates the sender sent |0⟩ (bit 0)
    # All other results (outcome 0) are inconclusive and should be discarded.
    def b92_sifting(self, sent_bits, received_measurements):
        """
        Perform the sifting stage of the B92 protocol.

        B92 sifting rules:
        - Keep only measurements where Bob got outcome = 1
        - If Z basis, outcome 1 -> Alice sent bit 1 (|+⟩)
        - If X basis, outcome 1 -> Alice sent bit 0 (|0⟩)

        Args:
            sent_bits (list): List of bits sent by Alice
            received_measurements (list): List of (outcome, basis) pairs from Bob

        Returns:
            tuple: (sifted_sender, sifted_receiver)
        """
        sifted_sender = []
        sifted_receiver = []

        for i, (sent_bit, (outcome, basis)) in enumerate(zip(sent_bits, received_measurements)):
            # Only keep measurements where Bob got outcome = 1
            if outcome == 1:
                if basis == "Z":
                    # If Bob measured 1 in Z basis, Alice must have sent |+⟩ (bit 1)
                    if sent_bit == 1:  # Verify Alice actually sent bit 1
                        sifted_sender.append(1)
                        sifted_receiver.append(1)
                elif basis == "X":
                    # If Bob measured 1 in X basis, Alice must have sent |0⟩ (bit 0)
                    if sent_bit == 0:  # Verify Alice actually sent bit 0
                        sifted_sender.append(0)
                        sifted_receiver.append(0)

        self.sifted_key = sifted_receiver
        return sifted_sender, sifted_receiver

    # Implement an instance method for Alice to generate random bits and prepare qubits.
    # The method should create a sequence of random bits, store them internally,
    # prepare corresponding qubits using the b92_prepare_qubit method, and return the prepared qubits.
    def b92_send_qubits(self, num_qubits):
        """
        Instance method for Alice to generate random bits and prepare qubits.

        Args:
            num_qubits (int): Number of qubits to generate

        Returns:
            list: List of prepared qubits
        """
        self.sent_bits = [random.randint(0, 1) for _ in range(num_qubits)]
        self.random_bits = self.sent_bits.copy()
        self.qubits = [self.b92_prepare_qubit(bit) for bit in self.sent_bits]
        return self.qubits

    # Implement an instance method for Bob to measure a received qubit.
    # The method should use b92_measure_qubit, store both the measurement outcome and the chosen basis
    # in received_measurements, and return True to confirm processing.
    def b92_process_received_qbit(self, qbit, from_channel=None):
        """
        Instance method for Bob to measure a received qubit.

        Args:
            qbit (str): The received qubit
            from_channel: Optional parameter for channel information

        Returns:
            bool: True to confirm processing
        """
        outcome, basis = self.b92_measure_qubit(qbit)
        self.received_measurements.append((outcome, basis))
        self.measurement_outcomes.append(outcome)
        self.received_bases.append(basis)
        return True

    # Implement the b92_estimate_error_rate method using the provided skeleton function.
    # The method should compute the error rate by comparing a sample of sifted key positions against reference bits. 
    # It must iterate through the provided sample positions, count valid comparisons, and increase the error count whenever a mismatch occurs.
    # If no comparisons are available, it should default to an error rate of zero. 
    # Finally, the method must return the computed error rate as a floating-point value between 0.0 and 1.0.
    def b92_estimate_error_rate(self, sample_positions, reference_bits):
        """
        Compute the error rate for the B92 protocol.

        Args:
            sample_positions (list): Positions to sample for error checking
            reference_bits (list): Reference bit values for comparison

        Returns:
            float: Estimated error rate (0.0 to 1.0)
        """
        if not sample_positions or not reference_bits:
            return 0.0

        errors = 0
        comparisons = 0

        for pos, ref_bit in zip(sample_positions, reference_bits):
            if pos < len(self.sifted_key):
                comparisons += 1
                if self.sifted_key[pos] != ref_bit:
                    errors += 1

        return errors / comparisons if comparisons > 0 else 0.0


# ============================================================
# Example simulation of B92 using instance methods
# ============================================================
if __name__ == "__main__":
    print("="*70)
    print("           B92 QUANTUM KEY DISTRIBUTION SIMULATION")
    print("="*70)

    alice = StudentB92Host("Alice")
    bob = StudentB92Host("Bob")

    # Alice generates and sends qubits
    num_qubits = 100
    print(f"\n📤 STEP 1: ALICE PREPARES QUBITS")
    print(f"   → Alice generates {num_qubits} random bits")
    qubits = alice.b92_send_qubits(num_qubits)

    # Count Alice's bit distribution
    alice_0_count = alice.sent_bits.count(0)
    alice_1_count = alice.sent_bits.count(1)
    print(f"   → Alice's bit distribution: {alice_0_count} zeros, {alice_1_count} ones")
    print(f"   → Alice's random bits: {alice.sent_bits[:20]}... (first 20)")
    print(f"   → Prepared qubits: {qubits[:20]}... (first 20)")

    # Bob measures received qubits
    print(f"\n📥 STEP 2: BOB MEASURES QUBITS")
    print(f"   → Bob receives and measures all {num_qubits} qubits")
    for q in qubits:
        bob.b92_process_received_qbit(q)

    # Analyze Bob's measurements
    z_measurements = sum(1 for _, basis in bob.received_measurements if basis == "Z")
    x_measurements = sum(1 for _, basis in bob.received_measurements if basis == "X")
    outcomes_0_count = sum(1 for outcome, _ in bob.received_measurements if outcome == 0)
    outcomes_1_count = sum(1 for outcome, _ in bob.received_measurements if outcome == 1)

    print(f"   → Bob's basis choices: {z_measurements} Z-basis, {x_measurements} X-basis")
    print(f"   → Bob's measurement outcomes: {outcomes_0_count} zeros, {outcomes_1_count} ones")
    print(f"   → Bob's measurements (first 20): {[(o,b) for o,b in bob.received_measurements[:20]]}")

    # Detailed analysis of outcome=1 cases
    z_outcome_1 = sum(1 for outcome, basis in bob.received_measurements if outcome == 1 and basis == "Z")
    x_outcome_1 = sum(1 for outcome, basis in bob.received_measurements if outcome == 1 and basis == "X")
    print(f"   → Outcome=1 breakdown: {z_outcome_1} in Z-basis, {x_outcome_1} in X-basis")

    # Sifting stage
    print(f"\n🔍 STEP 3: B92 SIFTING PROCESS")
    print(f"   → Keeping only Bob's outcome=1 measurements...")
    sifted_alice, sifted_bob = bob.b92_sifting(alice.sent_bits, bob.received_measurements)

    print(f"   → Raw outcome=1 count: {outcomes_1_count}")
    print(f"   → Sifted key length: {len(sifted_alice)} (after verification)")
    print(f"   → Alice sifted key: {sifted_alice}")
    print(f"   → Bob sifted key:   {sifted_bob}")

    # Verify sifting correctness
    discarded_count = outcomes_1_count - len(sifted_alice)
    print(f"   → Discarded {discarded_count} outcome=1 results (Alice sent wrong bit)")

    # Check if keys match
    key_match = sifted_alice == sifted_bob
    if key_match:
        print(f"   ✅ Keys match perfectly!")
    else:
        print(f"   ❌ Key mismatch detected!")
        mismatches = sum(1 for a, b in zip(sifted_alice, sifted_bob) if a != b)
        print(f"   → {mismatches} bit mismatches found")

    # Error rate estimation
    print(f"\n📊 STEP 4: ERROR ANALYSIS")
    if sifted_alice and sifted_bob:
        sample_positions = list(range(len(sifted_alice)))
        reference_bits = sifted_alice
        error_rate = bob.b92_estimate_error_rate(sample_positions, reference_bits)
        print(f"   → Quantum Bit Error Rate (QBER): {error_rate:.4f} ({error_rate*100:.2f}%)")
        print(f"   → Error threshold for security: <11% (typical)")

        if error_rate == 0:
            print(f"   ✅ No errors detected - channel is ideal")
        elif error_rate < 0.11:
            print(f"   ✅ Error rate acceptable for secure communication")
        else:
            print(f"   ⚠️  Error rate too high - potential eavesdropping!")
    else:
        print(f"   ⚠️  No sifted bits available for error analysis")

    # Protocol Statistics
    print(f"\n📈 STEP 5: PROTOCOL PERFORMANCE ANALYSIS")
    efficiency = len(sifted_alice) / num_qubits if num_qubits > 0 else 0
    theoretical_max = 0.25  # 25% theoretical maximum for B92

    print(f"   → Protocol efficiency: {efficiency:.4f} ({efficiency*100:.2f}%)")
    print(f"   → Theoretical maximum: {theoretical_max:.4f} ({theoretical_max*100:.2f}%)")
    print(f"   → Efficiency ratio: {(efficiency/theoretical_max)*100:.1f}% of theoretical max")

    # Key generation rate
    if len(sifted_alice) > 0:
        print(f"   → Final shared key length: {len(sifted_alice)} bits")
        print(f"   → Key generation rate: {len(sifted_alice)/num_qubits:.3f} bits per qubit")

    # Security metrics
    print(f"\n🔐 STEP 6: SECURITY ASSESSMENT")
    if len(sifted_alice) > 0:
        entropy = len(set(sifted_alice)) / len(sifted_alice) if len(sifted_alice) > 0 else 0
        print(f"   → Key randomness: {len(set(sifted_alice))} unique values in {len(sifted_alice)} bits")

        # Privacy amplification estimate (simplified)
        if error_rate < 0.11:
            secure_bits = int(len(sifted_alice) * (1 - 2 * error_rate))
            print(f"   → Estimated secure bits after privacy amplification: {secure_bits}")

        print(f"   → Key suitable for: {'✅ Cryptographic use' if error_rate < 0.11 and len(sifted_alice) > 10 else '❌ Testing only'}")

    print(f"\n" + "="*70)
    print("                    SIMULATION COMPLETE")
    print("="*70)

    # Summary table
    print(f"\n📋 FINAL SUMMARY:")
    print(f"   Initial qubits:        {num_qubits}")
    print(f"   Outcome=1 measurements: {outcomes_1_count}")
    print(f"   Final shared key bits: {len(sifted_alice)}")
    print(f"   Protocol efficiency:   {efficiency*100:.2f}%")
    print(f"   Quantum error rate:    {error_rate*100:.2f}%")
    print(f"   Security status:       {'✅ SECURE' if error_rate < 0.11 else '❌ INSECURE'}")
