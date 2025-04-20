document.addEventListener("DOMContentLoaded", () => {
    // Scrape URL
    document.getElementById("scrape-btn").addEventListener("click", async () => {
        // Clear previous results
        document.getElementById("scrape-result").textContent = "";

        const url = document.getElementById("scrape-url").value;

        if (!url) {
            alert("Please enter a URL");
            return;
        }

        try {
            const response = await fetch(`/scrape/${encodeURIComponent(url)}`);
            const data = await response.json();

            // Display the result with line breaks
            const resultElement = document.getElementById("scrape-result");
            resultElement.style.whiteSpace = "pre-wrap"; // Ensure line breaks are respected
            const formattedText = JSON.stringify(data.result.text, null, 2)
                .replace(/\\n/g, "\n") // Replace escaped \n with actual newlines
                .replace(/: /g, ":\n") // Add a newline after each colon and space
                .replace(/ - /g, "\n- "); // Add a newline before each dash
            resultElement.textContent = formattedText;
        } catch (error) {
            alert("Failed to scrape the URL");
        }

        // Clear previous url
        document.getElementById("scrape-url").value = "";

    });

    // Search by URL
    document.getElementById("search-url-btn").addEventListener("click", async () => {

        // Clear previous results
        document.getElementById("search-url-result").textContent = "";

        const url = document.getElementById("search-url").value;
        if (!url) {
            alert("Please enter a URL");
            return;
        }

        try {
            const response = await fetch(`/search_url/${encodeURIComponent(url)}`);
            const data = await response.json();

            // Display the result with line breaks
            const resultElement = document.getElementById("search-url-result");
            resultElement.style.whiteSpace = "pre-wrap"; // Ensure line breaks are respected
            const formattedText = JSON.stringify(data.result.text, null, 2)
                .replace(/\\n/g, "\n") // Replace escaped \n with actual newlines
                .replace(/: /g, ":\n") // Add a newline after each colon and space
                .replace(/ - /g, "\n- "); // Add a newline before each dash
            resultElement.textContent = formattedText;
        } catch (error) {
            alert("Failed to search by URL");
        }

        // Clear previous url
        document.getElementById("search-url").value = "";

    });

    // Search by Keyword
    document.getElementById("search-keyword-btn").addEventListener("click", async () => {
        // Clear previous results
        document.getElementById("search-keyword-result").textContent = "";


        const keyword = document.getElementById("search-keyword").value;
        if (!keyword) {
            alert("Please enter a keyword");
            return;
        }

        try {
            const response = await fetch(`/search_keyword/${encodeURIComponent(keyword)}`);
            const data = await response.json();

            // Display the result with line breaks
            const resultElement = document.getElementById("search-keyword-result");
            resultElement.style.whiteSpace = "pre-wrap"; // Ensure line breaks are respected
            const formattedText = JSON.stringify(data.result.text, null, 2)
                .replace(/\\n/g, "\n") // Replace escaped \n with actual newlines
                .replace(/: /g, ":\n") // Add a newline after each colon and space
                .replace(/ - /g, "\n- "); // Add a newline before each dash
            resultElement.textContent = formattedText;
        } catch (error) {
            alert("Failed to search by keyword");
        }

        // Clear previous keyword
        document.getElementById("search-keyword").value = "";

    });
});