document.getElementById('checkButton').addEventListener('click', () => {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    let currentUrl = tabs[0].url;
    document.getElementById('status').textContent = 'Checking URL: ' + currentUrl;
    
    chrome.runtime.sendMessage({action: "checkPhishing", url: currentUrl}, (response) => {
      if (response.error) {
        document.getElementById('status').textContent = 'Error: ' + response.error;
      } else {
        document.getElementById('status').textContent = response.is_phishing ? 
'Alert: This website is unsafe!' : 
          'This website is safe!';
      }
    });
  });
});
