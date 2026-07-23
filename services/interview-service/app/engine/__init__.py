# The OpenAI interview engine, called internally by app/services/ (no
# network hop — see architecture discussion on why this stays a module
# rather than its own microservice). Stateless: every function takes
# whatever context it needs as arguments and returns a decision; it never
# reads or writes storage itself — app/services/ does the remembering.
#
#   client.py              — shared OpenAI client + model name
#   types.py                — TranscriptTurn, shared across all engine calls
#   question_generator.py   — opening question for a new interview
#   interview_engine.py     — next-step decision: follow-up question +
#                              difficulty adjustment + end-of-interview
#                              detection, combined into one structured call
#                              (see interview_engine.py's docstring for why
#                              this consolidates two boxes from
#                              architecture.png into one LLM call)
#   feedback_generator.py   — final scored feedback once the interview ends