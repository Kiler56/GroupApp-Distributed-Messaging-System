export const navigateToMessages = (groupId: string) => {
  const baseUrl = import.meta.env.VITE_MESSAGES_URL || "http://localhost:5500";
  window.location.href = `${baseUrl}/index.html?group_id=${groupId}`;
}
