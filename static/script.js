let intervalId;

async function sendImage() {
    const video = document.querySelector('video');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    const dataUrl = canvas.toDataURL('image/jpeg');
    const blob = await fetch(dataUrl).then(res => res.blob());

    const formData = new FormData();
    formData.append('image', blob, 'image.jpg');

    const response = await fetch('/gaze', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();

    const resultText = `Gaze Direction: ${result.gaze_direction}`;
    document.getElementById('result').innerText = resultText;

    if (result.alert) {
        alert('You are out of the screen!');
    }
}

function startVideo() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            document.querySelector('video').srcObject = stream;
            intervalId = setInterval(sendImage, 1000);  // Capture and send frame every 1 second
        })
        .catch(error => {
            console.error('Error accessing webcam:', error);
        });
}

function stopVideo() {
    clearInterval(intervalId);
    const video = document.querySelector('video');
    video.srcObject.getTracks().forEach(track => track.stop());
}

function submitAnswer() {
    const form = document.getElementById('mcqForm');
    const formData = new FormData(form);
    fetch('/submit_answer', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('result').innerText = `Answer Submitted: ${result.message}`;
    })
    .catch(error => {
        console.error('Error submitting answer:', error);
    });
}

// Enter full-screen mode
function goFullScreen() {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) { // Firefox
        elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) { // Chrome, Safari and Opera
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { // IE/Edge
        elem.msRequestFullscreen();
    }
}

// Detect exit from full-screen mode
function onFullScreenChange() {
    if (!document.fullscreenElement) {
        alert('Please stay in full-screen mode!');
        goFullScreen();  // Optional: Force full-screen mode again
    }
}

window.onload = function() {
    startVideo();
    
    // Add event listeners for detecting full-screen changes
    document.addEventListener('fullscreenchange', onFullScreenChange);
    document.addEventListener('mozfullscreenchange', onFullScreenChange);
    document.addEventListener('webkitfullscreenchange', onFullScreenChange);
    document.addEventListener('msfullscreenchange', onFullScreenChange);
}

document.getElementById('fullScreenButton').addEventListener('click', goFullScreen);
document.getElementById('stopButton').addEventListener('click', stopVideo);
