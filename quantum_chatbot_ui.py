"""
Quantum Cryptography Chatbot UI Component
Simple interface for students to interact with the AI assistant
"""

import os
import ipywidgets as widgets
from IPython.display import display, clear_output
from openai import OpenAI
from promptforqkd import QUANTUM_CRYPTOGRAPHY_PROMPT

class SimpleQuantumChatbot:
    """Simple chatbot for quantum cryptography assistance"""
    
    def __init__(self):
        # Initialize OpenAI client with Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Please set GEMINI_API_KEY environment variable")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        )
        
        self.messages = [
            {"role": "system", "content": QUANTUM_CRYPTOGRAPHY_PROMPT}
        ]
    
    def get_response(self, user_message):
        """Get response from Gemini API"""
        try:
            # Add user message
            self.messages.append({"role": "user", "content": user_message})
            
            # Call Gemini API
            response = self.client.chat.completions.create(
                model="gemini-1.5-flash-latest",
                messages=self.messages,
                max_tokens=4000,
                temperature=0.7
            )
            
            # Extract response
            ai_response = response.choices[0].message.content
            
            # Add AI response to conversation
            self.messages.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.messages = [
            {"role": "system", "content": QUANTUM_CRYPTOGRAPHY_PROMPT}
        ]

def create_quantum_chatbot_ui():
    """Create the quantum chatbot interface for students"""
    
    # Initialize chatbot
    try:
        chatbot = SimpleQuantumChatbot()
    except ValueError as e:
        print(f"❌ {e}")
        print("💡 Please set your GEMINI_API_KEY environment variable first!")
        return None
    
    # Chat display - bigger interface
    chat_display = widgets.Output(layout=widgets.Layout(height='600px', overflow='auto'))
    
    # Input
    user_input = widgets.Textarea(
        placeholder="Ask me about BB84, B92, or quantum networking...",
        layout=widgets.Layout(width='100%', height='80px')
    )
    
    # Buttons
    send_btn = widgets.Button(description="Send", button_style='primary', layout=widgets.Layout(width='80px'))
    clear_btn = widgets.Button(description="Clear", button_style='warning', layout=widgets.Layout(width='80px'))
    code_btn = widgets.Button(description="Code", button_style='success', layout=widgets.Layout(width='80px'))
    
    # Quick action buttons
    bb84_btn = widgets.Button(description="BB84", button_style='info', layout=widgets.Layout(width='80px'))
    b92_btn = widgets.Button(description="B92", button_style='info', layout=widgets.Layout(width='80px'))
    debug_btn = widgets.Button(description="Debug", button_style='danger', layout=widgets.Layout(width='80px'))
    
    def display_message(role, content):
        """Display a message in the chat"""
        with chat_display:
            if role == "user":
                print(f"👤 You: {content}")
            else:
                print(f"🤖 Assistant: {content}")
                print("-" * 50)
    
    def send_message(b):
        """Send message to chatbot"""
        if user_input.value.strip():
            message = user_input.value.strip()
            user_input.value = ""
            
            display_message("user", message)
            
            with chat_display:
                print("🤔 Thinking...")
            
            # Get response from Gemini
            response = chatbot.get_response(message)
            
            with chat_display:
                clear_output(wait=True)
                display_message("user", message)
                display_message("assistant", response)
    
    def clear_chat(b):
        """Clear chat history"""
        chatbot.clear_history()
        chat_display.clear_output()
        with chat_display:
            print("🗑️ Chat cleared!")
    
    def code_help(b):
        """Get code help"""
        user_input.value = "Show me Python code for quantum key distribution with examples"
        send_message(None)
    
    def bb84_help(b):
        """BB84 help"""
        user_input.value = "Explain BB84 protocol and provide Python implementation"
        send_message(None)
    
    def b92_help(b):
        """B92 help"""
        user_input.value = "Explain B92 protocol and provide Python implementation"
        send_message(None)
    
    def debug_help(b):
        """Debug help"""
        user_input.value = "Help me debug my quantum simulation code"
        send_message(None)
    
    # Bind events
    send_btn.on_click(send_message)
    clear_btn.on_click(clear_chat)
    code_btn.on_click(code_help)
    bb84_btn.on_click(bb84_help)
    b92_btn.on_click(b92_help)
    debug_btn.on_click(debug_help)
    
    # Handle Enter key for Textarea
    def handle_enter(change):
        if change['new'] and change['new'].endswith('\n'):
            user_input.value = change['new'].rstrip('\n')
            send_message(None)
    
    user_input.observe(handle_enter, names='value')
    
    # Layout
    quick_actions = widgets.HBox([bb84_btn, b92_btn, debug_btn, code_btn])
    input_row = widgets.HBox([user_input, send_btn, clear_btn])
    
    interface = widgets.VBox([
        widgets.HTML("<h2 style='text-align: center; color: #2c3e50;'>🤖 Quantum Networking AI Assistant</h2>"),
        widgets.HTML("<p style='text-align: center; color: #6c757d;'>Powered by Gemini 1.5 Flash • Ask for code, explanations, or debugging help</p>"),
        chat_display,
        quick_actions,
        input_row
    ])
    
    return interface

def load_quantum_chatbot():
    """Simple function for students to load the chatbot"""
    print("🚀 Loading Quantum Cryptography AI Assistant...")
    interface = create_quantum_chatbot_ui()
    if interface:
        display(interface)
        print("✅ Chatbot loaded successfully!")
    else:
        print("❌ Failed to load chatbot. Please check your API key.")
