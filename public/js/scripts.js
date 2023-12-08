/*!
* Start Bootstrap - Full Width Pics v5.0.6 (https://startbootstrap.com/template/full-width-pics)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-full-width-pics/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

function uploadPicture() {
    var fileInput = document.getElementById('pictureInput');
    var file = fileInput.files[0];

    if (file) {
        var formData = new FormData();
        formData.append('picture', file);

        fetch('/upload_picture', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Handle success or redirect to success page
            window.location.href = '/upload_success.html';
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}