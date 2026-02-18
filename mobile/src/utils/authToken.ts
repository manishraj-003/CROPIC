import AsyncStorage from "@react-native-async-storage/async-storage";

const TOKEN_KEY = "cropic_jwt_token";

export async function getToken(): Promise<string> {
  const token = await AsyncStorage.getItem(TOKEN_KEY);
  return token || "";
}

export async function setToken(token: string): Promise<void> {
  await AsyncStorage.setItem(TOKEN_KEY, token);
}
