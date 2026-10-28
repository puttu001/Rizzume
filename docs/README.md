# Rizzume architecture and guide

These notes are a code-based guide to the system as it exists in this repository. They are intended for learning the design.
## Reading order

1. [HLD: system map and end-to-end flows](HLD.md)
2. [LLD: APIs, modules, data and state](LLD.md)
3. [Voice AI concepts: how the audio pipeline works](VOICE_AI_CONCEPTS.md)
4. [Interactive visual guide](visual-guide.html) — standalone HTML with clickable components, animated request flows and searchable concepts.

The diagrams use Mermaid. GitHub renders them in Markdown; in editors without Mermaid support, use a Mermaid preview extension.

## Important scope note

The app is an **AI interview practice app with turn-based speech input/output**. It does not implement a continuous, low-latency voice agent. Speech recognition is an asynchronous Celery job; speech synthesis is a synchronous HTTP request. The reporting service is scaffolded but is not part of the active interview flow. See the status section in [HLD](HLD.md).
