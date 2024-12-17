document.getElementById('checkButton').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        let currentUrl = tabs[0].url;
        document.getElementById('status').textContent = 'Checking URL: ' + currentUrl;

        // Send a message to the background script to check phishing status
        chrome.runtime.sendMessage({ action: "checkPhishing", url: currentUrl }, (response) => {
            if (!response) {
                document.getElementById('status').textContent = 'No response received.';
                return;
            }

            if (response.error) {
                document.getElementById('status').textContent = 'Error: ' + response.error;
            } else {
                const confidencePercentage = (response.confidence * 100).toFixed(2) + '%';
                document.getElementById('status').textContent = response.is_phishing ?
                    'Phishing website probability is: ' + confidencePercentage + '!' :
                    'Safe probability is: ' + confidencePercentage + '!';
            }
        });
    });
});
