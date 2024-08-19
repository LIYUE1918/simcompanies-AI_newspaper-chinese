// ==UserScript==
// @name         Auto Download
// @namespace    http://tampermonkey.net/
// @version      8.1
// @description  #检测时间自动下载html并保存为txt格式。#
// @match        #写上你要的爬的网站地址#
// @grant        none
// @icon         https://www.google.com/s2/favicons?sz=64&domain=github.com
// ==/UserScript==

(function() {
    'use strict';

    // Variable to keep track of the file number
    var fileNumber = parseInt(localStorage.getItem('fileNumber') || '1', 10);
    var downloading = false;

    // Function to perform the download
    function performDownload() {
        if (downloading) return; // Prevent multiple downloads at the same time
        downloading = true;

        var pageContent = document.documentElement.outerHTML;
        var blob = new Blob([pageContent], { type: 'text/plain' });

        // Create a timestamp
        var now = new Date();
        var timestamp = now.toISOString().replace(/:/g, '-'); // Replace colons for filename compatibility

        // Create a file name with sequential number and timestamp，保存格式「名称」+「时间」
        var filename = `${fileNumber}_${timestamp}.txt`;

        var link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
        URL.revokeObjectURL(link.href);

        // Increment file number and save to local storage
        fileNumber++;
        localStorage.setItem('fileNumber', fileNumber);

        // Set a flag in local storage to indicate the last download
        localStorage.setItem('lastDownloadTime', new Date().toISOString());

        // Reset downloading flag
        setTimeout(() => {
            downloading = false;
        }, 2000); // Wait a bit before allowing another download
    }

    // Function to check if the current time is at the beginning of the minute
    function checkTime() {
        var now = new Date();
        var seconds = now.getSeconds();
        var lastDownloadTime = localStorage.getItem('lastDownloadTime');
        var lastDownloadDate = lastDownloadTime ? new Date(lastDownloadTime) : null;

        // Check if it's time to download (start of a minute and last download was not in this minute)
        if (seconds === 0 && (!lastDownloadDate || now - lastDownloadDate > 60 * 1000)) { // 1 minute interval
            performDownload();
            // Refresh the page after downloading
            setTimeout(() => {
                if (!downloading) { // Only refresh if no download is ongoing
                    location.reload();
                }
            }, 2000); // Delay page reload to ensure download completes
        }
    }

    // Set interval to check the time every second
    setInterval(checkTime, 1000); // 1,000 ms = 1 second

    // Perform an initial check immediately
    checkTime();
})();
