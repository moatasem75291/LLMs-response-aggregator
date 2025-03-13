// utils/formatters.js
export const formatTimestamp = (timestamp) => {
  if (!timestamp) return "";

  try {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
  } catch (e) {
    return timestamp;
  }
};

export const formatScore = (score) => {
  if (typeof score !== "number") return "?";
  return (score * 100).toFixed(1) + "%";
};
