// ==UserScript==
// @name         API Finder
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  hit the button and find the api then auto download 
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    let logEntries = [];

    // Create and style the download button
    const button = document.createElement('button');
    button.innerText = 'Download Log';
    button.style.position = 'fixed';
    button.style.bottom = '20px';
    button.style.right = '20px';
    button.style.padding = '10px 20px';
    button.style.backgroundColor = '#007bff';
    button.style.color = '#fff';
    button.style.border = 'none';
    button.style.borderRadius = '5px';
    button.style.cursor = 'pointer';
    button.style.zIndex = '1000';

    document.body.appendChild(button);

    // Create a function to log all network requests
    function logNetworkRequests() {
        const oldXhrOpen = XMLHttpRequest.prototype.open;
        const oldFetch = window.fetch;

        // Override XMLHttpRequest.open to capture API requests
        XMLHttpRequest.prototype.open = function(method, url, ...rest) {
            logEntries.push(`XHR Request: ${method} ${url}`);
            console.log('XHR Request:', method, url);
            return oldXhrOpen.apply(this, [method, url, ...rest]);
        };

        // Override fetch to capture API requests
        window.fetch = function(url, ...rest) {
            logEntries.push(`Fetch Request: ${url}`);
            console.log('Fetch Request:', url);
            return oldFetch.apply(this, [url, ...rest]);
        };
    }

    // Function to download log file
    function downloadLog() {
        const blob = new Blob([logEntries.join('\n')], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'api_requests_log.txt';
        a.click();
        URL.revokeObjectURL(url);
    }

    // Add click event listener to the button
    button.addEventListener('click', downloadLog);

    // Run the function to start logging requests
    logNetworkRequests();
})();
