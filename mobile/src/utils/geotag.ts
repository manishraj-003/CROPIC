import * as Location from "expo-location";

export async function getCurrentCoords(): Promise<{ latitude: number; longitude: number } | null> {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== "granted") {
    return null;
  }

  const current = await Location.getCurrentPositionAsync({});
  return { latitude: current.coords.latitude, longitude: current.coords.longitude };
}
