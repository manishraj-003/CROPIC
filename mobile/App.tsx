import { SafeAreaView, StyleSheet, Text, View } from "react-native";
import { CaptureScreen } from "./src/screens/CaptureScreen";

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>CROPIC Field Capture</Text>
        <Text style={styles.subtitle}>Guided photo capture with quality checks</Text>
      </View>
      <CaptureScreen />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f1e7",
    paddingHorizontal: 16,
    paddingTop: 12,
  },
  header: {
    marginBottom: 12,
  },
  title: {
    fontSize: 24,
    fontWeight: "800",
    color: "#1e3428",
  },
  subtitle: {
    marginTop: 4,
    fontSize: 14,
    color: "#496056",
  },
});
