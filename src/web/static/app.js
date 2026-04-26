const form = document.getElementById("completion-form");
const userQueryInput = document.getElementById("user-query");
const dataInput = document.getElementById("data");
const submitBtn = document.getElementById("submit-btn");
const clearBtn = document.getElementById("clear-btn");
const responseBox = document.getElementById("response-box");
const healthPill = document.getElementById("health-pill");
const toast = document.getElementById("toast");
const sampleRequest = document.getElementById("sample-request");
const sampleTemplate = document.getElementById("sample-request-template");

if (sampleRequest && sampleTemplate) {
  sampleRequest.textContent = sampleTemplate.innerHTML.trim();
}

async function checkHealth() {
  try {
    const response = await fetch("/health");
    if (!response.ok) {
      throw new Error(`Health check failed with status ${response.status}`);
    }
    healthPill.textContent = "Healthy";
    healthPill.classList.add("ok");
    healthPill.classList.remove("error");
  } catch (error) {
    healthPill.textContent = "Unavailable";
    healthPill.classList.add("error");
    healthPill.classList.remove("ok");
    showToast("Health endpoint is not reachable.", true);
  }
}

function withTimeout(ms) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  return {
    signal: controller.signal,
    cancel: () => clearTimeout(timer),
  };
}

function showToast(message, isError = false) {
  toast.textContent = message;
  toast.classList.toggle("error", isError);
}

function setBusy(isBusy) {
  submitBtn.disabled = isBusy;
  clearBtn.disabled = isBusy;
  submitBtn.textContent = isBusy ? "Running..." : "Send to /completion";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    user_query: userQueryInput.value.trim(),
    data: dataInput.value.trim() || null,
  };

  if (!payload.user_query) {
    showToast("User query is required.", true);
    return;
  }

  setBusy(true);
  responseBox.textContent = "Waiting for response...";
  showToast("Sending request to /completion");
  let cancelTimeout = () => {};

  try {
    const timeout = withTimeout(45000);
    cancelTimeout = timeout.cancel;
    const response = await fetch("/completion", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      signal: timeout.signal,
    });
    timeout.cancel();

    const contentType = response.headers.get("content-type") || "";
    const isJson = contentType.includes("application/json");
    const body = isJson ? await response.json() : await response.text();

    if (!response.ok) {
      const message = isJson ? JSON.stringify(body, null, 2) : String(body);
      throw new Error(message);
    }

    responseBox.textContent = body.response || "No response field found.";
    showToast("Request completed successfully.");
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    const finalMessage = message.includes("aborted")
      ? "Request timed out after 45s. Try a shorter prompt or check backend speed."
      : message;
    responseBox.textContent = `Request failed:\n${finalMessage}`;
    showToast("Completion request failed. Check server logs or model config.", true);
  } finally {
    cancelTimeout();
    setBusy(false);
  }
});

clearBtn.addEventListener("click", () => {
  userQueryInput.value = "";
  dataInput.value = "";
  responseBox.textContent = "No response yet.";
  showToast("Inputs cleared.");
  userQueryInput.focus();
});

checkHealth();
