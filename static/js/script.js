var socket = io.connect('http://localhost:5000');

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
});

socket.on('connect_error', (err) => {
    console.log(`connect_error due to ${err.message}`);
});

var newJobCounts = [];

socket.on('new_job', function(data) {
    console.log("Received new job event with data:", data);

    // Ensure data and data.job are defined
    if (data && data.title && data.link && data.published) {
        var currentTime = new Date();
        var publishedTime = new Date(data.published);

        // Check if the job is published within the last 30 seconds
        if ((currentTime - publishedTime) / 1000 <= 30) {
            console.log("Job category:", data.category);

            // Notification
            notify(data, data.category);

            // Update job list
            var jobList = document.getElementById(data.category + 'Jobs');
            if (jobList) {
                var jobItem = document.createElement('div');
                jobItem.classList.add('job-item');
                jobItem.innerHTML = '<a class="job-title" href="' + data.link + '" onclick="markAsClicked(this)" target="_blank">' + data.title + '</a><p class="job-published">Published: ' + data.published + '</p>';
                jobList.appendChild(jobItem);
            } else {
                console.error("Job list not found for category:", data.category);
            }
        }
    } else {
        console.error("Invalid job data received:", data);
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

var NotificationCount = [];
// Notification function
function notify(job, category) {
    if (Notification.permission === 'granted') {
        var notification = new Notification('New Job Posted', {
            body: job.title + ' in ' + category,
            data: { url: job.link }
        });

        notification.onclick = function(event) {
            event.preventDefault(); // Prevent the browser from focusing the Notification's tab
            window.open(notification.data.url, '_blank');
        };
    } else {
        console.log('Notification permission not granted');
    }
}

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
    }, 150000);
}

// Window onload event
window.onload = function() {
    // Retrieve notified jobs from localStorage
    var notifiedJobs = {};
    for (var key in localStorage) {
        if (key.startsWith('notified_')) {
            notifiedJobs[key] = true;
        }
    }

    var selectedCategory = localStorage.getItem('selectedCategory');
    if (selectedCategory) {
        showJobs(selectedCategory);
    } else {
        showJobs('python');
    }
    reloadPage();

    // Retrieve existing jobs and notify only for new jobs
    var jobCategories = document.querySelectorAll('.main-content > div');
    jobCategories.forEach(function(categoryElement) {
        var category = categoryElement.id.replace('Jobs', '');
        var jobs = categoryElement.querySelectorAll('.job-item');
        jobs.forEach(function(job) {
            var jobId = job.querySelector('.job-title').getAttribute('href');
            if (!notifiedJobs['notified_' + jobId]) {
                var jobData = {
                    title: job.querySelector('.job-title').innerText,
                    link: job.querySelector('.job-title').getAttribute('href'),
                    published: job.querySelector('.job-published').innerText
                };
                notify(jobData, category);
            }
        });
    });
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
