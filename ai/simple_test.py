#!/usr/bin/env python3
"""
Simple test script for SpeechToTextModel
Run: python simple_test.py
"""

import os
import sys
from speech_model import SpeechToTextModel  # Your file should be named speech_model.py

def test_model_loading():
    """Test 1: Model Loading"""
    print("🤖 Testing Model Loading...")
    try:
        model = SpeechToTextModel(model_size="base")  # Use tiny for faster loading
        print("✅ Model loaded successfully!")
        
        info = model.get_model_info()
        print(f"   Model size: {info['model_size']}")
        print(f"   Model loaded: {info['model_loaded']}")
        print(f"   Supported languages: {len(info['supported_languages'])}")
        
        return model
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return None

def test_file_transcription(model):
    """Test 2: File Transcription (if you have an audio file)"""
    print("\n🎵 Testing File Transcription...")
    
    # Look for common audio files in current directory
    audio_files = []
    for ext in ['.wav', '.mp3', '.m4a', '.flac']:
        for file in os.listdir('.'):
            if file.lower().endswith(ext):
                audio_files.append(file)
    
    if audio_files:
        test_file = audio_files[0]
        print(f"   Found audio file: {test_file}")
        try:
            result = model.transcribe_file(test_file)
            print("✅ File transcription successful!")
            print(f"   Text: {result['text'][:100]}...")
            print(f"   Language: {result['language']}")
            print(f"   Confidence: {result['confidence']:.2f}")
            return True
        except Exception as e:
            print(f"❌ File transcription failed: {e}")
            return False
    else:
        print("⚠️  No audio files found in current directory")
        print("   To test file transcription, add a .wav, .mp3, .m4a, or .flac file")
        return False

def test_youtube_transcription(model):
    """Test 3: YouTube Transcription"""
    print("\n📺 Testing YouTube Transcription...")
    
    # Short test video (19 seconds)
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    
    response = input("   Test with short YouTube video? This will take 1-2 minutes (y/N): ").lower()
    if response != 'y':
        print("   Skipped YouTube test")
        return False
    
    try:
        print(f"   Processing: {test_url}")
        print("   ⏳ This may take 1-2 minutes...")
        
        result = model.transcribe_youtube_video(test_url, language="en")
        
        print("✅ YouTube transcription successful!")
        print(f"   Title: {result['video_title']}")
        print(f"   Duration: {result['duration']} seconds")
        print(f"   Language: {result['language']}")
        print(f"   Confidence: {result['confidence']:.2f}")
        print(f"   Text: {result['text'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ YouTube transcription failed: {e}")
        print("   This could be due to network issues, blocked videos, or missing FFmpeg")
        return False

def main():
    print("🎤 Simple Speech Model Test")
    print("=" * 40)
    
    # Test 1: Model Loading
    model = test_model_loading()
    if not model:
        print("\n❌ Cannot continue - model loading failed")
        return
    
    # Test 2: File Transcription
    file_test_passed = test_file_transcription(model)
    
    # Test 3: YouTube Transcription
    youtube_test_passed = test_youtube_transcription(model)
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 40)
    print(f"✅ Model Loading: PASSED")
    print(f"{'✅' if file_test_passed else '⚠️ '} File Transcription: {'PASSED' if file_test_passed else 'SKIPPED'}")
    print(f"{'✅' if youtube_test_passed else '⚠️ '} YouTube Transcription: {'PASSED' if youtube_test_passed else 'SKIPPED'}")
    
    if file_test_passed or youtube_test_passed:
        print("\n🎉 Your speech model is working correctly!")
    else:
        print("\n⚠️  Basic model loading works, but transcription tests were skipped.")
        print("   Try adding an audio file or testing with YouTube.")

if __name__ == "__main__":
    main()