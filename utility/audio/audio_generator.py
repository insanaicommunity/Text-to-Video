#import edge_tts

#async def generate_audio(text,outputFilename):
#   communicate = edge_tts.Communicate(text,"en-AU-WilliamNeural")
#   await communicate.save(outputFilename)

# ============================================
# FIX 2: REPLACE AUDIO GENERATOR (RECOMMENDED)
# ============================================
# Jalankan cell ini untuk mengganti audio_generator.py

audio_generator_code = '''
import edge_tts
import asyncio
from gtts import gTTS
import os

# Voice options for Edge TTS
VOICE = "en-US-ChristopherNeural"  # Male voice
# VOICE = "en-US-JennyNeural"      # Female voice

async def generate_audio_edge(text, output_filename):
    """Generate audio using Edge TTS"""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_filename)

def generate_audio_gtts(text, output_filename):
    """Fallback: Generate audio using Google TTS"""
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_filename)

async def generate_audio(text, output_filename):
    """
    Generate audio with automatic fallback:
    1. Try Edge TTS (better quality)
    2. Fallback to gTTS if Edge TTS fails
    """
    print("🎤 Generating audio...")
    
    # Method 1: Try Edge TTS
    try:
        print("   Trying Edge TTS...")
        await generate_audio_edge(text, output_filename)
        print("   ✅ Audio generated with Edge TTS")
        return
    except Exception as e:
        print(f"   ⚠️ Edge TTS failed: {type(e).__name__}")
    
    # Method 2: Fallback to gTTS
    try:
        print("   Trying Google TTS (fallback)...")
        generate_audio_gtts(text, output_filename)
        print("   ✅ Audio generated with Google TTS")
        return
    except Exception as e:
        print(f"   ⚠️ gTTS failed: {type(e).__name__}")
    
    # Method 3: Last resort - create silent audio
    try:
        print("   Creating placeholder audio...")
        import subprocess
        duration = len(text.split()) * 0.5  # Rough estimate
        subprocess.run([
            'ffmpeg', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=mono',
            '-t', str(duration), '-q:a', '9', output_filename
        ], capture_output=True)
        print("   ⚠️ Created silent audio (TTS unavailable)")
    except Exception as e:
        raise Exception(f"All audio generation methods failed: {e}")

# Synchronous wrapper for compatibility
def generate_audio_sync(text, output_filename):
    """Synchronous wrapper for generate_audio"""
    asyncio.run(generate_audio(text, output_filename))
'''

# Write the new audio generator
with open('utility/audio/audio_generator.py', 'w') as f:
    f.write(audio_generator_code)

print("✅ audio_generator.py has been updated with fallback support!")
print("🔄 Now run the video generation again")




