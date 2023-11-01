var playedConnectionTone = false;

$(document).ready(function () {
  $("#yourFormID").on("submit", function () {
    // ... Your submit logic

    // Close the modal after form submission
    $("#connectModal").modal("hide");
  });

  $("#publish-form").on("submit", function (e) {
    e.preventDefault(); // Prevent the form from submitting the traditional way

    var topic = $("#topic").val();
    var message = $("#message").val();

    fetch("/publish", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        topic: topic,
        message: message,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok " + response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Success:", data);
        // updateMessagesList(data.messages);  // Call a function to update the messages list
      })
      .catch((error) => {
        alert("error:", error);
        updateConnectionStatus(
          '<span class="badge bg-warning">Not Connected</span>'
        ); // Update the UI
      });
  });

  document
    .getElementById("broker-form")
    .addEventListener("submit", function (e) {
      e.preventDefault(); // Prevent the form from submitting the traditional way

      var broker = document.getElementById("broker").value;
      var port = document.getElementById("port").value;
      var username = document.getElementById("username").value;
      var password = document.getElementById("password").value;

      //   Update the connection details here

      // Update the connection details here
      document.getElementById("broker-display").innerHTML =
        "<strong>Broker:</strong> " + broker;
      document.getElementById("port-display").innerHTML =
        "<strong>Port:</strong> " + port;
      // Close the modal after form submission
      hideModal("connectModal");

      fetch("/connect", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          broker: broker,
          port: port,
          username: username,
          password: password,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(
              "Network response was not ok " + response.statusText
            );
          }
          return response.json();
        })
        .then((data) => {
          console.log("Success:", data);
          updateConnectionStatus(
            '<span class="badge bg-success">Connected</span>'
          );

          //  set flask variable connection_status// Update the UI
          connection_status = "Connected";
        })
        .catch((error) => {
          alert("error:", error);
          connection_status = "Not Connected";

          updateConnectionStatus(
            '<span class="badge bg-warning">Not Connected</span>'
          ); // Update the UI
        });
    });

  var socket = io.connect("http://" + document.domain + ":" + location.port);

  socket.on("update_connection_status", function (status) {
    updateUIConnectionStatus(status);
    if (playedConnectionTone == false) {
      playedConnectionTone = true;
      // playNotificationTone();
    }
  });

  socket.on("badge", function (message) {
    const badge = document.getElementById("notification-badge");
    badge.textContent = message;
    badge.style.display = "block"; // Show the badge
    setTimeout(() => {
      badge.style.display = "none"; // Hide the badge after 5 seconds
    }, 5000);
  });

  socket.on("update_defined_calls", function (message) {
    show_badge(message);

    // Update UI new li element

    var li = document.createElement("li");
    li.className = "list-group-item";
    li.textContent = message.name;
    // add padding and margin
    // li.style.padding = "10px";
    li.style.marginBottom = "15px";
    li.style.marginLeft = "5px";
    li.style.border = "1px solid #ddd";
    li.style.borderRadius = "5px";

    
    // create a button 
    var button = document.createElement("button");
    button.className = "btn btn-danger btn-sm float-end";

    button.textContent = "Run";
    button.onclick = function() {

      socket.emit("run_defined_call", message);
    }
    // shift right
    button.style.marginLeft = "20px";


    li.appendChild(button);
    // add breakpoint
    var br = document.createElement("br");
    
    li.appendChild(br);
    li.appendChild(br);
    li.appendChild(br);
    li.appendChild(br);

    document.getElementById("defined-calls-list").appendChild(li);

    // Scroll to the bottom of the messages container
    document.getElementById("defined-calls-list").scrollTop =
      document.getElementById("defined-calls-list").scrollHeight;
  });
});

// let context = new (window.AudioContext || window.webkitAudioContext)();

function show_badge(message) {
  const badge = document.getElementById("notification-badge");
  badge.textContent = message.topic + " " + message.message;
  badge.style.display = "block"; // Show the badge
  setTimeout(() => {
    badge.style.display = "none"; // Hide the badge after 5 seconds
  }, 5000);
}

function playTone(frequency = 440, duration = 0.5) {
  // Create an oscillator node
  let oscillator = context.createOscillator();
  oscillator.type = "sine"; // Type of sound
  oscillator.frequency.setValueAtTime(frequency, context.currentTime); // Set frequency (in Hz)

  // Connect the oscillator to the context's destination (the speakers)
  oscillator.connect(context.destination);

  // Start the oscillator and stop it after the specified duration
  oscillator.start();
  oscillator.stop(context.currentTime + duration);
}

function playNotificationTone() {
  const frequencies = [523.25, 587.33, 659.25]; // C5, D5, E5
  let startTime = context.currentTime;
  const noteDuration = 0.15; // Short duration for each note

  // Create a GainNode to control the volume
  let gainNode = context.createGain();
  gainNode.gain.value = 0.3; // Adjust volume here, 0.3 is 30% of the original volume
  gainNode.connect(context.destination);

  frequencies.forEach((frequency, index) => {
    let oscillator = context.createOscillator();
    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime(
      frequency,
      startTime + index * noteDuration
    );

    // oscillator.connect(context.destination);
    oscillator.connect(gainNode); // Connect oscillator to the gainNode instead of directly to the destination
    oscillator.start(startTime + index * noteDuration);
    oscillator.stop(startTime + (index + 1) * noteDuration);
  });
}

function updateConnectionStatus(status) {
  document.getElementById("connection-status").innerHTML = status;
}

function updateUIConnectionStatus(isConnected) {
  const statusElement = document.getElementById("connection-status");
  if (isConnected) {
    statusElement.textContent = "Connected";
    statusElement.style.color = "green";
  } else {
    statusElement.textContent = "Disconnected";
    statusElement.style.color = "red";
  }
}

function updateMessagesList(messages) {
  var messagesContainer = document.getElementById("messages-container");
  // messagesContainer.innerHTML = '';  // Clear the existing messages
  messages.forEach((message) => {
    var messageCard = document.createElement("div");
    messageCard.className = "message-card";
    var messageTopic = document.createElement("div");
    messageTopic.textContent = "topic: " + message.topic;
    messageTopic.className = "text-muted small";
    messageCard.appendChild(messageTopic);
    var messageText = document.createElement("div");
    messageText.textContent = message.text;
    messageCard.appendChild(messageText);
    var messageDate = document.createElement("div");
    messageDate.className = "text-muted small";
    messageDate.textContent = message.date;
    messageCard.appendChild(messageDate);
    messagesContainer.appendChild(messageCard);
  });
  // Scroll to the bottom of the messages container
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateCallsUIList(messages) {
  var messagesContainer = document.getElementById("defined-calls-list");
  // messagesContainer.innerHTML = '';  // Clear the existing messages
  messages.forEach((message) => {
    // create a li element

    var li = document.createElement("li");
    li.className = "list-group-item";
    li.textContent = message;

    messagesContainer.appendChild(li);
  });
  // Scroll to the bottom of the messages container
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideModal(id) {
  var modal = document.getElementById(id);
  modal.classList.remove("show");
  modal.classList.add("fade");
  var backdrop = document.querySelector(".modal-backdrop");
  if (backdrop) {
    backdrop.parentNode.removeChild(backdrop);
  }
}
