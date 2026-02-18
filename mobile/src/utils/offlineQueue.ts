import AsyncStorage from "@react-native-async-storage/async-storage";

const KEY = "cropic_upload_queue_v1";

export type UploadQueueItem = {
  id: string;
  userId: string;
  farmId: string;
  latitude: number;
  longitude: number;
  capturedAt: string;
  deviceId: string;
  language?: string;
  district?: string;
  village?: string;
  blurScore?: number;
  localUri: string;
};

export async function enqueue(item: UploadQueueItem): Promise<void> {
  const existing = await AsyncStorage.getItem(KEY);
  const list = existing ? (JSON.parse(existing) as UploadQueueItem[]) : [];
  list.push(item);
  await AsyncStorage.setItem(KEY, JSON.stringify(list));
}

export async function dequeueAll(): Promise<UploadQueueItem[]> {
  const existing = await AsyncStorage.getItem(KEY);
  const list = existing ? (JSON.parse(existing) as UploadQueueItem[]) : [];
  await AsyncStorage.removeItem(KEY);
  return list;
}

export async function listQueue(): Promise<UploadQueueItem[]> {
  const existing = await AsyncStorage.getItem(KEY);
  return existing ? (JSON.parse(existing) as UploadQueueItem[]) : [];
}
