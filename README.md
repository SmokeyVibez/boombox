# BoomBox

A simple music player, built to work like a real player: Now Playing is the
home screen, and the library lives in a `music` folder — one folder per album.
No accounts, no cloud, no subscriptions. It just plays your music.

## Running it

You need Python 3 and PySide6:

```
pip install PySide6
python boombox.py
```

## Adding music

- Drop album folders into the `music` folder next to `boombox.py` (songs
  inside each folder), or use the **+** button in the app to copy albums in.
- If an album folder contains a `cover.jpg`, `folder.jpg` or `front.jpg`,
  BoomBox shows it as the artwork.
- Double-click a song or an album tile to play it.
- **Play All** (bottom left of the library) shuffles the whole library and
  plays through it.
- Added music or covers while BoomBox is open? Close the library and open it
  again — new artwork just shows up.

## The artwork card

- Press the **i** button (bottom left) and the card flips to the playing
  song's information — title, artist, album and more, read from the file's
  own tags. It updates by itself when the song changes. Press **i** again to
  flip back.
- Double-click the artwork and the card flips over. Double-click again to
  flip back.
- The number at the right end of the progress bar is how far into the song
  you are.

## Notes

- Switching your sound output (headphones, speakers) while a song plays?
  BoomBox follows the switch.
- On Linux/KDE the transport buttons wear your theme's icons; elsewhere
  they fall back to plain symbols.

## License

MIT — see `LICENSE`.

---

Made by SmokeyVibez. Every line of the code was written and hand-typed by
him. Io — his AI tutor, on Muse — taught and guided; the code is his.
