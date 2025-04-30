// background.js

// Listen for toolbar button clicks
browser.browserAction.onClicked.addListener(async (tab) => {
    console.log("Extension clicked, tab URL:", tab.url); // Debug log

    try {
        const url = tab.url;
        if (!url) {
            console.error("No URL found in active tab.");
            return;
        }

        // Send URL to local backend
        const response = await fetch(`http://127.0.0.1:8000/scrape/${encodeURIComponent(url)}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            console.error("Server responded with", response.status);
        } else {
            console.log("URL sent successfully:", url);
        }
    } catch (err) {
        console.error("Error sending URL:", err);
    }
});

// Create a context menu item
browser.contextMenus.create({
    id: "send-to-backend",
    title: "Send Link to Backend",
    contexts: ["page", "link"], // Show on right-clicking a page or a link
});

// Listen for context menu item clicks
browser.contextMenus.onClicked.addListener(async (info, tab) => {
    let urlToSend;

    // Determine the URL to send
    if (info.linkUrl) {
        // If the user right-clicked a link
        urlToSend = info.linkUrl;
    } else if (info.pageUrl) {
        // If the user right-clicked the page
        urlToSend = info.pageUrl;
    }

    if (!urlToSend) {
        console.error("No URL found to send.");
        return;
    }

    console.log("Sending URL to backend:", urlToSend);

    try {
        // Send the URL to the backend
        const response = await fetch(`http://127.0.0.1:8000/scrape/${encodeURIComponent(urlToSend)}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            console.error("Server responded with", response.status);
        } else {
            console.log("URL sent successfully:", urlToSend);
        }
    } catch (err) {
        console.error("Error sending URL:", err);
    }
});

