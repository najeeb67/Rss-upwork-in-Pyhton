// Socket.io connection setup
var socket = io.connect('http://127.0.0.1:5000', {
    reconnection: true,
    reconnectionAttempts: Infinity,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    timeout: 20000,
    pingTimeout: 60000,
    pingInterval: 25000
});

// Event listener for successful connection
socket.on('connect', function() {
    console.log('Connected to server');
});

// Event listener for disconnection
socket.on('disconnect', function() {
    console.log('Disconnected from server');
});

// Event listener for connection errors
socket.on('connect_error', (err) => {
    console.log(`connect_error due to ${err.message}`);
});

// Object to track new job counts per category
var newJobCounts = {
    python: 0,
    react: 0,
    us: 0,
    node: 0,
    php: 0,
    wordpress: 0,
    quickbooks: 0,
    shopify: 0,
    apiIntegration: 0,
    paymentGateway: 0,
    fullTime: 0,
    chatbot: 0,
    scripting: 0,
    bubble: 0,
    webrtc: 0,
    vue: 0
};

// Event listener for new job notifications from the server
socket.on('new_job', function(data) {
    console.log("Received new job event with data:", data);

    // Notify user about the new job via notification
    notify(data.job, data.category);
    
    var formattedCategory = formatCategory(data.category);
    
    // Update newJobCounts and then update badge count
    if (formattedCategory && newJobCounts.hasOwnProperty(formattedCategory)) {
        newJobCounts[formattedCategory]++;
        updateBadgeCount(formattedCategory, newJobCounts[formattedCategory]);
    } else {
        console.error("Invalid category or count data received:", data);
    }
    // Update UI to display the new job if it meets certain criteria (e.g., published within the last minute)
    if (data.job && data.job.title && data.job.link && data.job.published) {
        var currentTime = new Date();
        var publishedTime = new Date(data.job.published);

        // Check if the job is published within the last minute
        if ((currentTime - publishedTime) / 1000 <= 60) {
            var jobList = document.getElementById(data.category + 'Jobs').querySelector('.job-items');
            if (jobList) {
                // Create a new job item element
                var jobItem = document.createElement('div');
                jobItem.classList.add('job-item');
                jobItem.innerHTML = '<a class="job-title" href="' + data.job.link + '" onclick="markAsClicked(this)" target="_blank">' + data.job.title + '</a><p class="job-published">Published: ' + data.job.published + '</p>';

                // Limit the number of job items to 50
                var jobItems = jobList.querySelectorAll('.job-item');
                if (jobItems.length >= 50) {
                    jobList.removeChild(jobItems[jobItems.length - 1]);
                }

                // Insert the new job item at the beginning of the list
                jobList.insertBefore(jobItem, jobList.firstChild);
            } else {
                console.error("Job list not found for category:", data.category);
            }
        }
    } else {
        console.error("Invalid job data received:", data);
    }
});

// Function to request notification permission (if supported by the browser)
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

// Function to display a notification for a new job
function notify(job, category) {
    if (Notification.permission === 'granted') {
        var notificationBody = job.title + ' in ' + category + '\nPublished: ' + job.published;
        var notification = new Notification('New Job Posted', {
            body: notificationBody,
            data: { url: job.link }
        });

        notification.onclick = function(event) {
            event.preventDefault();
            window.open(notification.data.url, '_blank');
        };
    } else {
        console.log('Notification permission not granted');
    }
}

function updateBadgeCount(category, count) {
    // Adjust the category value if necessary to match the data-category attribute in HTML
    var formattedCategory = formatCategory(category); // Function to format category name

    var badge = document.querySelector('.job-badge[data-category="' + formattedCategory + '"]');
    if (badge) {
        badge.innerText = count.toString();
    } else {
        console.error("Badge element not found for category:", formattedCategory);
    }
}

// Function to format category name (adjust as per your naming convention)
function formatCategory(category) {
    // Example: If your category is 'python_entries', you might need to extract 'python'
    return category.replace('_entries', ''); // Adjust as per your naming convention
}



// Initial setup when the window loads
window.onload = function() {
    // Logic to handle initial state or previous selections
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
        showJobs('python'); // Default category to show initially
    }

    // Function to reload the page after a certain period
    reloadPage();
};

// Function to display jobs based on selected category
function showJobs(category) {
    var jobCategories = document.querySelectorAll('.job-category');
    jobCategories.forEach(function(jobCategory) {
        jobCategory.style.display = 'none';
    });

    var selectedCategory = document.getElementById(category + 'Jobs');
    if (selectedCategory) {
        selectedCategory.style.display = 'block';
        localStorage.setItem('selectedCategory', category);
    }
}

// Function to mark a job link as visited
function markAsClicked(element) {
    var key = 'notified_' + element.innerText;
    localStorage.setItem(key, 'true');
    element.classList.add('visited');
}

// Function to reload the page after a certain period
function reloadPage() {
    console.log("Reloading page...");
    // Reset new job counts
    for (var category in newJobCounts) {
        if (newJobCounts.hasOwnProperty(category)) {
            newJobCounts[category] = 0;
        }
    }
    // Reload the page after 150000 ms (2.5 minutes)
    setTimeout(function() {
        window.location.reload();
    }, 150000);
}
