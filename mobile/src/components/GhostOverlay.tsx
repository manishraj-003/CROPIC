import { StyleSheet, Text, View } from "react-native";

export function GhostOverlay() {
  return (
    <View style={styles.overlay}>
      <View style={styles.frame} />
      <Text style={styles.hint}>Align crop inside frame and keep camera steady</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: {
    position: "relative",
    borderWidth: 1,
    borderColor: "#87a392",
    borderRadius: 16,
    padding: 10,
    backgroundColor: "#ffffffcc",
  },
  frame: {
    height: 200,
    borderWidth: 2,
    borderColor: "#2f6b49",
    borderStyle: "dashed",
    borderRadius: 12,
  },
  hint: {
    marginTop: 8,
    color: "#2f6b49",
    fontSize: 13,
    fontWeight: "600",
  },
});
