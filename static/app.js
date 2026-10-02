const state = { task: "qa" };
const config = {
  qa: { label: "What would you like to know?", placeholder: "Example: Which is the largest ocean?", button: "Ask EduGenie →" },
  explain: { label: "Which topic should I explain?", placeholder: "Example: Explain the OSI model for a beginner", button: "Explain Topic →" },
  quiz: { label: "Paste a passage or topic for the quiz", placeholder: "Paste your study notes here...", button: "Generate Quiz →" },
  summarize: { label: "Paste the text you want to summarize", placeholder: "Paste a long educational passage here...", button: "Summarize →" },
  learn: { label: "What do you want to learn?", placeholder: "Example: SQL", button: "Build Learning Path →" }
};

const tabs = document.querySelectorAll(".tab");
const input = document.querySelector("#inputText");
const label = document.querySelector("#inputLabel");
const level = document.querySelector("#level");
const submit = document.querySelector("#submitBtn");
const result = document.querySelector("#result");
const body = document.querySelector("#resultBody");
const form = document.querySelector("#taskForm");

function setTask(task) {
  state.task = task;
  tabs.forEach(t => t.classList.toggle("active", t.dataset.task === task));
  label.textContent = config[task].label;
  input.placeholder = config[task].placeholder;
  submit.innerHTML = config[task].button;
  level.classList.toggle("hidden", task !== "learn");
  input.value = "";
  result.classList.add("hidden");
}
tabs.forEach(tab => tab.addEventListener("click", () => setTask(tab.dataset.task)));

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c]));
}

function renderQuiz(items) {
  return items.map((q, i) => `
    <div class="quiz-q" data-answer="${escapeHtml(q.answer)}">
      <h3>${i + 1}. ${escapeHtml(q.question)}</h3>
      ${q.options.map(o => `<button class="option">${escapeHtml(o)}</button>`).join("")}
      <div class="feedback"></div>
    </div>`).join("");
}

function wireQuiz() {
  document.querySelectorAll(".quiz-q").forEach(q => {
    const answer = q.dataset.answer;
    q.querySelectorAll(".option").forEach(btn => btn.addEventListener("click", () => {
      q.querySelectorAll(".option").forEach(x => x.disabled = true);
      const correct = btn.textContent === answer;
      btn.classList.add(correct ? "correct" : "wrong");
      if (!correct) q.querySelectorAll(".option").forEach(x => { if (x.textContent === answer) x.classList.add("correct"); });
      q.querySelector(".feedback").textContent = correct ? "Correct!" : `Correct answer: ${answer}. ${q.dataset.explanation || ""}`;
    }));
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  submit.disabled = true;
  submit.textContent = "Thinking...";
  result.classList.remove("hidden");
  body.textContent = "EduGenie is generating your answer...";
  try {
    let endpoint, payload;
    if (state.task === "qa") { endpoint = "/qa"; payload = { question: text }; }
    if (state.task === "explain") { endpoint = "/explain"; payload = { text }; }
    if (state.task === "quiz") { endpoint = "/quiz"; payload = { text }; }
    if (state.task === "summarize") { endpoint = "/summarize"; payload = { text }; }
    if (state.task === "learn") { endpoint = "/learn/recommendations"; payload = { topic: text, level: level.value }; }
    const response = await fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Request failed");
    if (state.task === "qa") body.textContent = data.answer;
    if (state.task === "explain") body.textContent = data.explanation;
    if (state.task === "summarize") body.textContent = data.summary;
    if (state.task === "learn") body.textContent = data.recommendations;
    if (state.task === "quiz") {
      if (data.quiz?.error) throw new Error(data.quiz.error);
      body.innerHTML = renderQuiz(data.quiz);
      wireQuiz();
    }
  } catch (error) {
    body.textContent = `Something went wrong: ${error.message}`;
  } finally {
    submit.disabled = false;
    submit.innerHTML = config[state.task].button;
  }
});

document.querySelector("#copyBtn").addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(body.innerText); document.querySelector("#copyBtn").textContent = "Copied!"; setTimeout(() => document.querySelector("#copyBtn").textContent = "Copy", 1200); } catch {}
});
