document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('image-upload');
    const previewImage = document.getElementById('preview-image');
    const previewContainer = document.getElementById('preview-container');
    const uploadIcon = document.getElementById('upload-icon');

    fileInput.addEventListener('change', function () {
        const file = fileInput.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();

            reader.onload = function (e) {
                previewImage.src = e.target.result;
                uploadIcon.style.display = 'none';
                previewContainer.style.display = 'flex';
            };

            reader.readAsDataURL(file);
        }
    });
});


