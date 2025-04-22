document.getElementById("factForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const statement = document.getElementById("statement").value;
  const res = await fetch("/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ statement })
  });
  const data = await res.json();
  let output = "";

  if (data.status === "true") {
    output = `✅ This seems to be true: "${data.fact}" (Confidence: ${(
      data.confidence * 100
    ).toFixed(2)}%)`;
  } else if (data.status === "false") {
    output = `❌ This might be false: ${data.fact} (Confidence: ${(
      data.confidence * 100
    ).toFixed(2)}%)`;
  } else {
    output = `⚠️ Error: ${data.message}`;
  }

  document.getElementById("result").innerText = output;
});
