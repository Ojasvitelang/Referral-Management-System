// Load and display pending referrals
function loadReferrals() {
  fetch("/referrals/admin")
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector("#referralTable tbody");
      tbody.innerHTML = "";

      const pending = data.referrals.filter(ref => ref.status === "Pending");
      pending.forEach(ref => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${ref.name}</td>
          <td>${ref.phone}</td>
          <td>${ref.city}</td>
          <td>${ref.status}</td>
          <td>
            <button onclick="approveReferral('${ref.id}')">Approve</button>
            <button onclick="rejectReferral('${ref.id}')">Reject</button>
          </td>
        `;

        tbody.appendChild(row);
      });
    })
    .catch(err => {
      console.error("Failed to load referrals:", err);
      alert("Unable to load referral list.");
    });
}

// Approve referral
function approveReferral(referralId) {
  const admission_amount = prompt("Enter admission amount:");
  if (!admission_amount || isNaN(admission_amount)) {
    alert("Invalid admission amount");
    return;
  }

  fetch("/approve_referral", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ referral_id: referralId, admission_amount })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert("Error: " + data.error);
      } else {
        alert("Referral approved!");
        loadReferrals();
      }
    })
    .catch(err => {
      console.error("Approval failed:", err);
      alert("Error approving referral.");
    });
}

// Reject referral
function rejectReferral(referralId) {
  if (!confirm("Are you sure you want to reject this referral?")) return;

  fetch("/reject_referral", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ referral_id: referralId })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert("Error: " + data.error);
      } else {
        alert("Referral rejected.");
        loadReferrals();
      }
    })
    .catch(err => {
      console.error("Rejection failed:", err);
      alert("Error rejecting referral.");
    });
}

// Create user
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

// Simulated CSV download for dev testing
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

// 🔥 Final Feature: Handle Report Form Submit
document.getElementById("reportForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const start = document.getElementById("startDate").value;
  const end = document.getElementById("endDate").value;

  if (!start || !end) {
    alert("Please select both start and end dates.");
    return;
  }

  fetch(`/generate_report?start=${start}&end=${end}`)
    .then(res => res.blob())
    .then(blob => {
      const link = document.getElementById("downloadLink");
      link.href = URL.createObjectURL(blob);
      link.download = `referral_report_${start}_to_${end}.csv`;
      link.style.display = "inline-block";
      link.click();
    })
    .catch(err => {
      console.error("Report generation failed:", err);
      alert("Unable to generate report.");
    });
});

// Load referrals on page load
loadReferrals();
