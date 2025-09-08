/**
 * B92 WebSocket Service
 * ====================
 * 
 * Handles B92-specific WebSocket connections and events.
 * Separate from the main socket service to avoid conflicts with BB84.
 */

export interface B92Event {
  type: string;
  event_type: string;
  node: string;
  timestamp: number;
  data: any;
  log_level: string;
  protocol: string;
}

export interface B92LogEntry {
  level: string;
  time: string;
  source: string;
  message: string;
}

class B92WebSocketService {
  private static instance: B92WebSocketService;
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private eventListeners: ((event: B92Event) => void)[] = [];
  private logListeners: ((log: B92LogEntry) => void)[] = [];
  private b92Events: B92Event[] = [];
  private b92Logs: B92LogEntry[] = [];
  private isConnected = false;

  private constructor() {
    this.connect();
  }

  public static getInstance(): B92WebSocketService {
    if (!B92WebSocketService.instance) {
      B92WebSocketService.instance = new B92WebSocketService();
    }
    return B92WebSocketService.instance;
  }

  private connect(): void {
    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      const wsUrl = `${protocol}//${host}/ws/b92`;
      
      this.ws = new WebSocket(wsUrl);
      
      this.ws.onopen = () => {
        console.log('B92 WebSocket connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'b92_event') {
            this.handleB92Event(data);
          }
        } catch (error) {
          console.error('Error parsing B92 WebSocket message:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('B92 WebSocket disconnected');
        this.isConnected = false;
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('B92 WebSocket error:', error);
      };

    } catch (error) {
      console.error('Error creating B92 WebSocket connection:', error);
      this.attemptReconnect();
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect B92 WebSocket (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    } else {
      console.error('Max B92 WebSocket reconnection attempts reached');
    }
  }

  private handleB92Event(event: B92Event): void {
    // Add to events list
    this.b92Events.push(event);
    if (this.b92Events.length > 1000) {
      this.b92Events.shift();
    }

    // Convert to log entry
    const logEntry = this.convertB92EventToLog(event);
    if (logEntry) {
      this.b92Logs.push(logEntry);
      if (this.b92Logs.length > 1000) {
        this.b92Logs.shift();
      }

      // Notify log listeners
      this.logListeners.forEach(listener => {
        try {
          listener(logEntry);
        } catch (error) {
          console.error('Error in B92 log listener:', error);
        }
      });
    }

    // Notify event listeners
    this.eventListeners.forEach(listener => {
      try {
        listener(event);
      } catch (error) {
        console.error('Error in B92 event listener:', error);
      }
    });
  }

  private convertB92EventToLog(event: B92Event): B92LogEntry | null {
    try {
      const time = new Date(event.timestamp * 1000).toLocaleTimeString();
      let level = 'PROTOCOL';
      let message = 'B92 Event';

      // Convert B92 event to human-readable log
      switch (event.event_type) {
        case 'student_b92_send_start':
          level = 'PROTOCOL';
          message = `Student Alice: Starting B92 qubit preparation [b92_send_qubits]`;
          break;
        case 'student_b92_send_complete':
          level = 'STORY';
          message = `Student B92: Sending encoded qubits from Alice's b92_send_qubits() through quantum channel`;
          break;
        case 'student_b92_measure_start':
          level = 'PROTOCOL';
          message = `Student Bob: Starting B92 qubit measurement [b92_process_received_qbit]`;
          break;
        case 'student_b92_measure_complete':
          level = 'PROTOCOL';
          message = `Student Bob: B92 qubit measurement completed [b92_process_received_qbit]`;
          break;
        case 'student_b92_reconcile_start':
          level = 'PROTOCOL';
          message = `Student Bob: Starting B92 reconciliation process [b92_reconcile_bases]`;
          break;
        case 'student_b92_reconcile_complete':
          level = 'PROTOCOL';
          message = `Student Bob: B92 reconciliation completed [b92_reconcile_bases]`;
          break;
        case 'student_b92_error_start':
          level = 'PROTOCOL';
          message = `Student Bob: Starting B92 error rate estimation [b92_estimate_error_rate]`;
          break;
        case 'student_b92_error_complete':
          level = 'PROTOCOL';
          message = `Student Bob: B92 error estimation completed [b92_estimate_error_rate]`;
          break;
        case 'student_b92_ready':
          level = 'PROTOCOL';
          message = `Student Bob: Received all B92 qubits, ready for reconciliation [b92_reconcile_bases]`;
          break;
        case 'student_b92_trigger':
          level = 'PROTOCOL';
          message = `Student Alice: Triggering B92 reconciliation - sending bases to Bob [send_bases_for_reconcile]`;
          break;
        case 'student_b92_complete':
          level = 'PROTOCOL';
          message = `Student B92 Implementation Complete! All methods executed successfully`;
          break;
        default:
          level = 'PROTOCOL';
          message = `B92 Event: ${event.event_type}`;
          break;
      }

      return {
        level,
        time,
        source: event.node,
        message
      };
    } catch (error) {
      console.error('Error converting B92 event to log:', error);
      return null;
    }
  }

  public addEventListener(listener: (event: B92Event) => void): void {
    this.eventListeners.push(listener);
  }

  public removeEventListener(listener: (event: B92Event) => void): void {
    const index = this.eventListeners.indexOf(listener);
    if (index > -1) {
      this.eventListeners.splice(index, 1);
    }
  }

  public addLogListener(listener: (log: B92LogEntry) => void): void {
    this.logListeners.push(listener);
  }

  public removeLogListener(listener: (log: B92LogEntry) => void): void {
    const index = this.logListeners.indexOf(listener);
    if (index > -1) {
      this.logListeners.splice(index, 1);
    }
  }

  public getB92Events(): B92Event[] {
    return [...this.b92Events];
  }

  public getB92Logs(): B92LogEntry[] {
    return [...this.b92Logs];
  }

  public getRecentB92Logs(count: number = 100): B92LogEntry[] {
    return this.b92Logs.slice(-count);
  }

  public isConnectedToB92(): boolean {
    return this.isConnected;
  }

  public disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.isConnected = false;
  }
}

export default B92WebSocketService;
