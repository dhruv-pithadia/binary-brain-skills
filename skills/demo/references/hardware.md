# Measure the target machine

Inspect the actual target before choosing a budget. Run the doctor for architecture, total RAM where available, output-filesystem free disk, and CLI availability. Total RAM is not available memory; check current pressure with permitted diagnostics.

For a constrained machine, start with HTML/SVG, 30fps, a 540x960 draft, and one heavy stage at a time. Test a representative 3-5 second segment before a full render. Use a stronger or remote machine's measured capacity when it is the target. Do not assume the reference author's MacBook belongs to the user.

Release TTS/alignment models before rendering when memory is tight. Prefer existing cached small models with supported compute types. Do not assume CUDA or Metal support from an operating system or GPU name.

Bound SVG filters, live blurs, textures, and simultaneous video layers. Prefer supported streamed encoding to huge image sequences. Estimate scratch space from a measured sample and total frames, leaving headroom for swap and encoding.

Blender is optional for requested 3D. Check current requirements and test a small scene. Do not install a large renderer/model stack merely because the task mentions video.

Disclose lower-resolution delivery. Do not upscale a draft and label it native 1080p. Stop a repeated resource failure, simplify, and retest once. Do not delete user caches or switch to metered remote resources without authorization.

Read [Blender requirements](https://www.blender.org/download/requirements/), [Kokoro guidance](https://github.com/hexgrad/kokoro), or [faster-whisper requirements](https://github.com/SYSTRAN/faster-whisper) when selecting those tools. Tool presence is not a render benchmark.
