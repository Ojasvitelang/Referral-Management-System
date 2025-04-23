document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  console.log("Attempting login for:", username);

  const res = await fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include", // VERY IMPORTANT for Flask session!
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  console.log("Login response status:", res.status);
  console.log("Login response data:", data);

  if (res.ok) {
    const role = data.user.role;
    console.log("Login successful. Redirecting to:", role === "admin" ? "/admin" : "/dashboard");

    if (role === "admin") {
      window.location.href = "/admin";
    } else {
      sessionStorage.setItem("username", data.user.username);
      window.location.href = "/dashboard";
    }
  } else {
    const errorMsg = data.error || "Login failed";
    console.error("Login failed:", errorMsg);
    document.getElementById("errorMsg").innerText = errorMsg;
  }
});
