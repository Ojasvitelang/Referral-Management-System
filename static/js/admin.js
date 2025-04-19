// Handle new user creation
document.getElementById("newUserForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const form = e.target;

  const newUser = {
    username: form.username.value,
    password: form.password.value,
    name: form.name.value,
    gender: form.gender.value,
    qualification: form.qualification.value,
    courses_done: form.courses_done.value.split(",").map(c => c.trim()),
    phone: form.phone.value,
    email: form.email.value,
    city: form.city.value,
    tier: "Bronze",
    points: 0,
    referrals: []
  };

  try {
    const response = await fetch("/create_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(newUser)
    });

    const result = await response.json();
    if (response.ok) {
      alert("✅ User created successfully!");
      form.reset();
    } else {
      alert("❌ Error: " + (result.error || "Unknown error"));
    }
  } catch (err) {
    console.error("Failed to create user:", err);
    alert("❌ Network error");
  }
});

// Handle user CSV upload
function uploadUserCSV() {
  const fileInput = document.getElementById("userCsv");
  if (fileInput.files.length === 0) {
    alert("Please choose a CSV file.");
    return;
  }

  const file = fileInput.files[0];
  const reader = new FileReader();
  reader.onload = function (e) {
    const contents = e.target.result;
    console.log("User CSV Content:", contents);
    alert("User CSV uploaded (simulated)");
  };
  reader.readAsText(file);
}

// Simulate CSV report download
function downloadReport() {
  fetch("data/referrals.json")
    .then(res => res.json())
    .then(data => {
      let csv = "Referral ID,Referrer,Name,Phone,Email,Status,Course Interested,Created At,Converted At,Admission Amount,Points Awarded\n";
      data.referrals.forEach(ref => {
        csv += [
          ref.id,
          ref.referrer,
          ref.name,
          ref.phone,
          ref.email,
          ref.status,
          ref.course_interested,
          ref.created_at,
          ref.converted_at || "",
          ref.admission_amount || "",
          ref.points_awarded
        ].join(",") + "\n";
      });

      const blob = new Blob([csv], { type: "text/csv" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "referral_report.csv";
      link.click();
    });
}
