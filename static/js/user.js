// Load referral list
function loadReferrals() {
  fetch("data/referrals.json")
    .then(res => res.json())
    .then(data => {
      // Optionally show user data if you pass it from Flask template
      const table = document.getElementById("referralTable");
      table.innerHTML = `
        <tr>
          <th>Name</th><th>Status</th><th>Points</th><th>Course</th><th>City</th>
        </tr>`;
      data.referrals.forEach(ref => {
        table.innerHTML += `
          <tr>
            <td>${ref.name}</td>
            <td>${ref.status}</td>
            <td>${ref.points_awarded}</td>
            <td>${ref.course_interested}</td>
            <td>${ref.city}</td>
          </tr>`;
      });
    });
}
loadReferrals();

// Handle referral form submit
document.getElementById("referralForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const form = e.target;
  const referral = {
    name: form.name.value,
    city: form.city.value,
    phone: form.phone.value,
    email: form.email.value,
    qualification: form.qualification.value,
    course_interested: form.course.value,
    relationship: form.relationship.value,
    referrer: "CURRENT_SESSION_USER"  // Optional: can be passed from Flask
  };

  console.log("Submitting referral:", referral);
  alert("Referral submitted (simulated)");
  form.reset();
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
