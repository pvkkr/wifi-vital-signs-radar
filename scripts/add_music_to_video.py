"""
Soundtrack Synthesizer & Video Audio Processor
1. Synthesizes a high-fidelity 65-BPM ambient tech & heartbeat pulse soundtrack.
2. Removes background room/fan noise from 'final video.mp4'.
3. Produces two production-ready video files:
   - WiFi_CSI_Vital_Signs_Demo_Music.mp4 (Pure high-definition ambient tech music)
   - WiFi_CSI_Vital_Signs_Demo_Mixed.mp4 (Denoised ambient sound + background music)
"""

import os
import subprocess
import numpy as np
import scipy.io.wavfile as wav
import imageio_ffmpeg

def synthesize_soundtrack(duration_sec=31.2, sr=44100):
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False)
    audio = np.zeros_like(t)

    # 1. Rhythmic 65 BPM Cardiac Pulse (matches the 65 BPM video reading!)
    # 65 BPM = 1.0833 beats per second
    bpm = 65.0
    beat_interval = 60.0 / bpm
    
    # Generate heartbeat "lub-dub" acoustic pulse
    for beat_time in np.arange(0.5, duration_sec - 1.0, beat_interval):
        idx1 = int(beat_time * sr)
        idx2 = int((beat_time + 0.14) * sr) # 'dub' follows 140ms later
        
        # Lub pulse (lower frequency, ~55 Hz)
        pulse_len1 = int(0.12 * sr)
        if idx1 + pulse_len1 < len(t):
            t_pulse = np.linspace(0, 0.12, pulse_len1)
            env1 = np.exp(-35 * t_pulse) * np.sin(np.pi * t_pulse / 0.12)
            pulse1 = 0.22 * np.sin(2 * np.pi * 55 * t_pulse) * env1
            audio[idx1:idx1+pulse_len1] += pulse1
            
        # Dub pulse (slightly higher, ~75 Hz)
        pulse_len2 = int(0.10 * sr)
        if idx2 + pulse_len2 < len(t):
            t_pulse2 = np.linspace(0, 0.10, pulse_len2)
            env2 = np.exp(-40 * t_pulse2) * np.sin(np.pi * t_pulse2 / 0.10)
            pulse2 = 0.18 * np.sin(2 * np.pi * 75 * t_pulse2) * env2
            audio[idx2:idx2+pulse_len2] += pulse2

    # 2. Lush Ambient Synth Chords (Cmaj9 -> Am7 -> Fmaj7 -> Gsus4)
    # Chord progression: each chord lasts ~7.5 seconds
    chord_freqs = [
        [130.81, 164.81, 196.00, 246.94, 293.66],  # Cmaj9 (C3, E3, G3, B3, D4)
        [110.00, 130.81, 164.81, 196.00, 246.94],  # Am9 (A2, C3, E3, G3, B3)
        [87.31, 130.81, 174.61, 220.00, 261.63],   # Fmaj7 (F2, C3, F3, A3, C4)
        [98.00, 146.83, 196.00, 261.63, 293.66]    # Gsus4 (G2, D3, G3, C4, D4)
    ]
    chord_duration = duration_sec / 4.0

    for i, chord in enumerate(chord_freqs):
        c_start = i * chord_duration
        c_end = (i + 1) * chord_duration
        idx_start = int(c_start * sr)
        idx_end = int(min(duration_sec, c_end + 1.5) * sr)  # Overlap chords smoothly
        c_len = idx_end - idx_start
        t_c = np.linspace(0, (c_len / sr), c_len)

        # Smooth attack and release envelope
        env = np.ones(c_len)
        attack_len = int(0.8 * sr)
        release_len = int(1.2 * sr)
        env[:attack_len] = np.linspace(0, 1, attack_len) ** 2
        env[-release_len:] = np.linspace(1, 0, release_len) ** 2

        chord_signal = np.zeros(c_len)
        for f in chord:
            # Warm pad with subtle detuning and gentle harmonics
            v1 = np.sin(2 * np.pi * f * t_c)
            v2 = 0.5 * np.sin(2 * np.pi * (f * 1.002) * t_c)
            v3 = 0.25 * np.sin(2 * np.pi * (f * 2.0) * t_c)
            chord_signal += (v1 + v2 + v3)

        audio[idx_start:idx_end] += 0.08 * (chord_signal / len(chord)) * env

    # 3. High-Tech Sparkling Arpeggio (Gentle glass chimes)
    arpeggio_notes = [523.25, 587.33, 659.25, 783.99, 880.00, 987.77, 1046.50] # Pentatonic C
    arp_step = beat_interval / 4.0 # 16th notes
    for step_idx, note_t in enumerate(np.arange(1.5, duration_sec - 1.5, arp_step)):
        if step_idx % 3 == 0:  # Sparse tech pattern
            note_idx = (step_idx * 2) % len(arpeggio_notes)
            f_note = arpeggio_notes[note_idx]
            
            note_start = int(note_t * sr)
            note_len = int(0.25 * sr)
            if note_start + note_len < len(t):
                t_note = np.linspace(0, 0.25, note_len)
                env_note = np.exp(-18 * t_note) * np.sin(np.pi * t_note / 0.25)
                note_wave = 0.045 * (np.sin(2 * np.pi * f_note * t_note) + 0.3 * np.sin(2 * np.pi * (f_note * 2) * t_note)) * env_note
                audio[note_start:note_start+note_len] += note_wave

    # 4. Global Master Fade In & Fade Out
    fade_in = int(1.5 * sr)
    fade_out = int(2.0 * sr)
    audio[:fade_in] *= np.linspace(0, 1, fade_in)
    audio[-fade_out:] *= np.linspace(1, 0, fade_out)

    # Normalize to -1.5 dB peak
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = (audio / peak) * 0.85

    # Convert to 16-bit PCM Stereo
    audio_int16 = (audio * 32767).astype(np.int16)
    stereo_audio = np.column_stack((audio_int16, audio_int16))
    return stereo_audio

def process_video():
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    video_input = os.path.join(base_dir, "final video.mp4")
    
    if not os.path.exists(video_input):
        print(f"[ERROR] Could not find '{video_input}'!")
        return

    # Output filenames
    soundtrack_wav = os.path.join(base_dir, "assets", "vital_radar_soundtrack.wav")
    os.makedirs(os.path.join(base_dir, "assets"), exist_ok=True)
    
    output_music_only = os.path.join(base_dir, "WiFi_CSI_Vital_Signs_Demo_Music.mp4")
    output_mixed = os.path.join(base_dir, "WiFi_CSI_Vital_Signs_Demo_Mixed.mp4")

    print("[1/3] Synthesizing 65-BPM Ambient Tech & Heartbeat Soundtrack...")
    sr = 44100
    stereo_data = synthesize_soundtrack(duration_sec=31.2, sr=sr)
    wav.write(soundtrack_wav, sr, stereo_data)
    print(f"      Generated soundtrack: {soundtrack_wav}")

    print("\n[2/3] Generating Video 1 (Pure Ambient Music & 65-BPM Heartbeat Pulse)...")
    # Replace audio completely with the soundtrack
    cmd_music_only = [
        ffmpeg_exe, "-y",
        "-i", video_input,
        "-i", soundtrack_wav,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_music_only
    ]
    subprocess.run(cmd_music_only, check=True)
    print(f"      Successfully created: {output_music_only}")

    print("\n[3/3] Generating Video 2 (Denoised Room Mic + Background Music)...")
    # Apply FFT-based noise reduction filter + highpass on original mic, then mix with music
    filter_complex = (
        "[0:a]highpass=f=120,afftdn=nf=-24:tn=1,volume=0.7[denoised];"
        "[1:a]volume=0.85[music];"
        "[denoised][music]amix=inputs=2:duration=first[aout]"
    )
    cmd_mixed = [
        ffmpeg_exe, "-y",
        "-i", video_input,
        "-i", soundtrack_wav,
        "-c:v", "copy",
        "-filter_complex", filter_complex,
        "-map", "0:v:0",
        "-map", "[aout]",
        "-c:a", "aac",
        "-b:a", "256k",
        output_mixed
    ]
    subprocess.run(cmd_mixed, check=True)
    print(f"      Successfully created: {output_mixed}")
    
    print("\n=======================================================")
    print("  ALL VIDEOS PROCESSED & READY FOR YOUTUBE / LINKEDIN!")
    print("=======================================================")

if __name__ == "__main__":
    process_video()
