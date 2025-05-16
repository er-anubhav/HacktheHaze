import React, { useState } from 'react';
import Modal from './Modal';
import Masonry from './Masonry/Masonry';

export default function ImageGrid({ results }) {
  const [selectedImage, setSelectedImage] = useState(null);

  const flattenedData = Object.entries(results).flatMap(([url, images], groupIndex) =>
    images.map((imgUrl, imgIndex) => ({
      id: `${groupIndex}-${imgIndex}`,
      image: imgUrl,
      height: Math.floor(250 + Math.random() * 150),
    }))
  );

  return (
    <div className="w-full">
      <Masonry
        data={flattenedData}
        onClick={(imgUrl) => setSelectedImage(imgUrl)}
      />
      {selectedImage && (
        <Modal imageUrl={selectedImage} onClose={() => setSelectedImage(null)} />
      )}
    </div>
  );
}
