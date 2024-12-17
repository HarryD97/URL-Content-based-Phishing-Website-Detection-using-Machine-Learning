chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "checkPhishing") {
        checkPhishing(request.url, (result) => {
            sendResponse(result); // Directly send the result from the backend
        });
        return true; // Keep the message channel open for asynchronous response
    }
});

async function checkPhishing(url, callback) {
    try {
        console.log('Sending request to backend...');
        const response = await fetch('https://localhost:5000/check_url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });
        const result = await response.json();
        console.log('Received result:', result);

        // Notify user of phishing probability
        chrome.notifications.create('phishingAlert', {
            type: 'basic',
            iconUrl: 'icon48.png',
            title: 'Phishing Website Detection:',
            message: `Phishing probability is: ${(result.confidence * 100).toFixed(2)}%`,
            priority: 2
        });
        if (callback) callback(result);
    } catch (error) {
        console.error('Error:', error);

        // Notify user of error
        chrome.notifications.create('errorAlert', {
            type: 'basic',
            iconUrl: 'icon48.png',
            title: 'Error',
            message: 'Failed to connect to the Server',
            priority: 2
        });
        if (callback) callback({ error: error.message });
    }
}
