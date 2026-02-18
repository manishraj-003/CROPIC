// Lightweight Laplacian-like sharpness proxy for edge validation.
export function estimateBlurScore(intensityDeltas: number[]): number {
  if (!intensityDeltas.length) {
    return 0;
  }

  const absValues = intensityDeltas.map((v) => Math.abs(v));
  const avg = absValues.reduce((a, b) => a + b, 0) / absValues.length;
  return avg;
}

export function isBlurry(score: number, threshold = 12): boolean {
  return score < threshold;
}
