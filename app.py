from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  
        password='', 
        database='room_management'
    )
    return connection

# 1. Browse all available rooms
@app.route('/')
def browse_rooms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()
    conn.close()
    return render_template('browse_rooms.html', rooms=rooms)

# 2. Update room information
@app.route('/update_room/<int:room_id>', methods=['GET', 'POST'])
def update_room(room_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        room_name = request.form['room_name']
        room_type = request.form['room_type']
        capacity = request.form['capacity']
        price = request.form['price']
        description = request.form['description']

        cursor.execute("""
            UPDATE rooms
            SET room_name = %s, room_type = %s, capacity = %s, price = %s, description = %s
            WHERE room_id = %s
        """, (room_name, room_type, capacity, price, description, room_id))

        conn.commit()
        conn.close()
        return redirect(url_for('browse_rooms'))

    cursor.execute('SELECT * FROM rooms WHERE room_id = %s', (room_id,))
    room = cursor.fetchone()
    conn.close()
    return render_template('update_room.html', room=room)

# 3. Insert new room
@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_name = request.form['room_name']
        room_type = request.form['room_type']
        capacity = request.form['capacity']
        price = request.form['price']
        description = request.form['description']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rooms (room_name, room_type, capacity, price, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (room_name, room_type, capacity, price, description))

        conn.commit()
        conn.close()
        return redirect(url_for('browse_rooms'))

    return render_template('add_room.html')

# 4. View room details
@app.route('/view_room/<int:room_id>')
def view_room(room_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM rooms WHERE room_id = %s', (room_id,))
    room = cursor.fetchone()
    conn.close()
    return render_template('view_room.html', room=room)

if __name__ == '__main__':
    app.run(debug=True)
