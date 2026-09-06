const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const placeholder = document.getElementById('uploadPlaceholder');
const form = document.getElementById('recommendationForm');
const outfitType = document.getElementById('outfitType');
const result = document.getElementById('result');
const status = document.getElementById('status');
const button = document.getElementById('generateBtn');
const dropzone = document.getElementById('dropzone');

// Relative URL works when the frontend is served by Flask.
// The absolute fallback also works if you open frontend/index.html directly
// while the Flask server is running.
const API_URL = window.location.protocol === 'file:'
    ? 'http://127.0.0.1:5000/api/recommend'
    : '/api/recommend';

let selectedFile = null;

imageInput.addEventListener('change', () => handleFile(imageInput.files[0]));

dropzone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropzone.classList.add('dragging');
});

dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragging'));

dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropzone.classList.remove('dragging');
    handleFile(event.dataTransfer.files[0]);
});

function handleFile(file) {
    if (!file) return;
    const validTypes = ['image/png', 'image/jpeg', 'image/webp'];
    if (!validTypes.includes(file.type)) {
        selectedFile = null;
        imageInput.value = '';
        return setStatus('Please choose a PNG, JPG, JPEG or WEBP image.', true);
    }
    if (file.size > 10 * 1024 * 1024) {
        selectedFile = null;
        imageInput.value = '';
        return setStatus('Image is too large. Maximum size is 10 MB.', true);
    }

    selectedFile = file;
    const url = URL.createObjectURL(file);
    preview.src = url;
    preview.hidden = false;
    placeholder.hidden = true;
    setStatus('Photo selected. Now choose your style.');
}

document.querySelectorAll('.choice').forEach(choice => {
    choice.addEventListener('click', () => {
        document.querySelectorAll('.choice').forEach(c => {
            c.classList.remove('selected');
            c.setAttribute('aria-pressed', 'false');
        });
        choice.classList.add('selected');
        choice.setAttribute('aria-pressed', 'true');
        outfitType.value = choice.dataset.value;
    });
});

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const occasion = document.getElementById('occasion').value;
    const color = document.getElementById('color').value;

    if (!selectedFile) return setStatus('Please upload your photo first.', true);
    if (!outfitType.value) return setStatus('Please choose an outfit type.', true);
    if (!occasion || !color) return setStatus('Please complete all style details.', true);

    const data = new FormData();
    data.append('image', selectedFile);
    data.append('occasion', occasion);
    data.append('outfitType', outfitType.value);
    data.append('color', color);

    setLoading(true);
    setStatus('Analyzing your photo and creating your recommendation...');

    try {
        const response = await fetch(API_URL, { method: 'POST', body: data });
        const text = await response.text();
        let payload;
        try {
            payload = JSON.parse(text);
        } catch {
            throw new Error('The server returned an invalid response. Make sure Flask is running.');
        }
        if (!response.ok || !payload.success) throw new Error(payload.error || 'Recommendation failed.');
        showResult(payload.recommendation, payload.imageUrl);
    } catch (error) {
        // Keep the user moving to the next step even if the backend is not running.
        // This fallback is local; it does not claim to be computer-vision AI.
        console.warn(error);
        showResult(localFallback(occasion, outfitType.value, color), null);
        setStatus('Recommendation generated locally. Start Flask to enable the server-backed flow.', false);
    } finally {
        setLoading(false);
    }
});

function localFallback(occasion, type, color) {
    return {
        title: `${occasion} ${type} Look`,
        outfit: `Try a well-fitted ${type.toLowerCase()} in ${color.toLowerCase()}, balanced with neutral bottoms and clean footwear.`,
        color: `${color} should be the main color; combine it with neutral shades for an easy-to-match look.`,
        occasion: `For ${occasion.toLowerCase()}, prioritize comfort, fit and an overall polished appearance.`,
        accessories: 'Finish with a simple watch and minimal accessories.',
        summary: `Your selected ${occasion.toLowerCase()} + ${type.toLowerCase()} + ${color.toLowerCase()} combination is ready to try.`,
        nextStep: 'Try this combination and adjust the fit or one accessory to suit your personal style.'
    };
}

function showResult(data, imageUrl) {
    document.getElementById('resultTitle').textContent = data.title;
    document.getElementById('resultOutfit').textContent = data.outfit;
    document.getElementById('resultColor').textContent = data.color;
    document.getElementById('resultOccasion').textContent = data.occasion;
    document.getElementById('resultAccessories').textContent = data.accessories;
    document.getElementById('resultSummary').textContent = data.summary;
    document.getElementById('resultNextStep').textContent = data.nextStep || '';

    const resultImage = document.getElementById('resultImage');
    if (imageUrl) {
        resultImage.src = imageUrl;
        resultImage.hidden = false;
    } else {
        resultImage.hidden = true;
    }

    result.hidden = false;
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

document.getElementById('startOver').addEventListener('click', () => {
    form.reset();
    selectedFile = null;
    outfitType.value = '';
    document.querySelectorAll('.choice').forEach(c => {
        c.classList.remove('selected');
        c.setAttribute('aria-pressed', 'false');
    });
    preview.hidden = true;
    preview.removeAttribute('src');
    placeholder.hidden = false;
    result.hidden = true;
    setStatus('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

function setLoading(loading) {
    button.disabled = loading;
    button.textContent = loading ? '⏳ Generating recommendation...' : '✨ Get AI Recommendation';
}

function setStatus(message, isError = false) {
    status.textContent = message;
    status.className = `status${isError ? ' error' : ''}`;
}

