# wpm-trainer
WPM Trainer is software designed to train writers write faster.
If you are a writer who can't turn off their inner editor, this might help you.

The software works by setting a WPM target that must be reached every minute over a period of time.
When the goal is met a pleasant chime is played.
When the goal is not met a harsh buzz is played.
A graph visualizing the session results is also generated.

## Note About False Positives
Some anti-virus software may flag this program as a keylogger. 
This happens because the script actually does contain a keylogger.
For the software to work, keystrokes must be recorded no matter which software the user is writing with.
Keystrokes are only recorded while a training session is running.
Recorded keystrokes are recorded and discarded every minute, and all results are discarded when a session ends or is reset.
Keystrokes **are not** recorded outside of training sessions or when the software isn't running.
You can verify this for yourself by viewing the source code.