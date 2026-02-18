const API_BASE = "http://localhost:8000";

type UploadPayload = {
  user_id: string;
  farm_id: string;
  latitude: number;
  longitude: number;
  captured_at: string;
  device_id: string;
  blur_score?: number;
  language?: string;
  district?: string;
  village?: string;
};

export async function uploadMetadata(payload: UploadPayload, token: string): Promise<void> {
  const res = await fetch(`${API_BASE}/v1/images/metadata`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Upload failed: ${res.status} ${text}`);
  }
}
