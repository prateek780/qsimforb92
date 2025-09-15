import { LogI, LogLevel } from "./simulation-logs";

/**
 * Convert a simulation event to a log entry for B92 protocol
 * This parser handles B92-specific events from the enhanced B92 bridge
 */
export function convertEventToLogB92(eventData: any): any {
    if (!eventData) return null;

    let level = LogLevel.STORY;
    let source = 'Unknown';
    let message = 'Received data in unhandled format.';

    // Filter out irrelevant classical network logs when B92 is running
    if (eventData?.data?.type && eventData.data.type.startsWith('student_b92')) {
        // Prioritize B92 events - they are more important
    } else if (eventData?.message && eventData.message.includes('Received data in unhandled format')) {
        // Skip unhandled format messages when B92 is active
        return null;
    }

    try {
        // Check if it's a simulation_event structure (has event_type and node)
        if (typeof eventData === 'object' && eventData !== null && eventData.event_type !== undefined && eventData.node !== undefined) {

            source = eventData.node || source;
            // The actual event type is in data.type, not event_type
            const eventType = eventData.data?.type || eventData.event_type;
            const eventDetails = eventData.data; // Specific details for this event type

            // Handle B92 events based on message content since bridge doesn't use type parameter
            if (eventDetails?.message) {
                const msg = eventDetails.message;
                
                if (msg.includes('STUDENT B92: Starting with') && msg.includes('qubits using your code')) {
                    level = LogLevel.PROTOCOL;
                    const numQubits = eventDetails?.num_qubits || 0;
                    message = `🔬 Student B92 implementation: Starting protocol with ${numQubits} qubits`;
                } else if (msg.includes('STUDENT ALICE data: Generated') && msg.includes('bits and') && msg.includes('bases')) {
                    level = LogLevel.PROTOCOL;
                    message = `🔬 Student Alice data: Generated ${eventDetails?.message?.match(/(\d+)/g)?.[0] || 0} bits and ${eventDetails?.message?.match(/(\d+)/g)?.[1] || 0} bases`;
                } else if (msg.includes('STUDENT ALICE: Prepared') && msg.includes('qubits using b92_send_qubits')) {
                    level = LogLevel.PROTOCOL;
                    const qubitsPrepared = eventDetails?.message?.match(/(\d+)/g)?.[0] || 0;
                    message = `🔬 Student Alice: Prepared ${qubitsPrepared} qubits using b92_send_qubits() [b92_send_qubits] (${qubitsPrepared} qubits)`;
                } else if (msg.includes('STUDENT ALICE: Prepared qubit') && msg.includes('bit') && msg.includes('->')) {
                    level = LogLevel.PROTOCOL;
                    message = `🔬 Student Alice: ${msg.split('STUDENT ALICE: ')[1]} [b92_prepare_qubit]`;
                } else if (msg.includes('STUDENT BOB: Measured qubit') && msg.includes('outcome') && msg.includes('basis')) {
                    level = LogLevel.PROTOCOL;
                    message = `🔬 Student Bob: ${msg.split('STUDENT BOB: ')[1]} [b92_measure_qubit]`;
                } else if (msg.includes('STUDENT B92: Sending') && msg.includes('encoded qubits from Alice')) {
                    level = LogLevel.STORY;
                    const qubitsSent = eventDetails?.qubits_sent || 0;
                    message = `🔬 Student B92: Sending ${qubitsSent} encoded qubits from Alice's b92_send_qubits() through quantum channel (${qubitsSent} qubits) - Sample: [|0>, |+>, |0>...]`;
                } else if (msg.includes('STUDENT BOB: Received qubit') && msg.includes('!')) {
                    level = LogLevel.PROTOCOL;
                    const received = eventDetails?.qubits_received || 0;
                    const total = eventDetails?.total_expected || 0;
                    message = `🔬 Student Bob: Received qubit ${received}/${total}!`;
                } else if (msg.includes('STUDENT BOB: Received all') && msg.includes('qubits, ready for b92_sifting')) {
                    level = LogLevel.PROTOCOL;
                    const received = eventDetails?.message?.match(/(\d+)/g)?.[0] || 0;
                    message = `🔬 Student Bob: Received all ${received} qubits, ready for b92_sifting() [b92_sifting]`;
                } else if (msg.includes('STUDENT BOB: Starting sifting process')) {
                    level = LogLevel.PROTOCOL;
                    message = `🔬 Student Bob: Starting sifting process with Alice's bits [b92_sifting]`;
                } else if (msg.includes('STUDENT BOB b92_sifting(): Found') && msg.includes('sifted bits out of')) {
                    level = LogLevel.PROTOCOL;
                    const siftedBits = eventDetails?.shared_bases || 0;
                    const totalBits = eventDetails?.message?.match(/(\d+)/g)?.[1] || 0;
                    const efficiency = eventDetails?.efficiency || 0;
                    message = `🔬 Student Bob b92_sifting(): Found ${siftedBits} sifted bits out of ${totalBits} (Efficiency: ${efficiency.toFixed(1)}%) [b92_sifting] (${siftedBits} sifted bits) (${efficiency.toFixed(1)}% efficiency)`;
                } else if (msg.includes('STUDENT BOB: Sifting completed')) {
                    level = LogLevel.PROTOCOL;
                    const siftedBits = eventDetails?.shared_bases || 0;
                    message = `🔬 Student Bob: Sifting completed - found ${siftedBits} sifted bits [b92_sifting]`;
                } else if (msg.includes('STUDENT BOB: Starting error rate estimation process')) {
                    level = LogLevel.PROTOCOL;
                    message = `🔬 Student Bob: Starting error rate estimation process [b92_estimate_error_rate]`;
                } else if (msg.includes('STUDENT BOB b92_estimate_error_rate():') && msg.includes('error rate') && msg.includes('errors) using student implementation')) {
                    level = LogLevel.PROTOCOL;
                    const errorRate = eventDetails?.error_rate || 0;
                    const errorCount = eventDetails?.message?.match(/(\d+)\/(\d+)/)?.[0] || '0/0';
                    message = `🔬 Student Bob b92_estimate_error_rate(): ${(errorRate * 100).toFixed(1)}% error rate (${errorCount} errors) using student implementation [b92_estimate_error_rate] (${(errorRate * 100).toFixed(1)}% error rate) (${errorCount} errors)`;
                } else if (msg.includes('STUDENT BOB: Error rate') && msg.includes('using b92_estimate_error_rate')) {
                    level = LogLevel.PROTOCOL;
                    const errorRate = eventDetails?.error_rate || 0;
                    message = `🔬 Student Bob: Error rate ${(errorRate * 100).toFixed(1)}% using b92_estimate_error_rate()!`;
                } else if (msg.includes('STUDENT BOB: WARNING - Alice has no sent_bits data for sifting')) {
                    level = LogLevel.WARNING;
                    message = `⚠️ Student Bob: WARNING - Alice has no sent_bits data for sifting [b92_sifting]`;
                } else if (msg.includes('STUDENT BOB: WARNING - Bob has no received_measurements data for sifting')) {
                    level = LogLevel.WARNING;
                    message = `⚠️ Student Bob: WARNING - Bob has no received_measurements data for sifting [b92_sifting]`;
                } else if (msg.includes('STUDENT BOB: WARNING - No data available for error estimation')) {
                    level = LogLevel.WARNING;
                    message = `⚠️ Student Bob: WARNING - No data available for error estimation [b92_estimate_error_rate]`;
                } else if (msg.includes('WARNING: Bridge not attached to host')) {
                    level = LogLevel.WARNING;
                    message = `⚠️ Warning: Bridge not attached to host`;
                } else if (msg.includes('WARNING: Alice has no sent_bits data - using student implementation with empty data')) {
                    level = LogLevel.WARNING;
                    message = `⚠️ Warning: Alice has no sent_bits data - using student implementation with empty data`;
                } else if (msg.includes('WARNING: Bob has no received_measurements data - using student implementation with empty data')) {
                    level = LogLevel.WARNING;
                    message = `⚠️ Warning: Bob has no received_measurements data - using student implementation with empty data`;
                } else if (msg.includes('WARNING: No data available for error estimation - using student implementation with empty data')) {
                    level = LogLevel.WARNING;
                    message = `⚠️ Warning: No data available for error estimation - using student implementation with empty data`;
                } else if (msg.includes('DEBUG: Alice sent_bits after b92_send_qubits:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Alice sent bits: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Alice qubits prepared:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Alice qubits prepared: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Bob received_measurements after processing:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Bob received measurements: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Bob measurement_outcomes:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Bob measurement outcomes: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Bob received_bases:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Bob received bases: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Sifting result - Alice:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Sifting result - Alice: ${msg.split('Alice: ')[1].split(', Bob:')[0]}, Bob: ${msg.split('Bob: ')[1]}`;
                } else if (msg.includes('DEBUG: Bob sifted_key:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Bob sifted key: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: their_bits_sample:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Their bits sample: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Using Alice\'s data from sifting message:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Using Alice's data from sifting message: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Using Alice\'s data from student implementation:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Using Alice's data from student implementation: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Using Alice\'s data from host.basis_choices:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Using Alice's data from host.basis_choices: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: host.basis_choices contains bases, not bits:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: host.basis_choices contains bases, not bits: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Set expected_bits to')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Set expected bits to: ${msg.split('to ')[1]}`;
                } else if (msg.includes('DEBUG: Processing qubit')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Processing qubit: ${msg.split('DEBUG: ')[1]}`;
                } else if (msg.includes('DEBUG: Alice prepared qubit')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Alice prepared qubit: ${msg.split('DEBUG: ')[1]}`;
                } else if (msg.includes('DEBUG: Bob measured qubit')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Bob measured qubit: ${msg.split('DEBUG: ')[1]}`;
                } else if (msg.includes('DEBUG: Sending Alice\'s bits to Bob for sifting:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Sending Alice's bits to Bob for sifting: ${msg.split(': ')[1]}`;
                } else if (msg.includes('DEBUG: Received Alice\'s bits for sifting:')) {
                    level = LogLevel.DEBUG;
                    message = `🐛 Debug: Received Alice's bits for sifting: ${msg.split(': ')[1]}`;
                } else if (msg.includes('B92 QKD protocol completed successfully using student')) {
                    level = LogLevel.STORY;
                    const errorRate = eventDetails?.error_rate || 0;
                    const sharedBases = eventDetails?.shared_bases || 0;
                    message = `🔬 B92 QKD protocol completed successfully using student's code! (${(errorRate * 100).toFixed(1)}% error rate) (${sharedBases} sifted bits)`;
                } else if (msg.includes('B92 PROTOCOL COMPLETE using student')) {
                    level = LogLevel.PROTOCOL;
                    const errorRate = eventDetails?.error_rate || 0;
                    const sharedBases = eventDetails?.shared_bases || 0;
                    message = `🔬 Student B92 Implementation Complete! All methods executed successfully: b92_send_qubits(), b92_process_received_qbit(), b92_sifting(), b92_estimate_error_rate() (${(errorRate * 100).toFixed(1)}% error rate) (${sharedBases} sifted bits)`;
                } else if (msg.includes('B92 Protocol Complete! All student methods executed successfully')) {
                    level = LogLevel.PROTOCOL;
                    message = `🔬 B92 Protocol Complete! All student methods executed successfully [b92_complete]`;
                }
            }

            switch (eventType) {
                case 'transmission_started':
                    level = LogLevel.NETWORK; // Low-level network detail
                    message = `Transmission started.`;
                    if (eventDetails) {
                        message += ` (delay: ${eventDetails.delay?.toFixed(3)}s, bandwidth: ${eventDetails.bandwidth})`;
                    }
                    break;

                case 'data_sent':
                    level = LogLevel.STORY; // Standard protocol step
                    message = `Sent data.`;
                    if (eventDetails?.destination?.name && eventDetails.data !== undefined) {
                        message = `Sent data to ${eventDetails.destination.name}: "${sliceData(eventDetails.data)}".`;
                    } else if (eventDetails?.message) {
                        // Handle student B92 qubit transmission logs
                        message = eventDetails.message;
                    }
                    break;

                case 'data_received':
                    level = LogLevel.STORY; // Standard protocol step
                    message = `Received data.`;
                    if (eventDetails?.source?.name && eventDetails.data !== undefined) {
                        message = `Received data from ${eventDetails.source.name}: "${sliceData(eventDetails.data)}".`;
                    } else if (eventDetails?.message) {
                        // Handle student B92 qubit reception logs
                        message = eventDetails.message;
                    }
                    break;

                case 'qkd_started':
                    level = LogLevel.PROTOCOL; // High-level protocol event
                    message = `QKD protocol started.`;
                    if (eventDetails?.protocol) {
                        message = `${eventDetails.protocol.toUpperCase()} QKD protocol started.`;
                    }
                    break;

                case 'qkd_completed':
                    level = LogLevel.PROTOCOL; // High-level protocol event
                    message = `QKD protocol completed.`;
                    if (eventDetails?.key_length) {
                        message = `QKD protocol completed. Shared key length: ${eventDetails.key_length} bits.`;
                    }
                    break;

                case 'quantum_state_prepared':
                    level = LogLevel.PROTOCOL; // Quantum operation
                    message = `Quantum state prepared.`;
                    if (eventDetails?.basis && eventDetails?.bit !== undefined) {
                        message = `Prepared qubit: bit=${eventDetails.bit}, basis=${eventDetails.basis}.`;
                    }
                    break;

                case 'quantum_state_measured':
                    level = LogLevel.PROTOCOL; // Quantum operation
                    message = `Quantum state measured.`;
                    if (eventDetails?.basis && eventDetails?.outcome !== undefined) {
                        message = `Measured qubit: outcome=${eventDetails.outcome}, basis=${eventDetails.basis}.`;
                    }
                    break;

                case 'basis_reconciliation':
                    level = LogLevel.PROTOCOL; // Protocol step
                    message = `Basis reconciliation performed.`;
                    if (eventDetails?.matching_bases !== undefined) {
                        message = `Basis reconciliation: ${eventDetails.matching_bases} matching bases found.`;
                    }
                    break;

                case 'error_rate_estimation':
                    level = LogLevel.PROTOCOL; // Protocol step
                    message = `Error rate estimation performed.`;
                    if (eventDetails?.error_rate !== undefined) {
                        message = `Error rate estimation: ${(eventDetails.error_rate * 100).toFixed(2)}% error rate.`;
                    }
                    break;

                case 'key_extraction':
                    level = LogLevel.PROTOCOL; // Protocol step
                    message = `Shared key extracted.`;
                    if (eventDetails?.key_length) {
                        message = `Shared key extracted: ${eventDetails.key_length} bits.`;
                    }
                    break;

                case 'eavesdropping_detected':
                    level = LogLevel.WARN; // Security warning
                    message = `Eavesdropping detected!`;
                    if (eventDetails?.error_rate !== undefined) {
                        message = `Eavesdropping detected! Error rate: ${(eventDetails.error_rate * 100).toFixed(2)}%.`;
                    }
                    break;

                case 'quantum_channel_established':
                    level = LogLevel.NETWORK; // Network event
                    message = `Quantum channel established.`;
                    if (eventDetails?.channel_id) {
                        message = `Quantum channel ${eventDetails.channel_id} established.`;
                    }
                    break;

                case 'quantum_channel_lost':
                    level = LogLevel.WARN; // Network warning
                    message = `Quantum channel lost.`;
                    if (eventDetails?.channel_id) {
                        message = `Quantum channel ${eventDetails.channel_id} lost.`;
                    }
                    break;

                case 'entanglement_established':
                    level = LogLevel.PROTOCOL; // Quantum entanglement
                    message = `Quantum entanglement established.`;
                    if (eventDetails?.partner) {
                        message = `Quantum entanglement established with ${eventDetails.partner}.`;
                    }
                    break;

                case 'entanglement_lost':
                    level = LogLevel.WARN; // Entanglement warning
                    message = `Quantum entanglement lost.`;
                    if (eventDetails?.partner) {
                        message = `Quantum entanglement with ${eventDetails.partner} lost.`;
                    }
                    break;

                case 'repeater_operation':
                    level = LogLevel.NETWORK; // Repeater operation
                    message = `Quantum repeater operation.`;
                    if (eventDetails?.operation) {
                        message = `Quantum repeater: ${eventDetails.operation}.`;
                    }
                    break;

                case 'protocol_error':
                    level = LogLevel.ERROR; // Protocol error
                    message = `Protocol error occurred.`;
                    if (eventDetails?.error_message) {
                        message = `Protocol error: ${eventDetails.error_message}.`;
                    }
                    break;

                case 'security_breach':
                    level = LogLevel.ERROR; // Security error
                    message = `Security breach detected!`;
                    if (eventDetails?.breach_type) {
                        message = `Security breach: ${eventDetails.breach_type}.`;
                    }
                    break;

                // B92 specific events
                case 'b92_qubit_preparation':
                    level = LogLevel.PROTOCOL;
                    message = `B92 qubit prepared.`;
                    if (eventDetails?.bit !== undefined) {
                        message = `B92 qubit prepared: bit=${eventDetails.bit}.`;
                    }
                    break;

                case 'b92_qubit_measurement':
                    level = LogLevel.PROTOCOL;
                    message = `B92 qubit measured.`;
                    if (eventDetails?.outcome !== undefined && eventDetails?.basis) {
                        message = `B92 qubit measured: outcome=${eventDetails.outcome}, basis=${eventDetails.basis}.`;
                    }
                    break;

                case 'b92_sifting':
                    level = LogLevel.PROTOCOL;
                    message = `B92 sifting performed.`;
                    if (eventDetails?.sifted_bits !== undefined) {
                        message = `B92 sifting: ${eventDetails.sifted_bits} bits sifted.`;
                    }
                    break;

                case 'b92_error_estimation':
                    level = LogLevel.PROTOCOL;
                    message = `B92 error rate estimated.`;
                    if (eventDetails?.error_rate !== undefined) {
                        message = `B92 error rate: ${(eventDetails.error_rate * 100).toFixed(2)}%.`;
                    }
                    break;

                case 'b92_key_generation':
                    level = LogLevel.PROTOCOL;
                    message = `B92 key generated.`;
                    if (eventDetails?.key_length) {
                        message = `B92 key generated: ${eventDetails.key_length} bits.`;
                    }
                    break;

                default:
                    // message = `${source}: Unhandled simulation event type "${eventType}".`;
                    // level = LogLevel.WARN; // Unhandled type is a warning
                    // console.warn(`Unhandled simulation event type: ${eventType}`, eventData);
                    return null; // Don't show unhandled events to reduce noise
            }

        } else {
            // Handle other event formats (e.g., direct messages)
            if (typeof eventData === 'string') {
                message = eventData;
                level = LogLevel.STORY;
            } else if (eventData.message) {
                message = eventData.message;
                level = eventData.level || LogLevel.STORY;
                source = eventData.source || source;
            } else {
                // Fallback for unknown formats
                message = `Received data in unhandled format.`;
                level = LogLevel.WARN;
            }
        }

    } catch (error) {
        console.error('Error converting event to log:', error, eventData);
        message = `Error processing event: ${error.message}`;
        level = LogLevel.ERROR;
    }

    return {
        level,
        source,
        message,
        timestamp: new Date().toISOString(),
        raw: eventData
    };
}

/**
 * Slice data for display (truncate long strings)
 */
function sliceData(data: any, maxLength: number = 50): string {
    if (typeof data === 'string') {
        return data.length > maxLength ? data.substring(0, maxLength) + '...' : data;
    }
    return String(data);
}