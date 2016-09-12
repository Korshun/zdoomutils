This is a collection of utilities to simplify modding for ZDoom. You need [Python 3](https://www.python.org/downloads/) to run them.

## acsinclude

Replaces `#include` directives with contents of the included files. Ignores zcommon.acs.

## sndinfogen

Automatically generates an SNDINFO lump from the contents of the `sounds/` directory, allowing you to write `A_PlaySound("LUMPNAME")`. Automatically randomizes sounds by name: if you have `SND1`, `SND2` and `SND3`, it will add `$random SND { SND1 SND2 SND3 }`. Detects conflicting sound filenames, even if the sounds are in different directories.
