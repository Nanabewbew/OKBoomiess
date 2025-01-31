const ageGroupSelect = document.getElementById("age-group");
const startConversationButton = document.getElementById("start-conversation");
const chatSection = document.getElementById("chat-section");
const chatBox = document.getElementById("chat-box");
const userInputField = document.getElementById("user-input");
const sendMessageButton = document.getElementById("send-message");

let ageGroup = "";

// Start the conversation
startConversationButton.addEventListener("click", async () => {
  ageGroup = ageGroupSelect.value;
  if (!ageGroup) {
    alert("Please select an age group!");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ age_group: ageGroup }),
    });

    const data = await response.json();
    if (response.ok) {
      chatSection.style.display = "block";
      chatBox.innerHTML = `<p>${data.message}</p>`;
    } else {
      alert(`Error: ${data.error}`);
    }
  } catch (error) {
    console.error("Error starting conversation:", error);
  }
});

// Send a message
sendMessageButton.addEventListener("click", async () => {
  const userInput = userInputField.value.trim();
  if (!userInput) {
    alert("Please enter a message!");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ age_group: ageGroup, user_input: userInput }),
    });

    const data = await response.json();
    if (response.ok) {
      chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
      chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
      chatBox.scrollTop = chatBox.scrollHeight;
      userInputField.value = "";
    } else {
      alert(`Error: ${data.error}`);
    }
  } catch (error) {
    console.error("Error sending message:", error);
  }
});
