// components/ImageUploader.js
import { useState } from 'react';
import axios from 'axios';

function ImageUploader() {
  const [image, setImage] = useState(null);
  const [modifiedImage, setModifiedImage] = useState(null);

  const onImageChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setImage(event.target.files[0]);
    }
  };

  const onUpload = async () => {
    try {
      const formData = new FormData();
      formData.append('file', image);

      // Assuming the API route is /api/predict
        const response = await axios.post('http://127.0.0.1:8000/api/predict', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

      setModifiedImage(response.data.modified_image_url);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div>
      <input type="file" onChange={onImageChange} />
      <button onClick={onUpload}>Upload</button>
      {modifiedImage && <img src={modifiedImage} alt="Modified" />}
    </div>
  );
}

export default ImageUploader;
