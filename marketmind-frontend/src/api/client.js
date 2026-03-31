// Central API client for the frontend:
// - Sets backend base URL
// - Stores/reads JWT token in localStorage
// - Adds Authorization header automatically
// - Normalizes backend errors into one predictable Error object
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";
const TOKEN_KEY = "mm_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || "";
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request(path, { method = "GET", body, auth = true } = {}) {
  const headers = {
    "Content-Type": "application/json",
  };

  if (auth) {
    const token = getToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const message =
      data?.error?.message ||
      data?.message ||
      "Request failed";
    const error = new Error(message);
    error.status = response.status;
    error.code = data?.error?.code || "REQUEST_FAILED";
    error.details = data?.error?.details || null;
    throw error;
  }

  return data;
}

export const api = {
  get(path, options = {}) {
    return request(path, { ...options, method: "GET" });
  },
  post(path, body, options = {}) {
    return request(path, { ...options, method: "POST", body });
  },
  put(path, body, options = {}) {
    return request(path, { ...options, method: "PUT", body });
  },
};
