
const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";


function getToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }

  return localStorage.getItem("access_token");
}

function authHeaders(): HeadersInit {
  const token = getToken();

  return token
    ? {
        Authorization: `Bearer ${token}`,
      }
    : {};
}

export async function register(
  email: string,
  password: string
) {
  const response = await fetch(
    `${API_URL}/auth/register`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.text();

    throw new Error(
      `Registration failed (${response.status}): ${error}`
    );
  }

  return response.json();
}

export async function login(
  email: string,
  password: string
) {
  const response = await fetch(
    `${API_URL}/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.text();

    throw new Error(
      `Login failed (${response.status}): ${error}`
    );
  }

  const data = await response.json();

  localStorage.setItem(
    "access_token",
    data.access_token
  );

  return data;
}
export function logout() {
  localStorage.removeItem("access_token");
}
export async function uploadDocument(
  file: File
) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_URL}/documents/upload`,
    {
      method: "POST",
      headers: {
        ...authHeaders(),
      },
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.text();

    throw new Error(
      `Upload failed (${response.status}): ${error}`
    );
  }

  return response.json();
}

export async function getDocuments() {
  const response = await fetch(
    `${API_URL}/documents`,
    {
      headers: {
        ...authHeaders(),
      },
    }
  );

  if (!response.ok) {
    const error = await response.text();

    throw new Error(
      `Failed to fetch documents (${response.status}): ${error}`
    );
  }

  return response.json();
}
export async function sendChat(
  documentId: string,
  message: string,
  sessionId?: string
) {
  const response = await fetch(
    `${API_URL}/documents/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        ...authHeaders(),
      },

      body: JSON.stringify({
        document_id: documentId,
        message,
        history: [],
        session_id: sessionId || null,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.text();

    throw new Error(
      `Chat request failed (${response.status}): ${error}`
    );
  }

  return response.json();
}
export async function getChatHistory(
  sessionId: string
) {
  const response = await fetch(
    `${API_URL}/documents/chat/${sessionId}`
  );

  if (!response.ok) {
    const error = await response.text();

    throw new Error(
      `Failed to fetch chat history (${response.status}): ${error}`
    );
  }

  return response.json();
}

export async function deleteDocument(
  documentId: string
) {
  const response = await fetch(
    `${API_URL}/documents/${documentId}`,
    {
      method: "DELETE",
      headers: {
        ...authHeaders(),
      },
    }
  );

  if (!response.ok) {
    const error = await response.text();

    throw new Error(
      `Delete failed (${response.status}): ${error}`
    );
  }

  return response.json();
}
