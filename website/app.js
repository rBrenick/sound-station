// triggered from button in index.html
// triggers function in start_server.py
function playVideo() {
    fetch('/play-video?' + new URLSearchParams({
        'target_url': document.getElementById("video-url").value
    }))
        .then(response => response.json())
        .then(refreshView())
        .catch(error => console.error(error));
}

function addToQueue() {
    addUrlToQueue(document.getElementById("video-url").value)
}

function addUrlToQueue(url) {
    fetch('/add-queue?' + new URLSearchParams({
        'target_url': url
    }))
        .then(response => response.json())
        .then(refreshView())
        .catch(error => console.error(error));
}

function removeFromQueue(index) {
    fetch('/remove-from-queue?' + new URLSearchParams({
        'queue_index': index
    }))
        .then(response => response.json())
        .then(refreshView())
        .catch(error => console.error(error));
}

function clearList(listElement) {
    while (listElement.firstChild) {
        listElement.removeChild(listElement.lastChild);
    }
}

function parseQueue(queueData) {
    console.log("refreshing queue...");
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
    console.log("refreshing history...");
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
    console.log("refreshing title...");
    title_element = document.getElementById("current-video-title");
    if (titleData == ""){
        titleData = "Unknown"
    }
    title_element.innerHTML = titleData;
}

function refreshView() {
    fetch('./queue-list', {})
        .then((response) => response.json())
        .then((json) => parseQueue(json));
        
    fetch('./history-list', {})
        .then((response) => response.json())
        .then((json) => parseHistory(json));
        
    fetch('./current-video-title', {})
        .then((response) => response.json())
        .then((json) => parseTitle(json));
}

function runFunction() {
    fetch('/function-name')
        .then(response => response.json())
        .catch(error => console.error(error));
}

refreshView()
