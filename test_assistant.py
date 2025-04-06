from gui.ai_assistant import AIAssistant

def main():
    print("=== AI Assistant Manual Test ===")
    
    # Initialize the assistant
    try:
        assistant = AIAssistant()
        print("✓ Successfully initialized AI Assistant")
    except Exception as e:
        print(f"✗ Failed to initialize AI Assistant: {e}")
        return

    # Start conversation loop
    print("\nEnter your messages (type 'quit' to exit, 'reset' to start new conversation):")
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for quit command
        if user_input.lower() == 'quit':
            break
            
        # Check for reset command
        if user_input.lower() == 'reset':
            assistant.reset_conversation()
            print("Conversation reset. Starting new session.")
            continue
            
        # Skip empty messages
        if not user_input:
            continue

        # Process message
        try:
            result = assistant.analyze_message(user_input)
            if result['success']:
                print("\nAssistant:", result['response'])
            else:
                print("\n❌ Error:", result['message'])
        except Exception as e:
            print(f"\n❌ Error processing message: {e}")

    print("\nTest session ended.")

if __name__ == "__main__":
    main() 