document.addEventListener("DOMContentLoaded", () => {
    // Scrape URL
    document.getElementById("scrape-btn").addEventListener("click", async () => {
        const url = document.getElementById("scrape-url").value;
        if (!url) {
            alert("Please enter a URL");
            return;
        }

        try {
            const response = await fetch(`/scrape/${encodeURIComponent(url)}`);
            const data = await response.json();
            document.getElementById("scrape-result").textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            alert("Failed to scrape the URL");
        }
    });

    // Search by URL
    document.getElementById("search-url-btn").addEventListener("click", async () => {
        const url = document.getElementById("search-url").value;
        if (!url) {
            alert("Please enter a URL");
            return;
        }

        try {
            const response = await fetch(`/search_url/${encodeURIComponent(url)}`);
            const data = await response.json();
            document.getElementById("search-url-result").textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            alert("Failed to search by URL");
        }
    });

    // Search by Keyword
    document.getElementById("search-keyword-btn").addEventListener("click", async () => {
        const keyword = document.getElementById("search-keyword").value;
        if (!keyword) {
            alert("Please enter a keyword");
            return;
        }

        try {
            const response = await fetch(`/search_keyword/${encodeURIComponent(keyword)}`);
            const data = await response.json();
            document.getElementById("search-keyword-result").textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            alert("Failed to search by keyword");
        }
    });
});