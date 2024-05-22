var socket = io.connect('http://' + document.domain + ':' + location.port);

// Event listener for when the client connects to the server
socket.on('connect', function() {
    console.log("Connected to Server");
    document.getElementById("connectionStatus").innerText = "Connected";
});

// Event listener for when the client disconnects from the server
socket.on('disconnect', function() {
    console.log("Disconnected from Server");
    document.getElementById("connectionStatus").innerText = "Disconnected";
});

// Function to log messages to the container
function logToContainer(message) {
    var logContainer = document.getElementById("logContainer");
    var logMessage = document.createElement("div");
    logMessage.innerText = message;
    logContainer.appendChild(logMessage);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// Function to show jobs based on category
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

// Event listener for new job events from the server
// Event listener for new job events from the server
socket.on('new_job', function(data) {
    console.log("Received new job event with data:", data);

    // Ensure data and data.job are defined
    if (data && data.category && data.job) {
        console.log("Job category:", data.category);

        // Check if the job was posted within the last 24 hours
        var jobPostedTime = new Date(data.job.published);
        var currentTime = new Date();
        var twentyFourHoursAgo = new Date(currentTime - 24 * 60 * 60 * 1000);

        if (jobPostedTime > twentyFourHoursAgo) {
            // Check if this job has already been notified
            var notifiedJobs = JSON.parse(localStorage.getItem('notifiedJobs')) || {};
            if (!notifiedJobs[data.job.id]) {
                // Update job list
                var jobList = document.getElementById(data.category + 'Jobs');
                if (jobList) {
                    var jobItem = document.createElement('div');
                    jobItem.classList.add('job-item');
                    jobItem.innerHTML = '<a class="job-title" href="' + data.job.link + '" onclick="markAsClicked(this)" target="_blank">' + data.job.title + '</a><p class="job-published">Published: ' + data.job.published + '</p>';
                    jobList.insertBefore(jobItem, jobList.firstChild);
                } else {
                    console.error("Job list not found for category:", data.category);
                }

                // Notify the user about the new job
                notify(data.job, data.category);

                // Mark this job as notified
                notifiedJobs[data.job.id] = true;
                localStorage.setItem('notifiedJobs', JSON.stringify(notifiedJobs));
            } else {
                console.log("Job has already been notified, skipping...");
            }
        } else {
            console.log("Job is older than 24 hours, no notification sent.");
        }
    } else {
        console.error("Received job is undefined or missing category property");
        console.log("Data received:", data);
    }
});




function markAsClicked(link) {
    link.classList.add('clicked');
    NotificationCount = 0;
    document.title = "Job Finder";
}

if ("Notification" in window) {
    // Check if notification permission is granted
    if (Notification.permission === 'granted') {
        console.log('Notification permission granted');
    } else {
        // Request permission for notifications
        Notification.requestPermission().then((res) => {
            if (res === 'granted') {
                console.log('Notification permission granted');
            } else if (res === 'denied') {
                console.log('Permission denied');
            } else if (res === 'default') {
                console.log('Notification permission not given');
            }
        });
    }
} else {
    console.log('Notification not supported');
}

// Variable to keep track of notification count
var NotificationCount = 0;

// Function to display notification
function notify(job, category) {
    if (!job || !category) {
        console.error("Job or category is undefined");
        return; // Exit the function if job or category is undefined
    }

    console.log("Notification received for category:", category);
    // Check if permission is granted and job is provided
    if (Notification.permission === 'granted') {
        // Create notification
        var notification = new Notification("New " + category + " Job", {
            body: "New Job: " + job.title
        });

        // Increment notification count
        NotificationCount++;
        // Update document title to show notification count
        document.title = "(" + NotificationCount + ") Job Finder";
        console.log("NotificationCount:", NotificationCount);
        console.log("Document title:", document.title);

        // Update badge count for the category
        var badges = document.querySelectorAll('.job-badge');
        badges.forEach(function(badge) {
            if (badge.dataset.category === category) {
                var currentCount = parseInt(badge.innerText, 10);
                badge.innerText = (currentCount + 1).toString();
            }
        });
    }
}

// Function to reload the page
function reloadPage() {
    setTimeout(function() {
        window.location.reload();
    }, 300000); // Reload the page every 5 minutes
}

window.onload = function() {
    var selectedCategory = localStorage.getItem('selectedCategory');
    if (selectedCategory) {
        showJobs(selectedCategory);
    } else {
        showJobs('python');
    }
    reloadPage();
}
