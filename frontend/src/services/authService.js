const GATEWAY_API_URL  = "http://localhost:8000/auth";
export async function registerUser(data) {
  const response = await fetch(`${GATEWAY_API_URL }/register/`, {
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
export async function loginUser(data) {
  const response = await fetch(`${GATEWAY_API_URL}/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error("Invalid email or password");
  }
  return response.json();
}


