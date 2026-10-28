document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const form = document.getElementById('generate-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    const resultsDiv = document.getElementById('results');
    const attemptsContainer = document.getElementById('attempts-container');
    const previewDiv = document.getElementById('final-document');
    const editorTextarea = document.getElementById('markdown-editor');
    
    // Tab Elements
    const tabPreview = document.getElementById('tab-preview');
    const tabEdit = document.getElementById('tab-edit');
    
    // Download Elements
    const downloadPdfBtn = document.getElementById('download-pdf-btn');
    const downloadMdBtn = document.getElementById('download-md-btn');
    const downloadTxtBtn = document.getElementById('download-txt-btn');
    
    // State
    let currentDocumentName = 'Agent_Document';
    
    // Generation Form Handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const topic = document.getElementById('topic').value;
        const notes = document.getElementById('notes').value;
        const max_attempts = document.getElementById('max_attempts').value;
        
        // Update document name based on topic
        currentDocumentName = topic.replace(/[^a-z0-9]/gi, '_').toLowerCase() || 'agent_document';
        
        // UI Loading state
        submitBtn.disabled = true;
        btnText.textContent = 'Engineering Output...';
        loader.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        attemptsContainer.innerHTML = '';
        previewDiv.innerHTML = '';
        editorTextarea.value = '';
        
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic, notes, max_attempts })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Render attempts
                data.attempts.forEach((attempt, index) => {
                    const reviewText = attempt.review.toLowerCase();
                    const isApproved = reviewText.includes('status: approved');
                    const statusClass = isApproved ? 'status-approved' : 'status-rejected';
                    const statusText = isApproved ? 'Approved' : 'Rejected';
                    
                    // Add slight delay for sequential animation
                    setTimeout(() => {
                        const attemptHTML = `
                            <div class="attempt-card fade-in">
                                <div class="attempt-header">
                                    <h3><i class="fa-solid fa-code-branch"></i> Iteration ${attempt.attempt}</h3>
                                    <span class="status-badge ${statusClass}">${statusText}</span>
                                </div>
                                <div class="review-content">${attempt.review}</div>
                            </div>
                        `;
                        attemptsContainer.insertAdjacentHTML('beforeend', attemptHTML);
                    }, index * 200);
                });
                
                // Set Editor Content
                editorTextarea.value = data.final_document;
                
                // Set Preview Content
                updatePreview();
                
                // Show results
                resultsDiv.classList.remove('hidden');
                
                // Scroll to results smoothly
                setTimeout(() => {
                    resultsDiv.scrollIntoView({ behavior: 'smooth' });
                }, 100);
            } else {
                alert('An error occurred while generating the document.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the server.');
        } finally {
            submitBtn.disabled = false;
            btnText.textContent = 'Generate Stunning Document';
            loader.classList.add('hidden');
        }
    });

    // Function to render markdown
    function updatePreview() {
        const rawMarkdown = editorTextarea.value;
        previewDiv.innerHTML = marked.parse(rawMarkdown);
    }
    
    // Sync preview when typing in editor
    editorTextarea.addEventListener('input', updatePreview);

    // Tab Switching Logic
    tabPreview.addEventListener('click', () => {
        tabPreview.classList.add('active');
        tabEdit.classList.remove('active');
        previewDiv.classList.add('active-view');
        editorTextarea.classList.remove('active-view');
    });

    tabEdit.addEventListener('click', () => {
        tabEdit.classList.add('active');
        tabPreview.classList.remove('active');
        editorTextarea.classList.add('active-view');
        previewDiv.classList.remove('active-view');
    });

    // Download Logic Helper
    function downloadFile(content, filename, type) {
        const blob = new Blob([content], { type: type });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    // Download Button Handlers
    downloadPdfBtn.addEventListener('click', () => {
        const content = document.getElementById('final-document');
        if (!content || content.innerHTML.trim() === '') return alert('Nothing to download yet!');
        
        // Ensure we are on preview tab before downloading
        tabPreview.click();
        
        const opt = {
            margin:       0.5,
            filename:     `${currentDocumentName}.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        
        // Add a temporary background to fix transparency issue in PDF
        const oldBg = content.style.background;
        content.style.background = '#18181b'; // Match surface-dark
        content.style.padding = '15px';
        
        html2pdf().set(opt).from(content).save().then(() => {
            // Restore original styles
            content.style.background = oldBg;
            content.style.padding = '2rem';
        });
    });

    downloadMdBtn.addEventListener('click', () => {
        const content = editorTextarea.value;
        if (!content) return alert('Nothing to download yet!');
        downloadFile(content, `${currentDocumentName}.md`, 'text/markdown');
    });

    downloadTxtBtn.addEventListener('click', () => {
        const content = editorTextarea.value;
        if (!content) return alert('Nothing to download yet!');
        downloadFile(content, `${currentDocumentName}.txt`, 'text/plain');
    });
});
