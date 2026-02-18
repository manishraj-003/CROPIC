import { useEffect, useMemo, useState } from "react";
import { Button, StyleSheet, Text, TextInput, View } from "react-native";
import { GhostOverlay } from "../components/GhostOverlay";
import { estimateBlurScore, isBlurry } from "../utils/blur";
import { dequeueAll, enqueue, listQueue } from "../utils/offlineQueue";
import { getCurrentCoords } from "../utils/geotag";
import { getToken, setToken } from "../utils/authToken";
import { uploadMetadata } from "../utils/api";
import { captureImageUri } from "../utils/camera";

export function CaptureScreen() {
  const [message, setMessage] = useState("Ready to capture");
  const [tokenInput, setTokenInput] = useState("");
  const [queueCount, setQueueCount] = useState(0);
  const [capturedUri, setCapturedUri] = useState<string | null>(null);
  const blurScore = useMemo(() => estimateBlurScore([9, 15, 12, 19, 8]), []);
  const blocked = isBlurry(blurScore);

  useEffect(() => {
    refreshQueueCount();
  }, []);

  async function refreshQueueCount() {
    const items = await listQueue();
    setQueueCount(items.length);
  }

  async function saveOffline() {
    const uri = capturedUri ?? "file://placeholder.jpg";
    const coords = await getCurrentCoords();
    await enqueue({
      id: `local-${Date.now()}`,
      userId: "U1",
      farmId: "farm-demo",
      latitude: coords?.latitude ?? 0,
      longitude: coords?.longitude ?? 0,
      capturedAt: new Date().toISOString(),
      deviceId: "DEV-1",
      language: "hi",
      district: "karnal",
      village: "sample-village",
      blurScore,
      localUri: uri,
    });
    setMessage("Saved to offline queue");
    refreshQueueCount();
  }

  async function uploadNow() {
    try {
      const token = await getToken();
      if (!token) {
        setMessage("Set JWT token first");
        return;
      }
      const coords = await getCurrentCoords();
      if (!capturedUri) {
        setMessage("Capture image first");
        return;
      }
      await uploadMetadata(
        {
          user_id: "U1",
          farm_id: "farm-demo",
          latitude: coords?.latitude ?? 0,
          longitude: coords?.longitude ?? 0,
          captured_at: new Date().toISOString(),
          device_id: "DEV-1",
          blur_score: blurScore,
          language: "hi",
          district: "karnal",
          village: "sample-village",
        },
        token
      );
      setMessage("Upload successful");
    } catch (err) {
      setMessage(`Upload failed: ${String(err)}`);
    }
  }

  async function syncOffline() {
    const token = await getToken();
    if (!token) {
      setMessage("Set JWT token first");
      return;
    }
    const items = await dequeueAll();
    let success = 0;
    for (const item of items) {
      try {
        await uploadMetadata(
          {
            user_id: item.userId,
            farm_id: item.farmId,
            latitude: item.latitude,
            longitude: item.longitude,
            captured_at: item.capturedAt,
            device_id: item.deviceId,
            blur_score: item.blurScore,
            language: item.language,
            district: item.district,
            village: item.village,
          },
          token
        );
        success += 1;
      } catch {
        await enqueue(item);
      }
    }
    await refreshQueueCount();
    setMessage(`Synced ${success}/${items.length} offline items`);
  }

  return (
    <View style={styles.card}>
      <GhostOverlay />
      <TextInput
        style={styles.input}
        placeholder="Paste JWT token"
        value={tokenInput}
        onChangeText={setTokenInput}
      />
      <Button
        title="Capture Image"
        onPress={async () => {
          const uri = await captureImageUri();
          setCapturedUri(uri);
          setMessage(uri ? "Image captured" : "Capture cancelled or permission denied");
        }}
      />
      <Button
        title="Save Token"
        onPress={async () => {
          await setToken(tokenInput.trim());
          setMessage("Token saved");
          refreshQueueCount();
        }}
      />
      <Text style={styles.message}>Captured: {capturedUri ? "yes" : "no"}</Text>
      <Text style={styles.metric}>Blur score: {blurScore.toFixed(2)}</Text>
      <Text style={[styles.status, blocked ? styles.bad : styles.good]}>
        {blocked ? "Image too blurry. Retake required." : "Image quality check passed."}
      </Text>
      <Button title="Upload" disabled={blocked} onPress={uploadNow} />
      <Button title="Save Offline" onPress={saveOffline} />
      <Button title="Sync Offline Queue" onPress={syncOffline} />
      <Text style={styles.metric}>Offline queue: {queueCount}</Text>
      <Text style={styles.message}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#fff",
    borderRadius: 16,
    padding: 14,
    borderWidth: 1,
    borderColor: "#d7dfd7",
    gap: 10,
  },
  metric: {
    color: "#344239",
    fontWeight: "700",
  },
  input: {
    borderWidth: 1,
    borderColor: "#d7dfd7",
    borderRadius: 8,
    paddingHorizontal: 8,
    paddingVertical: 6,
    backgroundColor: "#fff",
  },
  status: {
    fontSize: 13,
    fontWeight: "700",
  },
  bad: {
    color: "#b84a3c",
  },
  good: {
    color: "#2f6b49",
  },
  message: {
    color: "#496056",
    fontSize: 12,
  },
});
