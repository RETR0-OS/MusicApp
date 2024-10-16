// Create a new Audio object
let audio = new Audio();
let currentSongIndex = -1; // Initially, no song is playing
let isPlaying = false;
let isShuffle = false; // Shuffle mode disabled by default
let shuffledOrder = []; // To store the shuffled order of songs
const songItems = Array.from(document.querySelectorAll('.song-item')); // Store the original order of songs
let currentOrder = [...songItems]; // By default, the order is the original list

const playPauseButton = document.querySelector('.play-pause');
const prevTrackButton = document.querySelector('.prev-track');
const nextTrackButton = document.querySelector('.next-track');
const shuffleButton = document.querySelector('.shuffle-button'); // Shuffle button
const volumeSlider = document.getElementById('volume-control');
const songTitle = document.getElementById('current-song-title');
const seekBar = document.getElementById('seek-bar');
const currentTimeDisplay = document.getElementById('current-time');
const totalDurationDisplay = document.getElementById('total-duration');

// Shuffle the array of songs (but only shuffle once when shuffle is enabled)
function shuffleArray(array) {
    let shuffled = array.slice(); // Create a shallow copy
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Select a random song if no song is playing
function playRandomSong() {
    currentSongIndex = Math.floor(Math.random() * currentOrder.length); // Pick a random song from the current order
    playSongFromCurrentIndex();
}

// Toggle shuffle mode
shuffleButton.addEventListener('click', function() {
    isShuffle = !isShuffle; // Toggle shuffle mode
    if (isShuffle) {
        if (shuffledOrder.length === 0) {
            shuffledOrder = shuffleArray([...songItems]); // Shuffle the playlist (only shuffle once)
        }
        currentOrder = shuffledOrder; // Use the shuffled order
        shuffleButton.innerHTML = '➡️'; // Change icon to right arrow when shuffle is active
    } else {
        currentOrder = [...songItems]; // Reset to the original order
        shuffleButton.innerHTML = '🔀'; // Change icon back to shuffle when shuffle is inactive
    }

    if (currentSongIndex === -1) { // If no song is playing
        playRandomSong(); // Start with a random song
    } else {
        playSongFromCurrentIndex(); // Play the current song in the new order
    }
});

// Play the song based on the current index in the appropriate order
function playSongFromCurrentIndex() {
    const currentSong = currentOrder[currentSongIndex]; // Get the song from the current order
    const songSrc = currentSong.getAttribute('data-song');
    const songTitleText = currentSong.getAttribute('data-title');
    const artistText = currentSong.getAttribute('data-artist');
    playSong(songSrc, songTitleText, artistText); // Play the song
}

// Play the selected song
function playSong(songSrc, songTitleText, artistText) {
    audio.src = songSrc;
    audio.play();
    isPlaying = true;

    // Update the UI with the song title
    songTitle.textContent = songTitleText;

    // Change the play button to a pause button
    playPauseButton.textContent = '⏸';

    // Update the total duration of the song when metadata is loaded
    audio.addEventListener('loadedmetadata', function () {
        totalDurationDisplay.textContent = formatTime(audio.duration);
        seekBar.max = audio.duration;
    });

    // Update the seek bar and current time display as the song plays
    audio.addEventListener('timeupdate', function () {
        seekBar.value = audio.currentTime;
        currentTimeDisplay.textContent = formatTime(audio.currentTime);
    });

    // Autoplay the next song when the current one ends
    audio.addEventListener('ended', playNextTrack);
}

// Toggle play/pause
function togglePlayPause() {
    if (currentSongIndex === -1) {
        playRandomSong(); // Play a random song if none is playing
    } else if (isPlaying) {
        audio.pause();
        isPlaying = false;
        playPauseButton.textContent = '⏯'; // Play symbol
    } else {
        audio.play();
        isPlaying = true;
        playPauseButton.textContent = '⏸'; // Pause symbol
    }
}

// Set up event listeners for each song item
songItems.forEach((songItem, index) => {
    songItem.querySelector('.play-button').addEventListener('click', function() {
        currentSongIndex = currentOrder.indexOf(songItem); // Correctly find the song in the current order
        playSongFromCurrentIndex();
    });
});

// Play the next track (cyclically in the current order, whether shuffled or not)
function playNextTrack() {
    if (currentSongIndex === -1) { // If no song is playing
        playRandomSong(); // Start with a random song
    } else {
        currentSongIndex = (currentSongIndex + 1) % currentOrder.length; // Increment and loop back if necessary
        playSongFromCurrentIndex(); // Play the next song
    }
}

// Play the previous track (cyclically in the current order, whether shuffled or not)
function playPrevTrack() {
    if (currentSongIndex === -1) { // If no song is playing
        playRandomSong(); // Start with a random song
    } else {
        currentSongIndex = (currentSongIndex - 1 + currentOrder.length) % currentOrder.length; // Decrement and loop back if necessary
        playSongFromCurrentIndex(); // Play the previous song
    }
}

// Seek bar control (jump to a specific time in the song)
seekBar.addEventListener('input', function() {
    audio.currentTime = seekBar.value;
});

// Volume control
volumeSlider.addEventListener('input', function(e) {
    audio.volume = e.target.value / 100;
});

// Format time in MM:SS format
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}

// Attach event listeners to the control buttons
playPauseButton.addEventListener('click', togglePlayPause);
nextTrackButton.addEventListener('click', playNextTrack);
prevTrackButton.addEventListener('click', playPrevTrack);
