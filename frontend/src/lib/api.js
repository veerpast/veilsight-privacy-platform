const readError = async (response) => {
  try {
    const body = await response.json();
    return body.detail || "The request could not be completed.";
  } catch {
    return "The local analysis service is not responding.";
  }
};

export async function getDetectorStatus() {
  const response = await fetch("/api/detectors");
  if (!response.ok) throw new Error(await readError(response));
  return response.json();
}

export async function analyzeImage(file, settings) {
  const form = new FormData();
  form.append("file", file);
  Object.entries(settings).forEach(([key, value]) => form.append(key, String(value)));
  const response = await fetch("/api/analyze", { method: "POST", body: form });
  if (!response.ok) throw new Error(await readError(response));
  return response.json();
}

export async function benchmarkImage(file, confidence) {
  const form = new FormData();
  form.append("file", file);
  form.append("confidence", String(confidence));
  const response = await fetch("/api/benchmark", { method: "POST", body: form });
  if (!response.ok) throw new Error(await readError(response));
  return response.json();
}

export async function analyzeVideo(file, settings) {
  const form = new FormData();
  form.append("file", file);
  Object.entries(settings).forEach(([key, value]) => form.append(key, String(value)));
  const response = await fetch("/api/analyze/video", { method: "POST", body: form });
  if (!response.ok) throw new Error(await readError(response));
  const metrics = JSON.parse(response.headers.get("X-VeilSight-Metrics") || "{}");
  return { url: URL.createObjectURL(await response.blob()), metrics };
}
