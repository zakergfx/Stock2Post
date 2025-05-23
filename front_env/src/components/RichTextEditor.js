import React, { useState } from "react";
import ReactQuill from "react-quill";
import 'react-quill/dist/quill.snow.css';

const RichTextEditor = () => {
  const [value, setValue] = useState('');

  const modules = {
    toolbar: [
      ['bold'],                     // gras
      [{ 'list': 'bullet' }],       // puces                       // ligne horizontale (custom bouton à ajouter si besoin)
    ]
  };

  return (
    <ReactQuill 
      value={value} 
      onChange={setValue} 
      modules={modules}
      formats={['bold', 'list', 'bullet']}
    />
  );
};

export default RichTextEditor;
