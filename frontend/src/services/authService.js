const USER_SERVICE_BASE = "http://localhost:8000/auth";

/* REGISTER */
export async function registerUser(data) {
  const response = await fetch(`${USER_SERVICE_BASE}/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData.email?.[0] ||
      errorData.full_name?.[0] ||
      errorData.password?.[0] ||
      "Registration failed"
    );
  }

  return response.json();
}

/* LOGIN */
export async function loginUser(data) {
  const response = await fetch(`${USER_SERVICE_BASE}/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Invalid email or password");
  }

  return response.json(); // { access, refresh }
}
