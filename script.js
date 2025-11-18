const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const result = document.getElementById('result');
const summaryEl = document.getElementById('summary');
const keywordsEl = document.getElementById('keywords');
const sentimentEl = document.getElementById('sentiment');
const highlightsEl = document.getElementById('highlights');
const titleEl = document.getElementById('title');

uploadBtn.addEventListener('click', async () => {
  if (!fileInput.files.length) {
    alert('Please select a file (PDF or TXT)');
    return;
  }
  const file = fileInput.files[0];
  const form = new FormData();
  form.append('file', file);

  uploadBtn.disabled = true;
  uploadBtn.innerText = 'Processing...';

  try {
    const res = await fetch('http://192.168.43.222:5000/upload', {
      method: 'POST',
      body: form
    });
    const data = await res.json();
    if (res.ok) {
      result.classList.remove('hidden');
      titleEl.innerText = data.auto_title || 'Document Summary';
      summaryEl.innerText = data.summary || 'No summary returned';
      keywordsEl.innerText = (data.keywords || []).join(', ');
      sentimentEl.innerText = data.sentiment || 'Neutral';
      highlightsEl.innerHTML = '';
      (data.highlights || []).forEach(h => {
        const li = document.createElement('li');
        li.innerText = h;
        highlightsEl.appendChild(li);
      });
    } else {
      alert(data.error || 'An error occurred');
    }
  } catch (err) {
    alert('Server not reachable. Make sure backend is running at http://127.0.0.1:5000');
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.innerText = 'Upload & Summarize';
  }
});
