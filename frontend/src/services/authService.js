const GATEWAY_API_URL  = import.meta.env.VITE_API_BASE_URL;
export async function registerUser(data) {
  const response = await fetch(`${GATEWAY_API_URL}/auth/register/`, {
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
  const response = await fetch(`${GATEWAY_API_URL}/auth/login/`, {
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


