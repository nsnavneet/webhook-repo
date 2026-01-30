function fmt(e) {
  const ts = e.timestamp || "";
  if (e.action === "PUSH") return `${e.author} pushed to ${e.to_branch} on ${ts}`;
  if (e.action === "PULL_REQUEST") return `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch} on ${ts}`;
  if (e.action === "MERGE") return `${e.author} merged branch ${e.from_branch} to ${e.to_branch} on ${ts}`;
  return JSON.stringify(e);
}

async function load() {
  const status = document.getElementById("status");
  try {
    const res = await fetch("/events");
    const data = await res.json();
    const list = document.getElementById("list");
    list.innerHTML = "";
    data.reverse().forEach(e => {
      const li = document.createElement("li");
      li.textContent = fmt(e);
      list.appendChild(li);
    });
    status.textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
  } catch (err) {
    status.textContent = "Error loading events";
  }
}

load();
setInterval(load, 15000);
