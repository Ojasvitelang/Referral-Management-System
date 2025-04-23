function loadReferrals() {
  const username = document.getElementById("referralForm").dataset.username;

  fetch("/referrals/" + username)
    .then((res) => res.json())
    .then((data) => {
      const table = document.getElementById("referralTable");
      table.innerHTML = `
        <tr>
          <th>Name</th><th>Status</th><th>Points</th><th>Course</th><th>City</th>
        </tr>`;
      data.referrals.forEach((ref) => {
        table.innerHTML += `
          <tr>
            <td>${ref.name}</td>
            <td>${ref.status}</td>
            <td>${ref.points_awarded}</td>
            <td>${ref.course_interested}</td>
            <td>${ref.city}</td>
          </tr>`;
      });
    })
    .catch((err) => {
      console.error("Failed to load referrals:", err);
      alert("Unable to load referral data.");
    });
}
loadReferrals();

// Load user tier and points
function loadUserInfo() {
  const username = document.getElementById("referralForm").dataset.username;

  fetch("/user/" + username)
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("tier").textContent = data.tier || "N/A";
      document.getElementById("points").textContent = data.points || 0;
    })
    .catch((err) => {
      console.error("Failed to load user info:", err);
    });
}
loadUserInfo();

// Handle referral form submit
document
  .getElementById("referralForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const form = e.target;
    const username = form.dataset.username;

    const referral = {
      name: form.name.value,
      city: form.city.value,
      phone: form.phone.value,
      email: form.email.value,
      qualification: form.qualification.value,
      course_interested: form.course_interested.value,
      relationship: form.relationship.value,
      referrer: username,
    };

    console.log("Submitting referral:", referral);

    fetch("/submit_referral", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(referral),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert("Error: " + data.error);
        } else {
          alert("Referral submitted successfully!");
          form.reset();
          loadReferrals();  // Refresh list
          loadUserInfo();   // Update points/tier after submit
        }
      })
      .catch((error) => {
        console.error("Submission error:", error);
        alert("An error occurred while submitting the referral.");
      });
  });

// Simulated CSV upload
function uploadCSV() {
  const fileInput = document.getElementById("csvUpload");
  if (fileInput.files.length === 0) {
    alert("Please choose a CSV file.");
    return;
  }

  const file = fileInput.files[0];
  const reader = new FileReader();
  reader.onload = function (e) {
    const contents = e.target.result;
    console.log("CSV Contents:", contents);
    alert("CSV uploaded (simulated)");
  };
  reader.readAsText(file);
}
