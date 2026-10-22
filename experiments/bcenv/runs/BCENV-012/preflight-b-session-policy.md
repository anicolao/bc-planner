# Original-session process ownership

Use a dedicated original tool session with a PTY for this preflight and the live
service. Retain that returned session identifier and stop only through that owned
session after work completes. PIDs are meaningful only in their originating
execution namespace; never treat a PID file as a global process identifier or
signal a later observer session's matching numeric PID. No namespace or security
settings are changed. Record terminal status and child completion receipts; do
not infer graceful termination merely from absence of a visible process.

The first preflight's initial substring-based PID inference was corrected before
any signal. Its service/driver ended naturally with exit1 due to the retained
transport race. This second attempt is separately registered, not a retry of the
first attempt's uncertain request. No failed evidence is overwritten.
