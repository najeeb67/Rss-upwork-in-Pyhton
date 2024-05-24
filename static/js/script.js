var socket;
var isConnected = false;
var socket = io.connect('http://localhost:5000');


  
socket.on('connect', function() {
    console.log('Connected to server');
});


socket.on('disconnect', function() {
        console.log('Disconnected from server');
    });
    


function logToContainer(message) {
    var logContainer = document.getElementById("logContainer");
    var logMessage = document.createElement("div");
    logMessage.innerText = message;
    logContainer.appendChild(logMessage);
    logContainer.scrollTop = logContainer.scrollHeight;
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
var newJobCounts = {
    python: 0,
    react: 0,
    // Add other categories here...
};

function updateBadgeCount(category, count) {
    var badge = document.querySelector('.job-badge[data-category="' + category + '"]');
    if (badge) {
        badge.innerText = count.toString();
    }
}



// Event listener for new job events from the server
socket.on('new_job', function(data) {
    console.log("Received new job event with data:", data);

    // Ensure data and data.jobs are defined
    if (data && data.jobs && data.category) {
        console.log("Job category:", data.category);

        // Update job list for the specified category
        var jobList = document.getElementById(data.category + 'Jobs');
        if (jobList) {
            // Clear the existing job items
            jobList.innerHTML = '';

            // Update the new job count for the category
            newJobCounts[data.category] += data.jobs.length;

            // Update badge count for the category
            updateBadgeCount(data.category, newJobCounts[data.category]);

            // Iterate over the new job entries and append them to the job list
            data.jobs.forEach(function(job) {
                var jobItem = document.createElement('div');
                jobItem.classList.add('job-item');
                jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
                jobList.appendChild(jobItem);
            });

            notify(data.job, data.category);
        } else {
            console.error("Job list not found for category:", data.category);
        }
    } else {
        console.error("Received job list is undefined or missing category property");
        console.log("Data received:", data);
    }
});


// Function to reload page and clear new job counts
function reloadPage() {
    console.log("Reloading page...");
    // Clear new job counts
    for (var category in newJobCounts) {
        if (newJobCounts.hasOwnProperty(category)) {
            newJobCounts[category] = 0;
        }
    }
    // Reload page after 2 minutes
    setTimeout(function() {
        window.location.reload();
    }, 120000);
}

window.onload = function() {
    var selectedCategory = localStorage.getItem('selectedCategory');
    if (selectedCategory) {
        showJobs(selectedCategory);
    } else {
        showJobs('python');
    }
    // Reload the page and clear new job counts
    reloadPage();
};




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

// function reloadPage() {
//     console.log("Reloading page...");
//     setTimeout(function() {
//         window.location.reload();
//     }, 120000); 
// }

// window.onload = function() {
//     var selectedCategory = localStorage.getItem('selectedCategory');
//     if (selectedCategory) {
//         showJobs(selectedCategory);
//     } else {
//         showJobs('python');
//     }
//     reloadPage();
// }
