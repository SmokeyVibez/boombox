#!/usr/bin/env python3
# Version 3.6.0 - transport buttons use real icons
# Version 3.5.6 - sound follows when you switch output devices
# Version 3.5.5 - stacked and two-part names show the title only
# Version 3.5.4 - genre shows as words, not as list
# Version 3.5.3 - library only rebuilds when something changed
# Version 3.5.2 - library refreshes on open, new covers show without a restart
# Version 3.5.1 - library buttons aligned right
# Version 3.5.0 - time readout at the end of the progress bar
# Version 3.4.0 - info button flips artwork to song information
# Version 3.3.0 - double-click artwork flips to the credits
# Version 3.2.0 - Play All button shuffles the whole library
# Version 3.1.3 - library slide no longer shifts the window or the player
# Version 3.1.2 - panel height follow the frame, + and - buttons no longer clip
# Version 3.1.1 - slide squish fixed, info button moved into the transport row
# Version 3.1.0 - About window on a round info button, bottom left
# Version 3.0.0 - renamed to BoomBox
# Version 2.8.1 - boombox titlebar icon, window title follows the song
# Version 2.8.0 - delete mode for albums, buttons keep no focus glow
# Version 2.7.0 - artwork placeholders, home picture, smooth scaling
# Version 2.6.2 - grid fills width, no scrollbar strip
# Version 2.6.1 - artwork falls back to the folder picture
# Version 2.6.0 - library is a folder grid with cover tiles
# Version 2.5.1 - library rows show song titles, not filenames
# Version 2.5.0 - shuffle and repeat, + button moved to library panel
# Version 2.4.2 - flac picker fix, duplicate double-click removed
# Version 2.4.1 - bigger title on its own row
# Version 2.4.0 - library panes slide animation
# Version 2.3.2 - title centered, last letter clipping fixed
# Version 2.3.1 - bar on its own row, bookend buttons, title fixes
# Version 2.3.0 - layout polish: centered bigger artwork, buttons on own row
# Version 2.2.0 - progress dialog when adding albums
# Version 2.1.0 - play/pause face flip, real artwork, loader picture-file fix
# Version 2.0.0 - progress bar, scrolling title, back and forward, double-click to play
# Version 1.9.0 - library panel beside the main window, play buttons on the bottom
# Version 1.8.1 - fixed the loose song crash
# Version 1.8.0 - play whole albums with the queue
# Version 1.7.0 - playback: play, pause and stop
# Version 1.6.0 - remove songs and albums from the library
# Version 1.5.0 - add songs and albums with + button
# Version 1.4.1 - button sizes and alignment fixed
# Version 1.4.0 - library window, artwork panel, collapsible albums
# Version 1.3.0 - library loading with albums
# Version 1.2.1 - library buttons smaller, lower, and to the right
# Version 1.2.0 - symobl buttons, added back and forward
# Version 1.1.0 - added the list, buttons and sound bar
# Version 1.0.0 - started SongDeck


import sys
import os
import shutil
import random
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QPushButton, QLabel, QSlider, QFileDialog, QMessageBox, QProgressDialog
from PySide6.QtCore import Qt, QUrl, QTimer, QSize, QObject, QEvent
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData, QMediaDevices
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QListWidget, QStackedWidget, QListWidgetItem, QToolButton
from PySide6.QtGui import QIcon
if os.environ.get("XDG_SESSION_TYPE") == "wayland":
    os.environ["QT_QPA_PLATFORM"] = "xcb"

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("BoomBox")
window.resize(500, 530)
folder = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, "frozen", False):
    folder = os.path.dirname(sys.executable)
library = os.path.join(folder, "music")
home_art = QPixmap(os.path.join(folder, "boombox-icon.png")).scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)
window.setWindowIcon(QIcon(home_art))
no_art = QPixmap(os.path.join(folder, "no-artwork-textured.png")).scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)
central = QWidget()
window.setCentralWidget(central)
layout = QHBoxLayout()
central.setLayout(layout)
main_widget = QWidget()
main_widget.setFixedWidth(478)
main_layout = QVBoxLayout()
main_layout.setContentsMargins(0, 0, 0, 0)
main_widget.setLayout(main_layout)
layout.addWidget(main_widget)
top_row = QHBoxLayout()
top_row.addStretch()
main_layout.addLayout(top_row)
art_label = QLabel("No artwork")
art_label.setAlignment(Qt.AlignCenter)
art_label.setFixedSize(360, 360)
art_label.setStyleSheet("border: 2px solid grey;")
art_label.setPixmap(home_art)
back_label = QLabel("<span style='font-size: 26px; font-weight: bold;'>BoomBox</span><br><br>Plays the albums on your PC. No accounts, no cloud, no internet.<br><br>Made by SmokeyVibez")
back_label.setAlignment(Qt.AlignCenter)
back_label.setWordWrap(True)
back_label.setStyleSheet("border: 2px solid grey;")
art_stack = QStackedWidget()
art_stack.setFixedSize(360,360)
art_stack.addWidget(art_label)
art_stack.addWidget(back_label)
info_label = QLabel()
info_label.setAlignment(Qt.AlignCenter)
info_label.setWordWrap(True)
info_label.setStyleSheet("border: 2px solid grey;")
art_stack.addWidget(info_label)
top_row.addWidget(art_stack)
top_row.addStretch()
back_button = QPushButton("⏮")
back_button.setFixedWidth(90)
play_button = QPushButton("▶")
play_button.setFixedWidth(90)
forward_button = QPushButton("⏭")
forward_button.setFixedWidth(90)
stop_button = QPushButton("⏹")
stop_button.setFixedWidth(90)
play_icon = QIcon.fromTheme("media-playback-start")
pause_icon = QIcon.fromTheme("media-playback-pause")
back_button.setIcon(QIcon.fromTheme("media-skip-backward"))
forward_button.setIcon(QIcon.fromTheme("media-skip-forward"))
stop_button.setIcon(QIcon.fromTheme("media-playback-stop"))
back_button.setIconSize(QSize(22, 22))
play_button.setIconSize(QSize(22, 22))
forward_button.setIconSize(QSize(22, 22))
stop_button.setIconSize(QSize(22, 22))
if not back_button.icon().isNull():
    back_button.setText("")
if not forward_button.icon().isNull():
    forward_button.setText("")
if not stop_button.icon().isNull():
    stop_button.setText("")
def set_play_face(playing):
    if playing:
        if not pause_icon.isNull():
            play_button.setIcon(pause_icon)
            play_button.setText("")
        else:
            play_button.setText("⏸")
    else:
        if not play_icon.isNull():
            play_button.setIcon(play_icon)
            play_button.setText("")
        else:
            play_button.setText("▶")
set_play_face(False)
shuffle_button = QPushButton("⇄")
repeat_button = QPushButton("↻")
shuffle_button.setFixedWidth (55)
repeat_button.setFixedWidth(55)
shuffle_button.setCheckable(True)
repeat_button.setCheckable(True)
library_button = QPushButton("Library")
library_button.setFixedWidth(100)
add_button = QPushButton("+")
add_button.setFixedWidth(40)
remove_button = QPushButton("-")
remove_button.setFixedWidth(40)
play_all_button = QPushButton("Play All")
play_all_button.setFixedWidth(80)
about_button = QToolButton()
about_button.setIcon(QIcon.fromTheme("dialog-information"))
if about_button.icon().isNull():
    about_button.setText("i")
about_button.setIconSize(QSize(22, 22))
about_button.setAutoRaise(True)
about_button.setFixedSize(28, 28)
button_row = QHBoxLayout()
main_layout.addLayout(button_row)
button_row.addWidget(shuffle_button)
button_row.addWidget(repeat_button)
button_row.addStretch()
button_row.addWidget(library_button)
bottom_row = QHBoxLayout()
main_layout.addLayout(bottom_row)
now_playing = QLabel("Nothing Playing")
now_playing.setAlignment(Qt.AlignCenter)
now_playing.setFixedWidth(470)
now_playing.setFixedHeight(20)
bottom_row.addWidget(now_playing)
sound_bar = QSlider(Qt.Horizontal)
bar_row = QHBoxLayout()
main_layout.addLayout(bar_row)
bar_row.addWidget(sound_bar)
time_label = QLabel("0:00")
bar_row.addWidget(time_label)
control_row = QHBoxLayout()
main_layout.addLayout(control_row)
control_row.addWidget(about_button)
control_row.addStretch()
control_row.addWidget(back_button)
control_row.addWidget(play_button)
control_row.addWidget(forward_button)
control_row.addWidget(stop_button)
control_row.addStretch()
right_spacer = QWidget()
right_spacer.setFixedWidth(28)
control_row.addWidget(right_spacer)
audio_output = QAudioOutput()
player = QMediaPlayer()
player.setAudioOutput(audio_output)
def follow_device():
    audio_output.setDevice(QMediaDevices.defaultAudioOutput())
device_watcher = QMediaDevices()
device_watcher.audioOutputsChanged.connect(follow_device)
queue = []
queue_index = 0
title_text = ""
title_offset = 0
title_timer = QTimer()
slide_timer = QTimer()
slide_step = 0
slide_target = 0
flip_timer = QTimer()
flip_step = 0
flip_target = None
repeat_mode = 0
library_panel = QWidget()
library_panel.setFixedSize(300, 530)
library_layout = QVBoxLayout()
library_panel.setLayout(library_layout)
panel_back = QPushButton("← Folders")
panel_back.hide()
library_layout.addWidget(panel_back, alignment=Qt.AlignLeft)
for button in [back_button, play_button, forward_button, stop_button, shuffle_button, repeat_button, library_button, add_button, play_all_button,remove_button, about_button, panel_back]:
    button.setFocusPolicy(Qt.NoFocus)
faces = QStackedWidget()
library_layout.addWidget(faces)
grid_list = QListWidget()
grid_list.setViewMode(QListWidget.IconMode)
grid_list.setIconSize(QSize(80, 80))
grid_list.setGridSize(QSize(86, 105))
grid_list.setResizeMode(QListWidget.Adjust)
grid_list.setMovement(QListWidget.Static)
grid_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
faces.addWidget(grid_list)
album_songs = QListWidget()
faces.addWidget(album_songs)
class GridFit(QObject):
    def eventFilter(self, watched, event):
        if event.type() == QEvent.Resize:
            width = grid_list.viewport().width() // 3
            if width >= 86:
                grid_list.setGridSize(QSize(width, 105))
        return False
grid_fit = GridFit()
grid_list.viewport().installEventFilter(grid_fit)
class ArtFlip(QObject):
    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonDblClick:
            flip_art()
        return False
art_flip = ArtFlip()
art_label.installEventFilter(art_flip)
back_label.installEventFilter(art_flip)
info_label.installEventFilter(art_flip)
def find_cover(path):
    files = sorted(os.listdir(path))
    for want in ("folder.jpg", "cover.jpg", "folder.png", "cover.png", "front.jpg"):
        for file in files :
            if file.lower() == want:
                return os.path.join(path, file)
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            return os.path.join(path, file)
    return None
def fill_grid():
    grid_list.setWordWrap(True)
    grid_list.clear()
    for name, path, songs in library_data:
        tile = QListWidgetItem(name)
        cover = find_cover(path)
        if cover is not None:
            tile.setIcon(QIcon(cover))
        else:
            tile.setIcon(QIcon.fromTheme("folder"))
        grid_list.addItem(tile)
    if loose_songs:
        tile = QListWidgetItem("Loose Songs")
        tile.setIcon(QIcon.fromTheme("folder"))
        grid_list.addItem(tile)
open_album = -1
delete_mode = False
def album_opened(item):
    global open_album
    if delete_mode:
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        return
    row = grid_list.row(item)
    album_songs.clear()
    if row < len(library_data):
       open_album = row
       name, path, songs = library_data[row]
    else:
        open_album = -1
        songs = loose_songs
    for song_path, title in songs:
        album_songs.addItem(title)
    open_timer.start(300)
grid_list.itemClicked.connect(album_opened)
open_timer = QTimer()
open_timer.setSingleShot(True)
def open_face():
    faces.setCurrentWidget(album_songs)
    panel_back.show()
open_timer.timeout.connect(open_face)
def album_double_clicked(item):
    global queue_index
    if delete_mode:
        return
    open_timer.stop()
    row = grid_list.row(item)
    queue.clear()
    if row < len(library_data):
        queue.extend(library_data[row][2])
    else:
        queue.extend(loose_songs)
    queue_index = 0
    if queue:
        play_queue_song()
grid_list.itemDoubleClicked.connect(album_double_clicked)
def back_to_grid():
    faces.setCurrentWidget(grid_list)
    panel_back.hide()
panel_back.clicked.connect(back_to_grid)
def album_song_double_clicked(item):
    player.stop()
    play_clicked()
album_songs.itemDoubleClicked.connect(album_song_double_clicked)
panel_button_row = QHBoxLayout()
library_layout.addLayout(panel_button_row)
panel_button_row.addWidget(play_all_button)
panel_button_row.addStretch()
panel_button_row.addWidget(add_button)
panel_button_row.addWidget(remove_button)
panel_clip = QWidget()
panel_clip.setFixedWidth(0)
layout.addWidget(panel_clip)
layout.addStretch()
library_panel.setParent(panel_clip)
panel_clip.hide()
def clean_name(file):
    name = os.path.splitext(file)[0]
    parts = name.split(" - ")
    if len(parts) >= 3:
        name = parts[-1]
    elif len(parts) == 2:
        name = parts[1]
    elif len(parts) == 1 and "-" in name:
        chunks = name.split("-")
        if len(chunks) >= 3 and "x" in chunks[1]:
            name = "-".join(chunks[2:]).replace("_", " ")
    elif len(parts) == 1 and "." in name:
        chunks = name.split(".", 1)
        if chunks[0].isdigit():
            name = chunks[1]
    return name
library_data = []
loose_songs = []
def load_library_data():
    global library_data, loose_songs
    library_data = []
    loose_songs = []
    for name in sorted(os.listdir(library)):
        path = os.path.join(library, name)
        if os.path.isdir(path):
            songs = []
            for root, dirs, files in os.walk(path):
                for file in sorted(files):
                    if file.lower().endswith((".mp3", ".flac", ".ogg", ".wav", ".m4a")):
                        songs.append((os.path.join(root, file), clean_name(file)))
            library_data.append((name, path, songs))
        elif name.lower().endswith((".mp3", ".flac", ".ogg", ".wav", ".m4a")):
            loose_songs.append((path, clean_name(name)))
load_library_data()
os.makedirs(library, exist_ok=True)
fill_grid()
def add_songs():
    picked, _ = QFileDialog.getOpenFileNames(
        window, "Add Songs", "", "Music (*.mp3 *.flac *.ogg *.wav *.m4a)")
    for pick in picked:
        shutil.copy(pick, library)
    load_library_data()
    fill_grid()
def refresh_library():
    old_data = library_data
    old_loose = loose_songs
    old_covers = []
    for name, path, songs in old_data:
        old_covers.append(find_cover(path))
    load_library_data()
    new_covers = []
    for name, path, songs in library_data:
        new_covers.append(find_cover(path))
    if library_data != old_data or loose_songs != old_loose or new_covers != old_covers:
        fill_grid()
def toggle_library():
    global slide_target
    if slide_target == 0:
        slide_target = 10
        panel_clip.show()
        library_panel.show()
        left = window.x()
        top = window.y()
        window.setFixedSize(806, 530)
        window.move(left, top)
        if delete_mode ==False:
           refresh_library()
    else:
        slide_target = 0
    slide_timer.start(15)
def add_album():
    picked = QFileDialog.getExistingDirectory(window, "Add Album")
    if picked:
        target = os.path.join(library, os.path.basename(picked))
        total = 0
        for root, dirs, files in os.walk(picked):
            total = total + len(files)
        progress = QProgressDialog("Adding album...", None, 0, total, window)
        progress.setWindowTitle("Adding")
        progress.setMinimumDuration(0)
        progress.show()
        app.processEvents()
        done_count = 0
        for root, dirs, files in os.walk(picked):
            for file in files:
                source = os.path.join(root, file)
                rel = os.path.relpath(source, picked)
                dest = os.path.join(target, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy(source, dest)
                done_count = done_count + 1
                progress.setValue(done_count)
                app.processEvents()
        progress.setValue(total)
        load_library_data()
        fill_grid()
def add_clicked():
    box = QMessageBox(window)
    box.setWindowTitle("Add")
    box.setText("Add songs or album?")
    songs_button = box.addButton("Songs", QMessageBox.ActionRole)
    album_button = box.addButton("Album", QMessageBox.ActionRole)
    box.addButton("Cancel", QMessageBox.RejectRole)
    box.exec()
    if box.clickedButton() == songs_button:
        add_songs()
    elif box.clickedButton() == album_button:
        add_album()
add_button.clicked.connect(add_clicked)
def grid_minus():
    global delete_mode
    if not delete_mode:
        delete_mode = True
        remove_button.setText("✓")
        for row in range(len(library_data)):
            tile = grid_list.item(row)
            tile.setFlags(tile.flags() | Qt.ItemIsUserCheckable)
            tile.setCheckState(Qt.Unchecked)
        return
    picked = []
    for row in range(len(library_data)):
        if grid_list.item(row).checkState() ==Qt.Checked:
            picked.append(row)
    delete_mode = False
    remove_button.setText("-")
    if not picked:
        fill_grid()
        return
    names = ""
    for row in picked:
        if names:
            names = names + ", "
        names= names + library_data[row][0]
    box = QMessageBox(window)
    box.setWindowTitle("Remove")
    box.setText("Remove " + names + "?")
    yes_button = box.addButton("Remove", QMessageBox.AcceptRole)
    box.addButton("Cancel", QMessageBox.RejectRole)
    box.exec()
    if box.clickedButton() == yes_button:
        for row in picked:
            shutil.rmtree(library_data[row][1])
    load_library_data()
    fill_grid()
def remove_clicked():
    if faces.currentWidget() == grid_list:
        grid_minus()
        return
    else:
        row = album_songs.currentRow()
        if row < 0 and open_album >= 0:
            name = library_data[open_album][0]
            path = library_data[open_album][1]
        elif row < 0:
            return
        elif open_album >= 0:
            name = library_data[open_album][2][row][1]
            path = library_data[open_album][2][row][0]
        else:
            name = loose_songs[row][1]
            path = loose_songs[row][0]
    box = QMessageBox(window)
    box.setWindowTitle("Remove")
    box.setText("Remove " + name + "?")
    yes_button = box.addButton("Remove", QMessageBox.AcceptRole)
    box.addButton("Cancel", QMessageBox.RejectRole)
    box.exec()
    if box.clickedButton() == yes_button:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        load_library_data()
        fill_grid()
        faces.setCurrentWidget(grid_list)
        panel_back.hide()
remove_button.clicked.connect(remove_clicked)
def play_clicked():
    global queue_index
    if player.playbackState() == QMediaPlayer.PlayingState:
        player.pause()
        set_play_face(False)
        return
    if player.playbackState() == QMediaPlayer.PausedState:
        player.play()
        set_play_face(True)
        return
    if faces.currentWidget() == grid_list:
        row = grid_list.currentRow()
        if row < 0:
            return
        queue.clear()
        if row < len(library_data):
            queue.extend(library_data[row][2])
        else:
            queue.extend(loose_songs)
        queue_index = 0
    else:
        row = album_songs.currentRow()
        if row < 0:
            return
        queue.clear()
        if open_album >= 0:
            queue.extend(library_data[open_album][2])
            queue_index = row
        else:
            queue.append(loose_songs[row])
            queue_index = 0
    if queue:
        play_queue_song()
def stop_clicked():
    global title_text, title_offset
    player.stop()
    player.setSource(QUrl())
    set_play_face(False)
    now_playing.setText("Nothing playing")
    window.setWindowTitle("BoomBox")
    art_label.setPixmap(home_art)
    title_text = "Nothing playing"
    title_offset = 0
def play_queue_song():
    global title_text, title_offset
    path, name = queue[queue_index]
    player.setSource(QUrl.fromLocalFile(path))
    player.play()
    set_play_face(True)
    now_playing.setText(name)
    window.setWindowTitle(name)
    title_text = name
    title_offset = 0
def play_next(status):
    global queue_index
    if status != QMediaPlayer.EndOfMedia:
        return
    if repeat_mode == 2:
        play_queue_song()
    elif shuffle_button.isChecked() and len(queue) > 1:
        pick = queue_index
        while pick == queue_index:
            pick = random.randrange(len(queue))
        queue_index = pick
        play_queue_song()
    elif queue_index + 1 < len(queue):
        queue_index = queue_index + 1
        play_queue_song()
    elif repeat_mode ==1 and len(queue) > 0:
        queue_index = 0
        play_queue_song()
    else:
        set_play_face(False)
play_button.clicked.connect(play_clicked)
stop_button.clicked.connect(stop_clicked)
player.mediaStatusChanged.connect(play_next)
library_button.clicked.connect(toggle_library)
def play_all():
    global queue_index
    queue.clear()
    for album in library_data:
        queue.extend(album[2])
    queue.extend(loose_songs)
    random.shuffle(queue)
    queue_index = 0
    if queue:
        play_queue_song()
play_all_button.clicked.connect(play_all)
def flip_art():
    if art_stack.currentWidget() == art_label:
        flip_to(back_label)
    else:
        flip_to(art_label)
def flip_to(page):
    global flip_target
    flip_target = page
    if flip_step ==0:
        flip_timer.start(15)
def flip_tick():
    global flip_step
    flip_step = flip_step + 1
    if flip_step < 6:
        art_stack.setFixedWidth(360 - flip_step * 60)
    elif flip_step == 6:
        art_stack.setFixedWidth(0)
        art_stack.setCurrentWidget(flip_target)
    elif flip_step < 12:
        art_stack.setFixedWidth((flip_step - 6) * 60)
    else:
        art_stack.setFixedWidth(360)
        flip_timer.stop()
        flip_step = 0
flip_timer.timeout.connect(flip_tick)
def info_text():
    data = player.metaData()
    fields = []
    fields.append(("Title", QMediaMetaData.Title))
    fields.append(("Artist", QMediaMetaData.AlbumArtist))
    fields.append(("Album", QMediaMetaData.AlbumTitle))
    fields.append(("Genre", QMediaMetaData.Genre))
    fields.append(("Track", QMediaMetaData.TrackNumber))
    fields.append(("Year", QMediaMetaData.Date))
    lines = []
    for label, key in fields:
        value = data.value(key)
        if value:
            if type(value) == list:
                value = ", ".join(value)
            lines.append(label + ": " + str(value))
    bitrate = data.value(QMediaMetaData.AudioBitRate)
    if bitrate:
        lines.append("Bitrate: " + str(bitrate // 1000) + " kbps")
    if lines:
        text = "\n".join(lines)
    else:
        text = "Nothing playing"
    return text
def info_clicked():
    info_label.setText(info_text())
    if art_stack.currentWidget() == info_label:
        flip_to(art_label)
    else:
        flip_to(info_label)
def refresh_info():
    if art_stack.currentWidget() == info_label:
        info_label.setText(info_text())
player.metaDataChanged.connect(refresh_info)
about_button.clicked.connect(info_clicked)
def format_time(ms):
    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return str(minutes) + ":" + str(seconds).zfill(2)
def set_bar_range(duration):
    sound_bar.setMaximum(duration)
def move_bar(position):
    sound_bar.setValue(position)
    time_label.setText(format_time(position))
player.durationChanged.connect(set_bar_range)
player.positionChanged.connect(move_bar)
sound_bar.sliderMoved.connect(player.setPosition)
def scroll_title():
    global title_offset
    if len(title_text) <= 45:
        return
    padded = title_text + " "
    title_offset = title_offset + 1
    if title_offset >= len(padded):
        title_offset = 0
    now_playing.setText((padded + padded)[title_offset:title_offset + 45])
title_timer.timeout.connect(scroll_title)
title_timer.start(250)
def slide_tick():
    global slide_step
    if slide_step < slide_target:
        slide_step = slide_step + 1
    elif slide_step > slide_target:
        slide_step = slide_step - 1
    panel_clip.setFixedWidth(slide_step * 30)
    if slide_step == slide_target:
        library_panel.setFixedHeight(panel_clip.height())
        slide_timer.stop()
        if slide_step == 0:
            panel_clip.hide()
            left = window.x()
            top = window.y()
            window.setFixedSize(500, 530)
            window.move(left, top)
slide_timer.timeout.connect(slide_tick)
def show_art():
    image = player.metaData().value(QMediaMetaData.CoverArtImage)
    if image is None:
        image = player.metaData().value(QMediaMetaData.ThumbnailImage)
    if image is None or image.isNull():
        path = player.source().toLocalFile()
        if path == "":
            return
        folder = os.path.dirname(path)
        cover = find_cover(folder)
        while cover is None and folder != library:
            folder = os.path.dirname(folder)
            cover = find_cover(folder)
        if cover is not None:
            art_label.setPixmap(QPixmap(cover).scaled(360, 360, Qt.KeepAspectRatio))
        else:
            art_label.setPixmap(no_art)
    else:
        picture = QPixmap.fromImage(image)
        art_label.setPixmap(picture.scaled(360, 360, Qt.KeepAspectRatio))
player.metaDataChanged.connect(show_art)
def forward_clicked():
    global queue_index
    if shuffle_button.isChecked() and len(queue) > 1:
        pick = queue_index
        while pick == queue_index:
            pick = random.randrange(len(queue))
        queue_index = pick
        play_queue_song()
        return
    if queue_index + 1 < len(queue):
        queue_index = queue_index + 1
        play_queue_song()
    elif repeat_mode == 1 and len(queue) > 0:
        queue_index = 0
        play_queue_song()
forward_button.clicked.connect(forward_clicked)
def back_clicked():
    global queue_index
    if player.position() > 3000:
        player.setPosition(0)
    elif queue_index > 0:
        queue_index = queue_index - 1
        play_queue_song()
back_button.clicked.connect(back_clicked)
def repeat_clicked():
    global repeat_mode
    repeat_mode = repeat_mode + 1
    if repeat_mode > 2:
        repeat_mode = 0
    if repeat_mode == 0:
        repeat_button.setChecked(False)
        repeat_button.setText("↻")
    elif repeat_mode == 1:
        repeat_button.setChecked(True)
        repeat_button.setText("↻")
    else:
        repeat_button.setChecked(True)
        repeat_button.setText("↻1")
repeat_button.clicked.connect(repeat_clicked)
window.show()
app.exec()
