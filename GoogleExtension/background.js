chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    if (!tab.url.startsWith('chrome://') && !tab.url.startsWith('edge://')) {
      console.log('Checking URL:', tab.url);
      checkPhishing(tab.url);
    }
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "checkPhishing") {
    checkPhishing(request.url, sendResponse);
    return true;  // 保持消息通道开放，以便异步响应
  }
});

async function checkPhishing(url, callback) {
  try {
    console.log('Sending request to backend...');
    const response = await fetch('http://localhost:5000/check_url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url })
    });

    const result = await response.json();
    console.log('Received result:', result);

    chrome.notifications.create('phishingAlert', {
      type: 'basic',
      iconUrl: 'icon48.png',
      title: 'Phishing Website Detection:',
      message: result.is_phishing ?
        'Alert：此网站可能是钓鱼网站!' :
        'This website is Safe',
      priority: 2
    });

    if (callback) callback(result);
  } catch (error) {
    console.error('Error:', error);
    chrome.notifications.create('errorAlert', {
      type: 'basic',
      iconUrl: 'icon48.png',
      title: 'Error',
      message: 'Failed to connect to the Server',
      priority: 2
    });

    if (callback) callback({error: error.message});
  }
}
