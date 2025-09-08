import random

class StudentB92Host:
    """
    Student's B92 QKD implementation class with instance methods.
    All prompts are included above their respective implementations.
    """

    # PROMPT FOR __init__ METHOD:
    # Implement the constructor for the participant.
    # Store participant name and initialize internal state for:
    # sent bits, prepared qubits, received measurements, and sifted key.

    def __init__(self, name):
        self.name = name
        self.sent_bits = []
        self.qubits = []
        self.received_measurements = []
        self.sifted_key = []
        self.random_bits = []
        self.measurement_outcomes = []
        self.received_bases = []

    # PROMPT FOR b92_prepare_qubit FUNCTION:
    # Implement a function that prepares a qubit based on a classical bit.
    # Use two non-orthogonal quantum states:
    #   - Bit 0 -> |0>
    #   - Bit 1 -> |+> (superposition state)
    # Return the prepared qubit.
    def b92_prepare_qubit(self, bit):
        if bit == 0:
            return "|0>"
        elif bit == 1:
            return "|+>"
        else:
            raise ValueError("Bit must be 0 or 1")

    # PROMPT FOR b92_measure_qubit FUNCTION:
    # Implement a function to simulate measurement in the B92 protocol.
    # Receiver chooses randomly between Z-basis {|0>, |1>} or X-basis {|+>, |->}.
    # Return the measurement outcome and basis used.
    def b92_measure_qubit(self, qubit):
        basis = random.choice(["Z", "X"])
        if basis == "Z":
            if qubit == "|0>":
                return 0, "Z"
            elif qubit == "|+>":
                return random.choice([0, 1]), "Z"
        else:
            if qubit == "|+>":
                return 0, "X"
            elif qubit == "|0>":
                return random.choice([0, 1]), "X"

    # PROMPT FOR b92_sifting FUNCTION:
    # Implement the sifting stage of the B92 protocol.
    # Keep only measurement results that give a conclusive outcome:
    # - Z-basis: outcome 1 -> sender sent |+>
    # - X-basis: outcome 1 -> sender sent |0>
    # Discard inconclusive results.
    def b92_sifting(self, sent_bits, received_measurements):
        sifted_sender = []
        sifted_receiver = []
        for bit, (outcome, basis) in zip(sent_bits, received_measurements):
            if basis == "Z" and outcome == 1:
                sifted_sender.append(1)
                sifted_receiver.append(1)
            elif basis == "X" and outcome == 1:
                sifted_sender.append(0)
                sifted_receiver.append(0)

        self.sifted_key = sifted_receiver
        return sifted_sender, sifted_receiver

    # PROMPT FOR b92_send_qubits METHOD:
    # Implement an instance method for Alice to generate random bits and prepare qubits.
    # Store sent bits and qubits internally.
    def b92_send_qubits(self, num_qubits):
        self.sent_bits = [random.randint(0, 1) for _ in range(num_qubits)]
        self.random_bits = self.sent_bits.copy()
        self.qubits = [self.b92_prepare_qubit(bit) for bit in self.sent_bits]
        return self.qubits

    # PROMPT FOR b92_process_received_qbit METHOD:
    # Implement an instance method for Bob to measure a received qubit.
    # Store the outcome and basis in received_measurements.
    def b92_process_received_qbit(self, qbit, from_channel=None):
        outcome, basis = self.b92_measure_qubit(qbit)
        self.received_measurements.append((outcome, basis))
        self.measurement_outcomes.append(outcome)
        self.received_bases.append(basis)
        return True

    # PROMPT FOR b92_estimate_error_rate METHOD:
    # Implement an instance method to compute the error rate using a sample of sifted key positions.
    def b92_estimate_error_rate(self, sample_positions, reference_bits):
        if not sample_positions or not reference_bits:
            return 0.0

        errors = 0
        comparisons = 0

        for pos, ref_bit in zip(sample_positions, reference_bits):
            if pos < len(self.measurement_outcomes):
                comparisons += 1
                if self.measurement_outcomes[pos] != ref_bit:
                    errors += 1
            elif pos < len(self.random_bits):
                comparisons += 1
                if self.random_bits[pos] != ref_bit:
                    errors += 1

        return errors / comparisons if comparisons > 0 else 0.0


# ============================================================
# Example simulation of B92 using instance methods
# ============================================================
if __name__ == "__main__":
    alice = StudentB92Host("Alice")
    bob = StudentB92Host("Bob")

    # Alice generates and sends qubits
    qubits = alice.b92_send_qubits(20)

    # Bob measures received qubits
    for q in qubits:
        bob.b92_process_received_qbit(q)

    # Sifting stage
    sifted_alice, sifted_bob = bob.b92_sifting(alice.sent_bits, bob.received_measurements)
    print("Alice sifted key:", sifted_alice)
    print("Bob sifted key:", sifted_bob)

    # Error rate estimation on the full sifted key
    if sifted_alice and sifted_bob:
        sample_positions = list(range(min(len(sifted_alice), len(sifted_bob))))
        reference_bits = [sifted_alice[i] for i in sample_positions]
        error_rate = bob.b92_estimate_error_rate(sample_positions, reference_bits)
        print("Estimated error rate:", error_rate)
