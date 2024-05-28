from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Połączenie z bazą danych
conn = psycopg2.connect(dbname="notes_db", user="postgres", password="password", host="localhost")
cursor = conn.cursor()

# Pobierz wszystkie notatki
@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    return jsonify(notes)

# Utwórz nową notatkę
@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data['title']
    content = data['content']

    cursor.execute('INSERT INTO notes (title, content) VALUES (%s, %s)', (title, content))
    conn.commit()

    return jsonify({'message': 'Notatka utworzona pomyślnie'})

# Pobierz konkretną notatkę
@app.route('/api/notes/<int:id>', methods=['GET'])
def get_note_by_id(id):
    cursor.execute('SELECT * FROM notes WHERE id = %s', (id,))
    note = cursor.fetchone()

    if note is None:
        return jsonify({'message': 'Notatka o podanym identyfikatorze nie istnieje'})

    return jsonify(note)

# Edytuj istniejącą notatkę
@app.route('/api/notes/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.get_json()
    title = data['title']
    content = data['content']

    cursor.execute('UPDATE notes SET title = %s, content = %s WHERE id = %s', (title, content, id))
    conn.commit()

    return jsonify({'message': 'Notatka zaktualizowana pomyślnie'})

# Usuń notatkę
@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    cursor.execute('DELETE FROM notes WHERE id = %s', (id,))
    conn.commit()

    return jsonify({'message': 'Notatka usunięta pomyślnie'})

if __name__ == '__main__':
    app.run(debug=True)