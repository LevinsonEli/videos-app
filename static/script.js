document.getElementById('create-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    fetch('/api/v1/videos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, description })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Video created:', data);
        fetchVideos(); // Refresh the video list
    })
    .catch(error => console.error('Error:', error));
});

function fetchVideos() {
    fetch('/api/v1/videos')
        .then(response => response.json())
        .then(videos => {
            const videoList = document.getElementById('video-list');
            videoList.innerHTML = '';
            videos.forEach(video => {
                const li = document.createElement('li');
                li.textContent = `Title: ${video.title}, Description: ${video.description}`;
                videoList.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
}

function updateVideo() {
    const id = document.getElementById('update-id').value;
    const title = document.getElementById('update-title').value;
    const description = document.getElementById('update-description').value;

    fetch(`/api/v1/videos/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, description })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Video updated:', data);
        fetchVideos(); // Refresh the video list
    })
    .catch(error => console.error('Error:', error));
}

function deleteVideo() {
    const id = document.getElementById('update-id').value;

    fetch(`/api/v1/videos/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Video deleted:', data);
        fetchVideos(); // Refresh the video list
    })
    .catch(error => console.error('Error:', error));
}

