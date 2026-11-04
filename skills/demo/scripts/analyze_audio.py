#!/usr/bin/env python3
"""Stream 16-bit PCM WAV into mouth-envelope data and non-destructive quiet hints."""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import sys
import wave


def dbfs(raw):
    samples = array('h', raw)
    if sys.byteorder != 'little':
        samples.byteswap()
    if not samples:
        return -120.0
    mean_square = sum(value * value for value in samples) / len(samples)
    return 20 * math.log10(max(math.sqrt(mean_square) / 32768, 1e-6))


def analyze(path, fps):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(65536), b''):
            digest.update(chunk)
    with wave.open(str(path), 'rb') as audio:
        rate, total, channels = audio.getframerate(), audio.getnframes(), audio.getnchannels()
        if audio.getsampwidth() != 2 or audio.getcomptype() != 'NONE' or channels not in (1, 2):
            raise ValueError('Use uncompressed 16-bit PCM WAV with one or two channels.')
        if rate <= 0 or total <= 0:
            raise ValueError('Audio must contain samples at a positive sample rate.')
        duration = total / rate
        frames, previous, position = [], 0.0, 0
        for index in range(math.ceil(total * fps / rate)):
            end = min(total, round((index + 1) * rate / fps))
            level = dbfs(audio.readframes(end - position))
            target = min(1.0, max(0.0, (level + 42) / 26))
            strength = target if target >= previous else max(target, previous * 0.55)
            frames.append({'time': round(index / fps, 6), 'dbfs': round(level, 3),
                           'mouth': min(9, max(0, round(strength * 9)))})
            previous, position = strength, end
        audio.rewind()
        window = max(1, round(rate * 0.03))
        position, quiet_start, quiet = 0, None, []
        while position < total:
            count = min(window, total - position)
            level = dbfs(audio.readframes(count))
            if level < -50:
                if quiet_start is None:
                    quiet_start = position / rate
            elif quiet_start is not None:
                if position / rate - quiet_start > 0.24:
                    quiet.append({'start': quiet_start, 'end': position / rate})
                quiet_start = None
            position += count
        if quiet_start is not None and duration - quiet_start > 0.24:
            quiet.append({'start': quiet_start, 'end': duration})
    return {'source_audio_sha256': digest.hexdigest(), 'duration_seconds': duration,
            'fps': fps, 'sample_rate': rate, 'channels': channels,
            'method': 'RMS amplitude only; not phoneme alignment or word transcription',
            'outside_audio_mouth': 0, 'mouth_frames': frames,
            'quiet_candidates': quiet,
            'quiet_note': 'Review by listening. No audio has been trimmed; quiet speech can be below the threshold.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('audio', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--fps', type=int, default=30)
    args = parser.parse_args()
    if not 1 <= args.fps <= 60:
        parser.error('--fps must be between 1 and 60')
    if args.audio.resolve() == args.output.resolve():
        parser.error('Output must not overwrite the audio file.')
    try:
        result = analyze(args.audio, args.fps)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    except (OSError, wave.Error, ValueError, EOFError) as error:
        parser.exit(1, f'Audio analysis failed: {error}\n')
    print(f'Wrote {len(result["mouth_frames"])} mouth frames for {result["duration_seconds"]:.3f}s; audio unchanged.')


if __name__ == '__main__':
    main()
