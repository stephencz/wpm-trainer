# wpm-trainer
WPM Trainer is software designed to train writers write faster.
If you are a writer who can't turn off their inner editor, this might help you.

The software works by setting a WPM target that must be reached every minute over a period of time.
When the goal is met a pleasant chime is played.
When the goal is not met a harsh buzz is played.
A graph visualizing the session results is also generated.

## How should I use this software?

There are two ways to use this software.

Firstly, you can use it to train yourself to write faster. 
If you set the words per minute to, let's say, 50 WPM, then you can force yourself to write that many words in each minute.
The words you write will probably not be of the highest quality, but you will have a high output if you can keep up with the target WPM.

The second, and more powerful way, to use this software is to set it to a lower WPM (10-25 WPM works nicely).
With lower WPM requirements, you can still have time to think about what you are writing, but also gaurentee an output.
For example, at 10 WPM you would have a minimum output of at least 600 WPH.
As someone who over edits my first drafts, and can waste hours fiddling with a single paragraph, this is how I use the software. 

## Note About False Positives
Some anti-virus software may flag this program as a keylogger. 
This happens because the script actually does contain a keylogger.
For the software to work, keystrokes must be recorded no matter which software the user is writing with.
Keystrokes are only recorded while a training session is running.
Recorded keystrokes are recorded and discarded every minute, and all results are discarded when a session ends or is reset.

Keystrokes **are not** recorded outside of training sessions or when the software isn't running.
You can verify this for yourself by viewing the *gui.py* and *keylisten.py* modules.

## Note About OS Support

Currently, this software only supports Microsoft Windows operating systems.
I have plans to provide Linux support in the future.

