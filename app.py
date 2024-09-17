# from flask import Flask, jsonify, render_template
# import sqlite3

# app = Flask(__name__)

# # Function to connect to the database
# def get_db_connection():
#     conn = sqlite3.connect('influencers.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# # Home route - renders HTML page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # API route to fetch influencer data
# @app.route('/api/influencers', methods=['GET'])
# def get_influencers():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM influencers LIMIT 100")  # Add pagination later
#     data = cursor.fetchall()
#     return jsonify([dict(row) for row in data])

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('influencers.db')
    conn.row_factory = sqlite3.Row  # This allows us to fetch results as dictionaries
    return conn

# Home route to serve HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API route to get influencers with pagination
@app.route('/api/influencers', methods=['GET'])
def get_influencers():
    conn = get_db_connection()
    
    # Get the page number from the request query parameter (default is 1)
    page = request.args.get('page', default=1, type=int)
    items_per_page = 100
    offset = (page - 1) * items_per_page

    # Query to select influencers with pagination (limit and offset)
    cursor = conn.execute('SELECT * FROM influencers LIMIT ? OFFSET ?', (items_per_page, offset))
    influencers = cursor.fetchall()

    # Query to count the total number of influencers in the table
    cursor = conn.execute('SELECT COUNT(*) FROM influencers')
    total_influencers = cursor.fetchone()[0]
    total_pages = (total_influencers + items_per_page - 1) // items_per_page

    conn.close()

    # Return the paginated results and total number of pages
    return jsonify({
        'influencers': [dict(row) for row in influencers],  # Convert row objects to dicts
        'total_pages': total_pages,
        'current_page': page
    })

if __name__ == '__main__':
    app.run(debug=True)
