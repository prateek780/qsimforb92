/**
 * B92 Log Parser
 * ==============
 * 
 * Handles B92-specific log events and converts them to human-readable format.
 * Extends the main log parser with B92 protocol-specific event handling.
 */

import { LogI, LogLevel } from './simulation-logs'

function formatTime(date: Date): string {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
}

/**
 * Converts B92-specific websocket events into human-readable LogI objects.
 * @param eventData The raw event object received from the websocket.
 * @returns A LogI object representing the formatted B92 log message.
 */
export function convertB92EventToLog(eventData: any): LogI {
    const time = formatTime(new Date());
    let level: LogLevel = LogLevel.PROTOCOL;
    let source = 'B92 Simulation';
    let message = 'Received B92 data in unhandled format.';

    try {
        // Check if it's a B92 simulation_event structure
        if (typeof eventData === 'object' && eventData !== null) {
            // Try different event structures
            const eventType = eventData.event_type || eventData.type || '';
            const node = eventData.node || eventData.source || 'B92 Simulation';
            const eventDetails = eventData.data || eventData;
            
            source = node;

            // Handle standard event types with B92 data
            if (eventDetails.protocol === 'B92' || eventDetails.message?.includes('B92') || eventDetails.message?.includes('b92') || eventType.includes('b92') || eventType.includes('B92')) {
                switch (eventType) {
                    case 'info':
                        level = LogLevel.PROTOCOL;
                        // Parse B92-specific info messages
                        if (eventDetails.message?.includes('STUDENT B92: Starting with')) {
                            const numQubits = eventDetails.num_qubits || 0;
                            message = `Student B92 implementation: Starting protocol with ${numQubits} qubits`;
                        } else if (eventDetails.message?.includes('STUDENT B92: Sent')) {
                            const qubitsSent = eventDetails.qubits_sent || 0;
                            message = `Student B92: Sending ${qubitsSent} encoded qubits from Alice's b92_send_qubits() through quantum channel (${qubitsSent} qubits) - Sample: [|0>, |+>, |0>...]`;
                        } else if (eventDetails.message?.includes('STUDENT Bob: Received qubit')) {
                            const qubitsReceived = eventDetails.qubits_received || 0;
                            const totalExpected = eventDetails.total_expected || 0;
                            message = `Student Bob: Received B92 qubit ${qubitsReceived}/${totalExpected} [b92_process_received_qbit]`;
                        } else if (eventDetails.message?.includes('STUDENT Bob: Error rate')) {
                            const errorRate = eventDetails.error_rate || 0;
                            message = `Student Bob b92_estimate_error_rate(): ${(errorRate * 100).toFixed(1)}% error rate using student implementation [b92_estimate_error_rate] (${(errorRate * 100).toFixed(1)}% error rate)`;
                        } else {
                            message = eventDetails.message || 'B92 Protocol Information';
                        }
                        break;
                    case 'data_sent':
                        level = LogLevel.STORY;
                        const dataSentQubits = eventDetails.qubits_sent || 0;
                        message = `All ${dataSentQubits} qubits sent successfully through quantum channel (${dataSentQubits} qubits)`;
                        break;
                    case 'data_received':
                        level = LogLevel.PROTOCOL;
                        const dataReceivedQubits = eventDetails.qubits_received || 0;
                        const dataTotalExpected = eventDetails.total_expected || 0;
                        if (dataReceivedQubits >= dataTotalExpected) {
                            message = `Student Bob: Received all ${dataTotalExpected} qubits, ready for b92_reconcile_bases() [b92_reconcile_bases]`;
                        } else {
                            message = `B92 Progress: ${dataReceivedQubits}/${dataTotalExpected} qubits sent`;
                        }
                        break;
                    case 'shared_key_generated':
                        level = LogLevel.STORY;
                        const sharedErrorRate = eventDetails.error_rate || 0;
                        const sharedSiftedKeyLength = eventDetails.sifted_key_length || 0;
                        message = `B92 QKD protocol completed successfully (${(sharedErrorRate * 100).toFixed(1)}% error rate) (${sharedSiftedKeyLength} shared bases)`;
                        break;
                    default:
                        // Use the message from the event data
                        message = eventDetails.message || `B92 ${eventType.replace('_', ' ').toUpperCase()}`;
                        level = LogLevel.PROTOCOL;
                        break;
                }
            } else if (eventDetails.packet && (
                eventDetails.packet.data?.includes('B92') ||
                eventDetails.packet.data?.includes('b92') ||
                JSON.stringify(eventDetails.packet).includes('B92') ||
                JSON.stringify(eventDetails.packet).includes('b92')
            )) {
                // Handle packet-based B92 events
                switch (eventType) {
                    case 'packet_received':
                        level = LogLevel.PROTOCOL;
                        message = `Classical Network: Received B92 packet from ${eventDetails.packet.from || 'unknown'}`;
                        break;
                    case 'packet_transmitted':
                        level = LogLevel.NETWORK;
                        message = `Classical Network: Transmitted B92 packet to ${eventDetails.packet.to || 'unknown'}`;
                        break;
                    case 'packet_routed':
                        level = LogLevel.NETWORK;
                        message = `Classical Router: Routed B92 packet through network`;
                        break;
                    default:
                        level = LogLevel.PROTOCOL;
                        message = `Classical Network: B92 packet ${eventType.replace('_', ' ')}`;
                        break;
                }
            } else {
                // Handle specific B92 event types
                switch (eventType) {
                // B92 Student Implementation Events
                case 'student_b92_send_start':
                    level = LogLevel.PROTOCOL;
                    const sendQubits = eventDetails.num_qubits || 0;
                    message = `Student Alice: Prepared ${sendQubits} qubits using b92_send_qubits() [b92_send_qubits] (${sendQubits} qubits)`;
                    break;
                    
                case 'student_b92_send_complete':
                    level = LogLevel.STORY;
                    const preparedQubits = eventDetails.prepared_qubits || 0;
                    message = `Student B92: Sending ${preparedQubits} encoded qubits from Alice's b92_send_qubits() through quantum channel (${preparedQubits} qubits) - Sample: [|0>, |+>, |0>...]`;
                    break;
                    
                case 'student_b92_measure_start':
                    level = LogLevel.PROTOCOL;
                    message = `Student Bob: Starting B92 qubit measurement [b92_process_received_qbit]`;
                    break;
                    
                case 'student_b92_measure_complete':
                    level = LogLevel.PROTOCOL;
                    const measuredBits = eventDetails.measured_bits || 0;
                    const measureTotalExpected = eventDetails.total_expected || 0;
                    if (measuredBits >= measureTotalExpected) {
                        message = `Student Bob: Received all ${measureTotalExpected} qubits, ready for b92_reconcile_bases() [b92_reconcile_bases]`;
                    } else {
                        message = `B92 Progress: ${measuredBits}/${measureTotalExpected} qubits sent`;
                    }
                    break;
                    
                case 'student_b92_reconcile_start':
                    level = LogLevel.PROTOCOL;
                    message = `Student Bob: Starting reconciliation process with Alice's bases [b92_reconcile_bases]`;
                    break;
                    
                case 'student_b92_reconcile_complete':
                    level = LogLevel.PROTOCOL;
                    const reconciledBits = eventDetails.reconciled_bits || 0;
                    const reconciliationEfficiency = eventDetails.efficiency || 0;
                    message = `Student Bob b92_reconcile_bases(): Found ${reconciledBits} matching bases (Efficiency: ${(reconciliationEfficiency * 100).toFixed(1)}%) [b92_reconcile_bases] (${reconciledBits} shared bases) (${(reconciliationEfficiency * 100).toFixed(1)}% efficiency)`;
                    break;
                    
                case 'student_b92_error_start':
                    level = LogLevel.PROTOCOL;
                    message = `Student Bob: Starting error rate estimation process [b92_estimate_error_rate]`;
                    break;
                    
                case 'student_b92_error_complete':
                    level = LogLevel.PROTOCOL;
                    const estimatedErrorRate = eventDetails.estimated_error_rate || 0;
                    const errorSampleSize = eventDetails.error_sample_size || 0;
                    message = `Student Bob b92_estimate_error_rate(): ${(estimatedErrorRate * 100).toFixed(1)}% error rate (${errorSampleSize} samples) using student implementation [b92_estimate_error_rate] (${(estimatedErrorRate * 100).toFixed(1)}% error rate)`;
                    break;
                    
                case 'student_b92_ready':
                    level = LogLevel.PROTOCOL;
                    const receivedQubits = eventDetails.received_qubits || 0;
                    message = `Student Bob: Received all ${receivedQubits} B92 qubits, ready for reconciliation [b92_reconcile_bases]`;
                    break;
                    
                case 'student_b92_trigger':
                    level = LogLevel.PROTOCOL;
                    message = `Student Alice: Triggering B92 reconciliation - sending bases to Bob [send_bases_for_reconcile]`;
                    break;
                    
                case 'student_b92_complete':
                    level = LogLevel.PROTOCOL;
                    const finalErrorRate = eventDetails.final_error_rate || 0;
                    const finalKeyLength = eventDetails.final_key_length || 0;
                    message = `Student B92 Implementation Complete! All methods executed successfully: b92_send_qubits(), b92_process_received_qbit(), b92_reconcile_bases(), b92_estimate_error_rate() (${(finalErrorRate * 100).toFixed(1)}% error rate)`;
                    break;
                    
                case 'b92_protocol_complete':
                    level = LogLevel.PROTOCOL;
                    const protocolErrorRate = eventDetails.final_error_rate || 0;
                    const protocolKeyLength = eventDetails.final_key_length || 0;
                    message = `B92 Protocol Complete! All student methods executed successfully [b92_complete]`;
                    break;
                    
                // B92 Protocol Events
                case 'b92_protocol_start':
                    level = LogLevel.STORY;
                    message = `🔬 B92 Quantum Key Distribution Protocol Started`;
                    break;

                case 'b92_qubit_preparation':
                    level = LogLevel.PROTOCOL;
                    const prepQubits = eventDetails?.num_qubits || 0;
                    message = `Student Alice: Preparing ${prepQubits} qubits using B92 encoding [b92_send_qubits]`;
                    break;

                case 'b92_qubit_transmission':
                    level = LogLevel.NETWORK;
                    const transmittedQubits = eventDetails?.transmitted_qubits || 0;
                    message = `Alice → Bob: Transmitting ${transmittedQubits} B92-encoded qubits through quantum channel`;
                    break;

                case 'b92_qubit_measurement':
                    level = LogLevel.PROTOCOL;
                    const measuredQubits = eventDetails?.measured_qubits || 0;
                    message = `Student Bob: Measuring received qubit using random basis [b92_process_received_qbit] (${measuredQubits} qubits processed)`;
                    break;

                case 'b92_sifting_start':
                    level = LogLevel.PROTOCOL;
                    message = `Student Bob: Starting B92 sifting process [b92_sifting]`;
                    break;

                case 'b92_sifting_complete':
                    level = LogLevel.PROTOCOL;
                    const siftingBits = eventDetails?.sifted_bits || 0;
                    const totalBits = eventDetails?.total_bits || 0;
                    const siftingEfficiency = totalBits > 0 ? (siftingBits / totalBits * 100).toFixed(1) : '0.0';
                    message = `Student Bob: B92 sifting completed - ${siftingBits}/${totalBits} bits kept (${siftingEfficiency}% efficiency)`;
                    break;

                case 'b92_error_estimation':
                    level = LogLevel.PROTOCOL;
                    const estimationErrorRate = eventDetails?.error_rate || 0;
                    const sampleSize = eventDetails?.sample_size || 0;
                    message = `Student Bob: Error rate estimation [b92_estimate_error_rate] - ${(estimationErrorRate * 100).toFixed(2)}% error rate (${sampleSize} samples)`;
                    break;

                case 'b92_protocol_complete':
                    level = LogLevel.STORY;
                    const completeKeyLength = eventDetails?.final_key_length || 0;
                    const completeErrorRate = eventDetails?.final_error_rate || 0;
                    message = `✅ B92 Protocol Completed Successfully! Final key: ${completeKeyLength} bits, Error rate: ${(completeErrorRate * 100).toFixed(2)}%`;
                    break;

                // B92 Student Implementation Events
                case 'student_b92_send_start':
                    level = LogLevel.PROTOCOL;
                    message = `Student Alice: Starting B92 qubit preparation [b92_send_qubits]`;
                    break;

                case 'student_b92_send_complete':
                    level = LogLevel.PROTOCOL;
                    const sendCompleteQubits = eventDetails?.prepared_qubits || 0;
                    message = `Student Alice: B92 qubit preparation completed - ${sendCompleteQubits} qubits prepared [b92_send_qubits]`;
                    break;

                case 'student_b92_measure_start':
                    level = LogLevel.PROTOCOL;
                    message = `Student Bob: Starting B92 qubit measurement [b92_process_received_qbit]`;
                    break;

                case 'student_b92_measure_complete':
                    level = LogLevel.PROTOCOL;
                    const measurementBits = eventDetails?.measured_bits || 0;
                    message = `Student Bob: B92 measurement completed - ${measurementBits} qubits measured [b92_process_received_qbit]`;
                    break;

                case 'student_b92_reconcile_start':
                    level = LogLevel.PROTOCOL;
                    message = `Student Bob: Starting B92 reconciliation process [b92_reconcile_bases]`;
                    break;

                case 'student_b92_reconcile_complete':
                    level = LogLevel.PROTOCOL;
                    const reconcileBits = eventDetails?.reconciled_bits || 0;
                    const reconcileEfficiency = eventDetails?.efficiency || 0;
                    message = `Student Bob: B92 reconciliation completed - ${reconcileBits} bits reconciled (${(reconcileEfficiency * 100).toFixed(1)}% efficiency)`;
                    break;

                case 'student_b92_error_start':
                    level = LogLevel.PROTOCOL;
                    message = `Student Bob: Starting B92 error rate estimation [b92_estimate_error_rate]`;
                    break;

                case 'student_b92_error_complete':
                    level = LogLevel.PROTOCOL;
                    const errorEstimationRate = eventDetails?.estimated_error_rate || 0;
                    const errorCompleteSampleSize = eventDetails?.error_sample_size || 0;
                    message = `Student Bob: B92 error estimation completed - ${(errorEstimationRate * 100).toFixed(2)}% error rate (${errorCompleteSampleSize} samples)`;
                    break;

                case 'student_b92_ready':
                    level = LogLevel.PROTOCOL;
                    const readyQubits = eventDetails?.received_qubits || 0;
                    message = `Student Bob: Received all ${readyQubits} B92 qubits, ready for reconciliation [b92_reconcile_bases]`;
                    break;

                case 'student_b92_trigger':
                    level = LogLevel.PROTOCOL;
                    message = `Student Alice: Triggering B92 reconciliation - sending bases to Bob [send_bases_for_reconcile]`;
                    break;

                // B92 Error Events
                case 'b92_error_qubit_loss':
                    level = LogLevel.WARN;
                    const lostQubits = eventDetails?.lost_qubits || 0;
                    message = `⚠️ B92 Warning: ${lostQubits} qubits lost during transmission`;
                    break;

                case 'b92_error_high_error_rate':
                    level = LogLevel.WARN;
                    const highErrorRate = eventDetails?.error_rate || 0;
                    message = `⚠️ B92 Warning: High error rate detected (${(highErrorRate * 100).toFixed(2)}%) - possible eavesdropping`;
                    break;

                case 'b92_error_insufficient_key':
                    level = LogLevel.WARN;
                    const keyLength = eventDetails?.key_length || 0;
                    message = `⚠️ B92 Warning: Insufficient key length (${keyLength} bits) after sifting`;
                    break;

                // B92 Success Events
                case 'b92_success_secure_key':
                    level = LogLevel.STORY;
                    const secureKeyLength = eventDetails?.key_length || 0;
                    message = `🔐 B92 Success: Secure quantum key established (${secureKeyLength} bits)`;
                    break;

                case 'b92_success_low_error_rate':
                    level = LogLevel.STORY;
                    const lowErrorRate = eventDetails?.error_rate || 0;
                    message = `✅ B92 Success: Low error rate (${(lowErrorRate * 100).toFixed(2)}%) - channel appears secure`;
                    break;

                default:
                    // Check if it's a generic BB84 event that we should handle
                    if (eventType.startsWith('student_bb84_')) {
                        // Convert BB84 events to B92 context
                        const b92EventType = eventType.replace('student_bb84_', 'student_b92_');
                        return convertB92EventToLog({
                            ...eventData,
                            event_type: b92EventType
                        });
                    }
                    break;
                }
            }

        } else if (typeof eventData === 'object' && eventData !== null && (eventData.summary_text !== undefined || eventData.error_message !== undefined)) {
            // Handle simulation summaries
            source = 'B92 Simulation Summary';
            if (eventData.error_message) {
                level = LogLevel.ERROR;
                message = `B92 ERROR: ${eventData.error_message}`;
            } else if (Array.isArray(eventData.summary_text) && eventData.summary_text.length > 0) {
                level = LogLevel.STORY;
                message = eventData.summary_text.join('\n');
            } else {
                level = LogLevel.WARN;
                message = 'Received empty B92 simulation summary.';
            }

        } else {
            // Try to handle as a generic B92 event
            if (eventType && eventType.startsWith('student_b92_')) {
                // Handle student B92 events
                switch (eventType) {
                    case 'student_b92_send_start':
                        level = LogLevel.PROTOCOL;
                        message = `Student Alice: Starting B92 qubit preparation [b92_send_qubits]`;
                        break;
                    case 'student_b92_send_complete':
                        level = LogLevel.STORY;
                        message = `Student B92: Sending encoded qubits from Alice's b92_send_qubits() through quantum channel`;
                        break;
                    case 'student_b92_measure_start':
                        level = LogLevel.PROTOCOL;
                        message = `Student Bob: Starting B92 qubit measurement [b92_process_received_qbit]`;
                        break;
                    case 'student_b92_measure_complete':
                        level = LogLevel.PROTOCOL;
                        message = `Student Bob: B92 qubit measurement completed [b92_process_received_qbit]`;
                        break;
                    case 'student_b92_reconcile_start':
                        level = LogLevel.PROTOCOL;
                        message = `Student Bob: Starting B92 reconciliation process [b92_reconcile_bases]`;
                        break;
                    case 'student_b92_reconcile_complete':
                        level = LogLevel.PROTOCOL;
                        message = `Student Bob: B92 reconciliation completed [b92_reconcile_bases]`;
                        break;
                    case 'student_b92_error_start':
                        level = LogLevel.PROTOCOL;
                        message = `Student Bob: Starting B92 error rate estimation [b92_estimate_error_rate]`;
                        break;
                    case 'student_b92_error_complete':
                        level = LogLevel.PROTOCOL;
                        message = `Student Bob: B92 error estimation completed [b92_estimate_error_rate]`;
                        break;
                    case 'student_b92_ready':
                        level = LogLevel.PROTOCOL;
                        message = `Student Bob: Received all B92 qubits, ready for reconciliation [b92_reconcile_bases]`;
                        break;
                    case 'student_b92_trigger':
                        level = LogLevel.PROTOCOL;
                        message = `Student Alice: Triggering B92 reconciliation - sending bases to Bob [send_bases_for_reconcile]`;
                        break;
                    case 'student_b92_complete':
                        level = LogLevel.PROTOCOL;
                        message = `Student B92 Implementation Complete! All methods executed successfully`;
                        break;
                    default:
                        level = LogLevel.PROTOCOL;
                        message = `B92 Event: ${eventType}`;
                        break;
                }
            } else {
                // Unhandled format
                level = LogLevel.WARN;
                source = 'B92 Simulation System';
                message = 'Received B92 data in unhandled format.';
            }
        }

    } catch (error: any) {
        message = `Error processing B92 event data: ${error.message}`;
        level = LogLevel.ERROR;
        source = 'B92 System';
        console.error('Error processing B92 event data:', eventData, error);
    }

    return { level, time, source, message };
}

/**
 * Enhanced log parser that handles both BB84 and B92 events
 */
export function convertEventToLogWithB92(eventData: any): LogI {
    // Debug: Log the event structure to see what we're receiving
    console.log('B92 Parser received event:', eventData);
    
    // First try B92-specific parsing
    if (eventData && typeof eventData === 'object') {
        const eventType = eventData.event_type || eventData.type || '';
        const eventDetails = eventData.data || eventData;
        
        // Check if this is a B92 event by looking at the data
        const isB92Event = eventDetails.protocol === 'B92' || 
                          eventDetails.message?.includes('B92') ||
                          eventDetails.message?.includes('b92') ||
                          eventType.includes('b92') || 
                          eventType.includes('B92') ||
                          // Check packet data for B92 content
                          (eventDetails.packet && (
                              eventDetails.packet.data?.includes('B92') ||
                              eventDetails.packet.data?.includes('b92') ||
                              JSON.stringify(eventDetails.packet).includes('B92') ||
                              JSON.stringify(eventDetails.packet).includes('b92')
                          )) ||
                          // Check if event type starts with student_b92
                          eventType.startsWith('student_b92_') ||
                          // Check if message contains B92
                          eventData.message?.includes('B92') ||
                          eventData.message?.includes('b92');
        
        if (isB92Event) {
            return convertB92EventToLog(eventData);
        }
        
        // If it's a student implementation event, check if we're in B92 mode
        if (eventType.startsWith('student_') && eventType.includes('b92')) {
            return convertB92EventToLog(eventData);
        }
    }
    
    // Fall back to regular BB84 parsing
    try {
        // Import the original log parser
        const { convertEventToLog } = require('./log-parser');
        return convertEventToLog(eventData);
    } catch (error) {
        // If original parser not available, use B92 parser as fallback
        return convertB92EventToLog(eventData);
    }
}
