import asyncio
import time

class VoiceAssistantDemo:
    def __init__(self):
        self.audio_buffer = []
        self.wake_word_detected = False
        self.pending_responses = []
        
    async def audio_capture_loop(self):
        """Continuously capture audio (simulated)"""
        print("🎤 Audio capture started")
        while True:
            # Simulate capturing audio every 50ms
            audio_chunk = f"audio_chunk_{time.time()}"
            self.audio_buffer.append(audio_chunk)
            
            # Keep buffer manageable
            if len(self.audio_buffer) > 100:
                self.audio_buffer.pop(0)
                
            await asyncio.sleep(0.05)  # 50ms intervals
    
    async def wake_word_monitoring(self):
        """Monitor audio buffer for wake words"""
        print("👂 Wake word monitoring started")
        while True:
            if len(self.audio_buffer) > 10:
                # Simulate wake word detection
                if "special_audio" in str(self.audio_buffer[-1]):
                    print("🔔 Wake word detected!")
                    self.wake_word_detected = True
                    
            await asyncio.sleep(0.1)  # Check every 100ms
    
    async def conversation_processing(self):
        """Handle conversations when wake word is detected"""
        print("💭 Conversation processor started")
        while True:
            if self.wake_word_detected:
                print("🤖 Processing voice command...")
                
                # Simulate LLM processing time
                await asyncio.sleep(1.0)
                
                response = f"Response generated at {time.time()}"
                self.pending_responses.append(response)
                self.wake_word_detected = False
                
            await asyncio.sleep(0.1)
    
    async def response_synthesis(self):
        """Convert responses to speech"""
        print("🔊 Response synthesis started")
        while True:
            if self.pending_responses:
                response = self.pending_responses.pop(0)
                print(f"🗣️ Speaking: {response}")
                
                # Simulate speech synthesis time
                await asyncio.sleep(0.5)
                
            await asyncio.sleep(0.1)
    
    async def run(self):
        """Run all components concurrently"""
        print("🚀 Starting voice assistant...")
        
        # This is where the magic happens - all four loops run together!
        await asyncio.gather(
            self.audio_capture_loop(),
            self.wake_word_monitoring(),
            self.conversation_processing(),
            self.response_synthesis()
        )

# Run the demo
async def main():
    assistant = VoiceAssistantDemo()
    
    # Simulate a wake word after 2 seconds
    async def trigger_wake_word():
        await asyncio.sleep(2)
        assistant.audio_buffer.append("special_audio_chunk")
    
    # Run both the assistant and the trigger
    await asyncio.gather(
        assistant.run(),
        trigger_wake_word()
    )

if __name__ == "__main__":
    asyncio.run(main())
