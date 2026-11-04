"""Check audio-data behavior using known PCM signals, without models or networking."""
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import wave

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/demo/scripts/analyze_audio.py'


class AudioAnalysisTests(unittest.TestCase):
    def test_silence_speech_silence_and_non_destructive_output(self):
        with tempfile.TemporaryDirectory() as d:
            audio, output = Path(d) / 'signal.wav', Path(d) / 'analysis.json'
            rate = 44100
            samples = [0] * rate
            samples += [int(16000 * math.sin(2 * math.pi * 440 * i / rate)) for i in range(rate)]
            samples += [0] * rate
            with wave.open(str(audio), 'wb') as wav:
                wav.setparams((1, 2, rate, 0, 'NONE', 'not compressed'))
                wav.writeframes(struct.pack('<' + 'h' * len(samples), *samples))
            before = hashlib.sha256(audio.read_bytes()).hexdigest()
            subprocess.run([sys.executable, str(SCRIPT), str(audio), '--output', str(output)], check=True, capture_output=True)
            result = json.loads(output.read_text())
            self.assertEqual(result['source_audio_sha256'], before)
            self.assertEqual(hashlib.sha256(audio.read_bytes()).hexdigest(), before)
            self.assertEqual(len(result['mouth_frames']), 90)
            self.assertEqual(result['duration_seconds'], 3)
            self.assertTrue(all(f['mouth'] == 0 for f in result['mouth_frames'][:30]))
            self.assertGreater(max(f['mouth'] for f in result['mouth_frames'][30:60]), 0)
            self.assertEqual(result['mouth_frames'][-1]['mouth'], 0)
            self.assertEqual(len(result['quiet_candidates']), 2)
            self.assertEqual(result['outside_audio_mouth'], 0)

    def test_unsupported_sample_width_is_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as d:
            audio, output = Path(d) / '8bit.wav', Path(d) / 'analysis.json'
            with wave.open(str(audio), 'wb') as wav:
                wav.setparams((1, 1, 8000, 0, 'NONE', 'not compressed'))
                wav.writeframes(bytes([128]) * 800)
            result = subprocess.run([sys.executable, str(SCRIPT), str(audio), '--output', str(output)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())
            self.assertIn('16-bit PCM', result.stderr)


if __name__ == '__main__':
    unittest.main()
