// Establish socket connection
var socket = io.connect('http://localhost:5000');

// Variables
var isConnected = false;
var NotificationCount = 0;
var newJobCounts = {
    python: 0,
    react: 0,
    // Add other categories here...
};

// Event listeners for socket connection
socket.on('connect', function() {
    isConnected = true;
    console.log('Connected to server');
});

socket.on('disconnect', function() {
    isConnected = false;
    console.log('Disconnected from server');
});

// Event listener for new job events from the server
socket.on('new_job', function(data) {
    console.log("Received new job event with data:", data);

    if (data && data.jobs && data.category) {
        console.log("Job category:", data.category);
        console.log("testing")
        var jobList = document.getElementById(data.category + 'Jobs');
        if (jobList) {
            jobList.innerHTML = '';

            newJobCounts[data.category] += data.jobs.length;

            updateBadgeCount(data.category, newJobCounts[data.category]);

            data.jobs.forEach(function(job) {
                var jobItem = document.createElement('div');
                jobItem.classList.add('job-item');
                jobItem.innerHTML = '<a class="job-title" href="' + job.link + '" onclick="markAsClicked(this)" target="_blank">' + job.title + '</a><p class="job-published">Published: ' + job.published + '</p>';
                jobList.appendChild(jobItem);
            });
            
            console.log("this is woking")
        } else {
            console.error("Job list not found for category:", data.category);
        }
    } else {
        console.error("Received job list is undefined or missing category property");
        console.log("Data received:", data);
    }
});

// Notification permission check and request
if ("Notification" in window) {
    if (Notification.permission === 'granted') {
        console.log('Notification permission granted');
    } else {
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

// Notification function
function notify(job, category) {
    console.log("Notify function called with job:", job, "and category:", category);

    if (!job || !category) {
        console.error("Job or category is undefined");
        return;
    }

    if (Notification.permission === 'granted') {
        var notification = new Notification("New " + category + " Job", {
            body: "New Job: " + job.title
        });

        notification.onclick = function() {
            console.log("Notification clicked!");
            // Optionally handle click event
        };

        NotificationCount++;
        document.title = "(" + NotificationCount + ") Job Finder";

        updateBadgeCount(category, newJobCounts[category] + 1);
    } else {
        console.log("Notification permission not granted");
    }
}

notify("hello", "this thewlnfbv")
// Function to update badge count
function updateBadgeCount(category, count) {
    var badge = document.querySelector('.job-badge[data-category="' + category + '"]');
    if (badge) {
        badge.innerText = count.toString();
    }
}

// Function to reload page and clear new job counts
function reloadPage() {
    console.log("Reloading page...");
    for (var category in newJobCounts) {
        if (newJobCounts.hasOwnProperty(category)) {
            newJobCounts[category] = 0;
        }
    }
    setTimeout(function() {
        window.location.reload();
    }, 120000);
}

// Window onload event
window.onload = function() {
    var selectedCategory = localStorage.getItem('selectedCategory');
    if (selectedCategory) {
        showJobs(selectedCategory);
    } else {
        showJobs('python');
    }
    reloadPage();
};

// Helper function to show jobs by category
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

// Function to mark job as clicked
function markAsClicked(link) {
    link.classList.add('clicked');
    NotificationCount = 0;
    document.title = "Job Finder";
}
