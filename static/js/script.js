var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function(){
    console.log("Connected to Server");
    document.getElementById("connectionStatus").innerText = "Connected";
});

socket.on('disconnect', function(){
    console.log("Disconnected from Server");
    document.getElementById("connectionStatus").innerText = "Disconnected";
});

function logToContainer(message) {
    var logContainer = document.getElementById("logContainer");
    var logMessage = document.createElement("div");
    logMessage.innerText = message;
    logContainer.appendChild(logMessage);
    logContainer.scrollTop = logContainer.scrollHeight; 
}

socket.on('new_python_job', function(job){ 
    notify(job , "Python");
    reloadPage();
    var jobList = document.getElementById('job-list');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Python Job: " + job.title);
});

socket.on('new_react_job', function(job){ 
    notify(job , "React");
    reloadPage();
    var jobList = document.getElementById('reactJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New React Job: " + job.title);
});
socket.on('new_us_job', function(job){ 
    notify(job , "us");
    reloadPage();
    var jobList = document.getElementById('us_Jobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New US Job: " + job.title);
});

socket.on('new_node_job', function(job){ 
    notify(job, "node");
    reloadPage();
    var jobList = document.getElementById('nodeJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Node Job: " + job.title);
});

socket.on('new_php_job', function(job){ 
    notify(job , "php");
    reloadPage();
    var jobList = document.getElementById('phpJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New PHP Job: " + job.title);
});

socket.on('new_wordpress_job', function(job){ 
    notify(job, "wordpress");
    reloadPage();
    var jobList = document.getElementById('wordpressJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New WordPress Job: " + job.title);
});

socket.on('new_quickbooks_job', function(job){ 
    notify(job , "quickbooks");
    reloadPage();
    var jobList = document.getElementById('quickbooksJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New QuickBook Job: " + job.title);
});

socket.on('new_shopify_job', function(job){ 
    notify(job , "shopify");
    reloadPage();
    var jobList = document.getElementById('shopifyJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Shopify Job: " + job.title);
});

socket.on('new_api_integration_job', function(job) {
    notify(job , "api_integration");
    reloadPage();
    var jobList = document.getElementById('apiIntegrationJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New API Integration Job: " + job.title);
});

socket.on('new_payment_gateway_job', function(job) {
    notify(job, "payment_gatewy");
    reloadPage();
    var jobList = document.getElementById('paymentGatewayJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Payment Gateway Job: " + job.title);
});

socket.on('new_full_time_job', function(job) {
    notify(job , "full_time_job");
    reloadPage();
    var jobList = document.getElementById('fullTimeJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Full-Time Job: " + job.title);
});

socket.on('new_chatbot_job', function(job){ 
    notify(job, "chatbot");
    reloadPage();
    var jobList = document.getElementById('chatbotJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Shopify Job: " + job.title);
});

socket.on('new_scripting_job', function(job){ 
    notify(job, "scripting");
    reloadPage();
    var jobList = document.getElementById('scriptingJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Shopify Job: " + job.title);
});
socket.on('new_bubble_job', function(job){ 
    notify(job , "bubble");
    reloadPage();
    var jobList = document.getElementById('bubbleJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Shopify Job: " + job.title);
});

socket.on('new_webrtc_job', function(job){ 
    notify(job , "webrtc");
    reloadPage();
    var jobList = document.getElementById('webrtcJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Shopify Job: " + job.title);
});
socket.on('new_vue_job', function(job){ 
    notify(job,"vue_job");
    reloadPage();
    var jobList = document.getElementById('vueJobs');
    var jobItem = document.createElement('div');
    jobItem.classList.add('job-item');
    jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
    jobList.insertBefore(jobItem, jobList.firstChild);
    displayNotification("New Shopify Job: " + job.title);
});

function markAsClicked(link){
    link.classList.add('clicked');
    NotificationCount = 0;
    document.title = "Job Finder"
}

if ("Notification" in window){
    if (Notification.permission ==='granted'){
        notify();
    } else {
        Notification.requestPermission().then((res) => {
            if (res === 'granted'){
                notify();
            } else if (res ==='denied'){
                console.log('Permission denied');
            } else if (res ==="default")
            console.log("notification permision not given ")
        })
    }
} else {
    console.log("Notification not supported");
}

var NotificationCount = 0
function notify(job,category) {
    if (Notification.permission === 'granted' && job) {
        var notification = new Notification("New"+ category+ "Job", {
            body: "New Job: " + job.title,
        });

        NotificationCount ++;
        document.title = "(" + NotificationCount + ") Job Finder";

        var badge = document.getElementById(category + 'Count');
        if (badge){
            var currentCount = parseInt(badge.innerText, 10);
            badge.innerText = currentCount + 1;
        }
    }
}


function reloadPage(){
    setTimeout(function(){
        window.location.reload();
    }, 150000);
}

window.onload = function(){
    reloadPage();
} 

function showJobs(category) {
    var jobCategories = document.querySelectorAll('.main-content > div');
    jobCategories.forEach(function(categoryElement) {
        categoryElement.style.display = 'none';
    });

    var selectedCategory = document.getElementById(category + 'Jobs');
    if (selectedCategory) {
        var allJobs = selectedCategory.querySelectorAll('.job');
        var currentTime = new Date();
        var twentyFourHoursAgo = new Date(currentTime - 24 * 60 * 60 * 1000);

        allJobs.forEach(function(job) {
            var postedTime = new Date(job.dataset.postedTime);
            if (postedTime > twentyFourHoursAgo) {
                job.style.display = 'block';
            } else {
                job.style.display = 'none';
            }
        });

        selectedCategory.style.display = 'block';
        localStorage.setItem('selectedCategory', category);
    }
}


window.onload = function(){
    var selectedCategory = localStorage.getItem('selectedCategory');
    if (selectedCategory) {
        showJobs(selectedCategory);
    } else {
       
        showJobs('python'); 
    }
    reloadPage();
}

