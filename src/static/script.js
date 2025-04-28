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

            // Check if the response is OK
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();

            // Log the response for debugging
            console.log("Response data:", data);

            // Handle the response format
            if (typeof data.result === "number") {
                // If result is a number, display it
                document.getElementById("scrape-result").textContent = `Scrape result: data has successfully scraped`;
            } else if (data.result && typeof data.result.text === "string") {
                // If result contains text, display it
                const resultElement = document.getElementById("scrape-result");
                resultElement.style.whiteSpace = "pre-wrap"; // Ensure line breaks are respected
                const formattedText = data.result.text
                    .replace(/\\n/g, "\n") // Replace escaped \n with actual newlines
                    .replace(/: /g, ":\n") // Add a newline after each colon and space
                    .replace(/ - /g, "\n- "); // Add a newline before each dash
                resultElement.textContent = formattedText;
            } else {
                throw new Error("Unexpected response format");
            }
        } catch (error) {
            console.error("Error during scraping:", error); // Log the error for debugging
            alert("Failed to scrape the URL");
        }

        // Clear previous URL
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

            console.log(data); // Debugging: Log the API response

            // Handle multiple results
            const results = data.result || [];
            if (!Array.isArray(results) || results.length === 0) {
                document.getElementById("search-keyword-result").textContent = "No results found.";
                return;
            }

            // Display each result
            const resultElement = document.getElementById("search-keyword-result");
            resultElement.style.whiteSpace = "pre-wrap"; // Ensure line breaks are respected
            resultElement.textContent = ""; // Clear previous content

            results.forEach((item, index) => {
                // Create a container for each result
                const resultContainer = document.createElement("div");
                resultContainer.style.marginBottom = "1em";

                // Add result details
                const title = document.createElement("h4");
                title.textContent = `Result ${index + 1}`;
                resultContainer.appendChild(title);

                const url = document.createElement("a");
                url.href = item.url;
                url.textContent = item.url;
                url.target = "_blank"; // Open in a new tab
                resultContainer.appendChild(url);

                const time = document.createElement("p");
                time.textContent = `Time: ${item.time}`;
                resultContainer.appendChild(time);

                const text = document.createElement("p");
                text.textContent = item.text;
                resultContainer.appendChild(text);

                // Append the result container to the result element
                resultElement.appendChild(resultContainer);
            });
        } catch (error) {
            console.error("Error:", error);
            alert("Failed to search by keyword");
        }

        // Clear previous keyword
        document.getElementById("search-keyword").value = "";
    });
});