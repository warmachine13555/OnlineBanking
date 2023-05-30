import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('userdata.db')
cursor = conn.cursor()

def delete_user(username):
    # Execute the DELETE query
    cursor.execute("DELETE FROM userdata WHERE username=?", (username,))
    conn.commit()
    print(f"Deleted user '{username}' successfully.")

# Get the username from the user
username_to_delete = input("Enter the username to delete: ")

# Call the delete_user function
delete_user(username_to_delete)

# Close the database connection
conn.close()
