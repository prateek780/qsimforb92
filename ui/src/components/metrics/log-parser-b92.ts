import { LogI, LogLevel } from "./simulation-logs";

/**
 * Formats a Date object into HH:MM:SS string format.
 * @param date The Date object to format.
 * @returns The formatted time string.
 */
function formatTime(date: Date): string {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
}

/**
 * Converts a raw websocket event object into a human-readable LogI object for B92 protocol.
 * @param eventData The raw event object received from the websocket.
 * @returns A LogI object representing the formatted log message.
 */
export function convertB92EventToLog(eventData: any): LogI {
    const time = formatTime(new Date());
    let level: LogLevel = LogLevel.PROTOCOL; // Default to a standard protocol-level log
    let source = 'B92 Simulation'; // Default source if node is not available
    let message = 'Received B92 data in unhandled format.';

    try {
        // Check if it's a simulation_event structure (has event_type and node)
        if (typeof eventData === 'object' && eventData !== null && eventData.event_type !== undefined && eventData.node !== undefined) {

            source = eventData.node || source;
            const eventType = eventData.event_type;
            const eventDetails = eventData.data; // Specific details for this event type

            switch (eventType) {
                case 'transmission_started':
                    level = LogLevel.NETWORK; // Low-level network detail
                    message = `B92 Transmission started.`;
                    if (eventDetails) {
                        message += ` (delay: ${eventDetails.delay?.toFixed(3)}s, bandwidth: ${eventDetails.bandwidth})`;
                    }
                    break;

                case 'data_sent':
                    level = LogLevel.STORY; // Standard protocol step
                    message = `B92 Data sent.`;
                    if (eventDetails?.destination?.name && eventDetails.data !== undefined) {
                        message = `Sent B92 data to ${eventDetails.destination.name}: "${sliceData(eventDetails.data)}".`;
                    } else if (eventDetails?.message) {
                        // Handle student B92 qubit transmission logs
                        message = eventDetails.message;
                        if (eventDetails.qubits_sent) {
                            message += ` (${eventDetails.qubits_sent} qubits)`;
                        }
                        if (eventDetails.student_qubits) {
                            message += ` - Sample: [${eventDetails.student_qubits.slice(0, 3).join(', ')}...]`;
                        }
                    }
                    break;

                case 'packet_delivered':
                    level = LogLevel.NETWORK; // Low-level network detail
                    message = `B92 Packet delivered.`;
                    if (eventDetails?.destination !== undefined) {
                        message = `B92 Packet delivered to ${eventDetails.destination}.`;
                        if (eventDetails.packet_id) {
                            message += ` (ID: ${eventDetails.packet_id.substring(0, 6)}...)`;
                        }
                        if (eventDetails.delay !== undefined) {
                            message += ` (Delay: ${eventDetails.delay?.toFixed(3)}s)`;
                        }
                    }
                    break;

                case 'packet_received':
                    level = LogLevel.NETWORK; // Standard protocol step
                    message = `B92 Packet received.`;
                    if (eventDetails?.packet) {
                        const packet = eventDetails.packet;
                        // Extract simple type name from "<class 'module.Class'>" format
                        const packetTypeMatch = packet.type?.match(/<class\s*'[^']*\.([^']+)'\s*>/);
                        const packetType = packetTypeMatch ? packetTypeMatch[1] : 'Unknown Packet';
                        const packetFrom = packet.from || 'Unknown Sender';

                        message = `Received ${packetType} from ${packetFrom}.`;

                        // Specific handling for B92 QKD data strings (Python dict string)
                        if (packetType === 'QKDTransmissionPacket' && typeof packet.data === 'string') {
                            // Use regex to safely extract the 'type' field from the Python dict string
                            const qkdTypeMatch = packet.data.match(/'type'\s*:\s*'([^']+)'/);
                            if (qkdTypeMatch && qkdTypeMatch[1]) {
                                message += ` (B92 QKD Type: ${qkdTypeMatch[1]}).`;
                            }
                        } else if (packetType === 'ClassicDataPacket' && typeof packet.data === 'string' && !packet.data.startsWith('bytearray')) {
                            // Include classic data unless it's the bytearray representation
                            message += ` Data: "${sliceData(packet.data)}".`;
                        }
                    }
                    break;

                case 'packet_lost':
                    level = LogLevel.ERROR;
                    message = `B92 Packet lost.`;
                    break;

                case 'qkd_initiated':
                    level = LogLevel.STORY; // A major, high-level action
                    message = `Initiated B92 QKD.`;
                    if (eventDetails?.with_adapter?.name) {
                        message = `Initiated B92 QKD with ${eventDetails.with_adapter.name}.`;
                    } else if (eventDetails?.message) {
                        // Handle student B92 implementation logs
                        message = eventDetails.message;
                        if (eventDetails.protocol) {
                            message += ` (${eventDetails.protocol})`;
                        }
                        if (eventDetails.num_qubits) {
                            message += ` - ${eventDetails.num_qubits} qubits`;
                        }
                    }
                    break;

                case 'shared_key_generated':
                    level = LogLevel.STORY;
                    if (eventDetails?.message) {
                        // Handle student B92 completion logs
                        message = eventDetails.message;
                        if (eventDetails.error_rate !== undefined) {
                            message += ` (${(eventDetails.error_rate * 100).toFixed(1)}% error rate)`;
                        }
                        if (eventDetails.shared_bases !== undefined) {
                            message += ` (${eventDetails.shared_bases} sifted bits)`;
                        }
                    } else if (eventDetails?.key?.length) {
                        message = `${eventDetails.key.length} bit B92 shared key generated for encryption: ${sliceData(eventDetails.key)}`;
                    } else {
                        message = 'B92 Shared key generated.';
                    }
                    break;

                case 'data_encrypted':
                    level = LogLevel.STORY;
                    message = `B92 Data encrypted using ${eventDetails.algorithm} algorithm. Cipher: ${sliceData(eventDetails.cipher)}`;
                    break;

                case 'data_decrypted':
                    level = LogLevel.STORY;
                    message = `B92 Data decrypted using ${eventDetails.algorithm} algorithm. Cipher: ${sliceData(eventDetails.data)}`;
                    break;

                case 'data_received':
                    level = LogLevel.NETWORK;
                    message = `B92 Data received.`;
                    if (eventDetails) {
                        if (eventDetails.message?.type) {
                            message = `Received B92 message (Type: ${eventDetails.message.type})`;
                        } else if (eventDetails.data !== undefined && typeof eventDetails.data === 'string' && !eventDetails.data.startsWith('bytearray')) {
                            // Handle "Hello World!" case etc. (classic data)
                            message = `Received B92 data: "${sliceData(eventDetails.data)}".`;
                        } else if (eventDetails.packet) {
                            // Sometimes this event carries packet info too
                            const packet = eventDetails.packet;
                            const packetTypeMatch = packet.type?.match(/<class\s*'[^']*\.([^']+)'\s*>/);
                            const packetType = packetTypeMatch ? packetTypeMatch[1] : 'Unknown Packet';
                            const packetFrom = packet.from || 'Unknown Sender';
                            message = `Received B92 packet data (${packetType} from ${packetFrom})`;
                        } else if (eventDetails.message && eventDetails.student_method) {
                            // Handle student B92 qubit reception logs
                            message = eventDetails.message;
                            if (eventDetails.student_method) {
                                message += ` (${eventDetails.student_method})`;
                            }
                        }
                    }
                    break;

                case 'classical_data_received':
                    level = LogLevel.STORY;
                    message = `B92 Data received at destination: "${sliceData(eventDetails.data)}"`;
                    break;

                case 'qubit_lost':
                    level = LogLevel.ERROR;
                    message = `B92 Qubit lost during transmission.`;
                    break;

                case 'info':
                    const infoType = eventData.type ?? 'info';

                    switch (infoType) {
                        case 'packet_fragmented':
                            level = LogLevel.NETWORK;
                            message = eventDetails.message || 'B92 Packet fragmented because of mtu limit.'
                            break
                        case 'fragment_received':
                            level = LogLevel.NETWORK;
                            message = eventDetails.message || `B92 Fragment received.`
                            break
                        case 'fragment_reassembled':
                            level = LogLevel.NETWORK;
                            message = eventDetails.message || 'B92 Fragment reassembled.'
                            break
                        default:
                            // Handle student B92 implementation logs
                            if (eventDetails?.message) {
                                level = LogLevel.PROTOCOL; // Student implementation details
                                message = eventDetails.message;
                                
                                // Add additional context for student B92 logs
                                if (eventDetails.student_method) {
                                    message += ` [${eventDetails.student_method}]`;
                                }
                                if (eventDetails.qubits_prepared) {
                                    message += ` (${eventDetails.qubits_prepared} qubits)`;
                                }
                                if (eventDetails.shared_bases !== undefined) {
                                    message += ` (${eventDetails.shared_bases} sifted bits)`;
                                }
                                if (eventDetails.efficiency !== undefined) {
                                    message += ` (${eventDetails.efficiency.toFixed(1)}% efficiency)`;
                                }
                                if (eventDetails.error_rate !== undefined) {
                                    message += ` (${(eventDetails.error_rate * 100).toFixed(1)}% error rate)`;
                                }
                                if (eventDetails.errors !== undefined && eventDetails.comparisons !== undefined) {
                                    message += ` (${eventDetails.errors}/${eventDetails.comparisons} errors)`;
                                }
                            } else {
                                level = LogLevel.PROTOCOL;
                                message = 'B92 Information event.';
                            }
                            break
                    }

                    break

                default:
                    // message = `${source}: Unhandled B92 simulation event type "${eventType}".`;
                    // level = LogLevel.WARN; // Unhandled type is a warning
                    // console.warn(`Unhandled B92 simulation event type: ${eventType}`, eventData);
                    break;
            }

        } else if (typeof eventData === 'object' && eventData !== null && (eventData.summary_text !== undefined || eventData.error_message !== undefined)) {
            // Check if it's a simulation_summary structure
            source = 'B92 Simulation Summary'; // Summary events are not node-specific
            if (eventData.error_message) {
                level = LogLevel.ERROR;
                message = `B92 ERROR: ${eventData.error_message}`;
            } else if (Array.isArray(eventData.summary_text) && eventData.summary_text.length > 0) {
                level = LogLevel.STORY; // Summaries are high-level narratives
                message = eventData.summary_text.join('\n'); // Join summary lines
            } else {
                level = LogLevel.WARN; // An empty summary is unexpected
                message = 'Received empty B92 simulation summary.';
            }

        } else {
            // If it doesn't match expected simulation event or summary structure
            level = LogLevel.WARN;
            source = 'B92 Simulation System';
            message = 'Received B92 data in unhandled format.';
            console.warn('Received B92 data in unhandled format:', eventData);
        }

    } catch (error: any) {
        // Catch any errors during processing to prevent the function from crashing
        message = `Error processing B92 event data: ${error.message}`;
        level = LogLevel.ERROR;
        source = 'B92 System';
        console.error('Error processing B92 event data:', eventData, error);
    }

    return { level, time, source, message };
}

function sliceData(data: string): string {
    if (typeof data !== 'string') { return data }
    return data.slice(0, 10) + (data.length > 10 ? '...' : '');
}

/**
 * Enhanced log parser that handles both BB84 and B92 events
 */
export function convertEventToLogWithB92(eventData: any): LogI {
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