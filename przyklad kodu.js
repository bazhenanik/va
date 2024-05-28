import React, { useState, useEffect } from 'react';

function NoteList() {
  const [notes, setNotes] = useState([]);

  // Pobierz notatki z API
  useEffect(() => {
    fetch('/api/notes')
      .then((response) => response.json())
      .then((data) => setNotes
