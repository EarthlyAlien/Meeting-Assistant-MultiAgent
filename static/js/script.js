document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('audioFile');
    const fileUpload = document.querySelector('.file-upload');
    const loading = document.getElementById('loading');
    const resultsSection = document.querySelector('.results-section');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    // Handle drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileUpload.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        fileUpload.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        fileUpload.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        fileUpload.classList.add('highlight');
    }

    function unhighlight() {
        fileUpload.classList.remove('highlight');
    }

    fileUpload.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        updateFileName();
    }

    // Update file name display
    fileInput.addEventListener('change', updateFileName);

    function updateFileName() {
        const fileName = fileInput.files[0]?.name;
        const span = fileUpload.querySelector('span');
        span.textContent = fileName || 'Choose audio file or drag it here';
    }

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        
        // Show loading spinner
        loading.style.display = 'flex';
        resultsSection.style.display = 'none';

        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'success') {
                // Update UI with results
                document.getElementById('summaryContent').innerHTML = formatMarkdown(data.results.summary.summary);
                document.getElementById('transcriptionContent').innerHTML = formatTranscription(data.results.transcription.transcription);
                document.getElementById('actionItemsContent').innerHTML = formatActionItems(data.results.action_items.action_items);
                
                // Show results section
                resultsSection.style.display = 'block';
                
                // Reset form
                form.reset();
                updateFileName();
            } else {
                showError(data.message);
            }
        } catch (error) {
            showError('An error occurred while processing the meeting recording.');
            console.error('Error:', error);
        } finally {
            loading.style.display = 'none';
        }
    });

    // Handle tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Add active class to clicked button and corresponding pane
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Helper functions
    function formatMarkdown(text) {
        if (!text) return '';
        // Basic markdown formatting
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    function formatTranscription(text) {
        if (!text) return '';
        return text
            .split('\n')
            .map(line => line.trim())
            .filter(line => line)
            .map(line => {
                const [speaker, ...content] = line.split(':');
                if (content.length) {
                    return `<p><strong>${speaker}:</strong> ${content.join(':')}</p>`;
                }
                return `<p>${line}</p>`;
            })
            .join('');
    }

    function formatActionItems(items) {
        if (!items || !items.length) {
            return '<p>No action items found.</p>';
        }

        return items
            .map((item, index) => `
                <div class="action-item">
                    <h3>Action Item ${index + 1}</h3>
                    <p><strong>Task:</strong> ${item.task || 'No task specified'}</p>
                    <p><strong>Assignee:</strong> ${item.assignee || 'Unassigned'}</p>
                    <p><strong>Deadline:</strong> ${item.deadline || 'No deadline'}</p>
                </div>
            `)
            .join('');
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        form.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }
}); 