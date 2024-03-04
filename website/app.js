// triggered from button in index.html
// triggers function in start_server.py
function playVideoFromURL() {
    fetch('/play-video-from-url?' + new URLSearchParams({
        'target_url': document.getElementById("video-url").value
    }))
        .then(refreshView())
        .catch(error => console.error(error));
}

function addToQueue() {
    addUrlToQueue(document.getElementById("video-url").value)
}

function addUrlToQueue(url) {
    fetch('/add-to-queue?' + new URLSearchParams({
        'target_url': url
    }))
        .then(refreshView())
        .catch(error => console.error(error));
}

function removeFromQueue(index) {
    fetch('/remove-from-queue?' + new URLSearchParams({
        'queue_index': index
    }))
        .then(refreshView())
        .catch(error => console.error(error));
}

function clearList(listElement) {
    while (listElement.firstChild) {
        listElement.removeChild(listElement.lastChild);
    }
}

function parseQueue(queueData) {
    clearList(document.getElementById("queue-list"));
    
    if (Object.keys(queueData).length == 0) {
        list_element = document.getElementById("queue-list");
        empty_indicator = document.createElement('p');
        empty_indicator.innerHTML = "[Empty]"
        list_element.appendChild(empty_indicator);
    }
    
    for (const [index, asset_info] of Object.entries(queueData)) {
        list_element = document.getElementById("queue-list");
        asset_div = document.createElement("div");
        asset_div.style = "display: flex; padding-bottom:20px;"
        list_element.appendChild(asset_div);
        
        button = document.createElement('button');
        button.innerHTML = "x";
        button.onclick = function () {
            removeFromQueue(index);
        };
        asset_div.appendChild(button);
        
        url_link = document.createElement('a');
        url_link.href = asset_info["url"];
        url_link.innerHTML = asset_info["title"];
        asset_div.appendChild(url_link);
    }
}

function parseHistory(historyData) {
    
    clearList(document.getElementById("history-list"));
    
    if (Object.keys(historyData).length == 0) {
        list_element = document.getElementById("history-list");
        empty_indicator = document.createElement('p');
        empty_indicator.innerHTML = "[Empty]"
        list_element.appendChild(empty_indicator);
    }
    
    for (const [index, asset_info] of Object.entries(historyData)) {
        
        list_element = document.getElementById("history-list");

        asset_div = document.createElement("div");
        asset_div.style = "display: flex; padding-bottom:20px;"
        list_element.appendChild(asset_div);
        
        button = document.createElement('button');
        button.innerHTML = "+";
        button.onclick = function () {
            addUrlToQueue(asset_info["url"]);
        };
        asset_div.appendChild(button);
        
        url_link = document.createElement('a');
        url_link.href = asset_info["url"];
        url_link.innerHTML = asset_info["title"];
        asset_div.appendChild(url_link);
    }
}

function parseTitle(titleData) {
    title_element = document.getElementById("current-video-title");
    title_element.innerHTML = titleData;
}

function setVolumeSlider(volumeValue) {
    volume_slider = document.getElementById("volumeSlider");
    volume_slider.value = volumeValue;
}

function refreshView() {
    console.log("refreshing view...");
    
    fetch('./queue-list', {})
        .then((response) => response.json())
        .then((json) => parseQueue(json));
    
    fetch('./history-list', {})
        .then((response) => response.json())
        .then((json) => parseHistory(json));
    
    fetch('./current-video-title', {})
        .then((response) => response.json())
        .then((json) => parseTitle(json));
        
    fetch('./get-volume', {})
        .then((response) => response.json())
        .then((json) => setVolumeSlider(json));
}

function pauseVideo() {
    fetch('/pause-video')
        .catch(error => console.error(error));
}

function playVideo() {
    fetch('/play-video')
        .catch(error => console.error(error));
}

refreshView()

// Connect volume slider
function updateVolume(newValue) {
    fetch('/set-volume?' + new URLSearchParams({
        'value': newValue
    }))
        .catch(error => console.error(error));
}

volume_slider = document.getElementById("volumeSlider");
volume_slider.oninput = function() {
  updateVolume(this.value);
}

