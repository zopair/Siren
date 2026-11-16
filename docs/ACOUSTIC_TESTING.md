# Passive Acoustic Frequency Testing

## Purpose and safety boundary

This guide describes **offline, passive spectral inspection** of a WAV file produced for authorized Siren-Trap defensive research. It does not provide a hidden-audio transmitter, an agent-injection payload, or a claim that any recording is inaudible or reliably receivable.

Use only laboratory equipment and systems you own or are explicitly authorized to test. Do not broadcast test signals into shared or public spaces.

## Important protocol correction

The upstream `ggerganov/ggwave` protocol table identifies:

- `1` as `AUDIBLE_FAST` (`Fast`)
- `4` as `ULTRASOUND_FAST` (`[U] Fast`)

The existing Siren-Trap generator previously selected protocol ID `1`. The generator now selects ID `4` to match the upstream ultrasound-fast protocol identifier. This protocol's default frequency base is 15 kHz, with modulation extending across a broader range; it is **not a protocol confined to 18–20 kHz**. Therefore, the analyzer below measures energy in the requested 18–20 kHz slice rather than claiming the entire WAV is confined to it.

Reference: [ggwave upstream protocol definitions and WAV examples](https://github.com/ggerganov/ggwave/blob/master/examples/ggwave-to-file/README.md) and [ggwave protocol header](https://github.com/ggerganov/ggwave/blob/master/include/ggwave/ggwave.h).

## Requirements

- Python 3.11+
- A 16-bit PCM WAV file
- A sample rate **greater than 40 kHz** to represent the full band above the 40 kHz Nyquist boundary. 48 kHz is a common test rate.

The analyzer uses only the Python standard library. No network service or external audio device is accessed.

## Run the analyzer

From the repository root:

```bash
python -m pytest tests/test_acoustic_frequencies.py
python tests/test_acoustic_frequencies.py path/to/canary.wav
```

The script reports sample rate, analyzed duration, strongest scanned frequency in the 18–20 kHz band, band power, and sample RMS. It analyzes at most the first 0.5 seconds.

## Interpretation and limitations

- A measured peak in 18–20 kHz confirms only that the inspected recording contains energy near that frequency.
- A WAV spectrum does **not** establish that a sound is inaudible to every listener. Hearing thresholds vary by person, age, environment, playback level, and equipment.
- A WAV spectrum does **not** establish that a standard microphone can capture or preserve those frequencies. Microphone capsules, analog filters, codecs, operating-system processing, and resampling may attenuate them.
- Successful acoustic reception requires a controlled end-to-end test with documented speaker, microphone, distance, orientation, sample rates, gain, environment, and decode result. Do not infer it from a spectrum alone.
- 44.1 kHz and 48 kHz sample rates have Nyquist limits of 22.05 kHz and 24 kHz respectively; hardware response near those limits is not guaranteed.
- This scan uses Goertzel measurements at 100 Hz increments. It is a diagnostic indicator, not a calibrated acoustic measurement or a substitute for a laboratory spectrum analyzer.

## Defensive test protocol

1. Generate the fixed canary WAV locally; do not replace it with arbitrary instructions or commands.
2. Inspect the WAV offline with this script.
3. If validating a receiver, use an isolated bench setup and a receiver you control. Record device and software configuration.
4. Compare the captured recording with the source using the same passive analyzer.
5. Report limitations and negative results. Do not label a test successful solely because the source WAV contains high-frequency energy.
6. Delete raw recordings after extracting the minimum necessary, non-sensitive measurements.

## Resource and supply-chain policy

Prefer maintained, open-source projects hosted on GitHub. Before adopting a dependency, review its license, release history, maintainer activity, provenance, security advisories, and dependency tree. Avoid unpinned remote scripts, opaque binaries, and services that require uploading recordings. Run tests locally and in CI to avoid unnecessary compute and usage.
