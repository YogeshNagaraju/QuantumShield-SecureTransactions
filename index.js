document.addEventListener("DOMContentLoaded", async () => {
    try {
        await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
        await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
        await faceapi.nets.ssdMobilenetv1.loadFromUri('/models');
        console.log("Face-api models loaded successfully.");
    } catch (error) {
        console.error("Error loading face-api models:", error);
    }
});

function startFaceRegistration() {
    document.getElementById("video-container").classList.remove("hidden");
    startVideo();
}

function startVideo() {
    const video = document.getElementById("video");
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
        .then(stream => { 
            video.srcObject = stream;
            console.log("Webcam started successfully.");
        })
        .catch(err => {
            console.error("Error accessing webcam:", err);
            alert("Please allow camera access and check if it's being used by another application.");
        });
}

function captureFace() {
    const video = document.getElementById("video");
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    // Set canvas size to match the video frame
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw the current frame from the video
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the image to Base64 format
    const capturedImage = canvas.toDataURL("image/png");

    // Display the captured image on screen
    document.getElementById("captured-face").src = capturedImage;
    document.getElementById("captured-face-container").classList.remove("hidden");

    // Stop the webcam after capture
    video.srcObject.getTracks().forEach(track => track.stop());
    document.getElementById("video-container").classList.add("hidden");

    alert("Face captured successfully!");

    // Send user, transaction, and image data to the server
    saveDataToServer(capturedImage);
}

function saveDataToServer(imageData) {
    const userData = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        transaction_id: document.getElementById("transaction_id").value,
        date: document.getElementById("date").value,
        account_number: document.getElementById("account_number").value,
        transaction_type: document.getElementById("transaction_type").value,
        amount: parseFloat(document.getElementById("amount").value),
        image: imageData
    };

    fetch('http://127.0.0.1:5000/save_data', {  
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Error saving data:", data.error);
            alert("Failed to save data: " + data.error);
        } else {
            console.log("Data saved successfully at:", data.path);
            document.getElementById("result").innerText = `Risk Level: ${data.risk_level}`;
            alert("Data saved successfully!");
        }
    })
    .catch(error => {
        console.error("Error sending data:", error);
        alert("Error sending data to the server.");
    });
}
