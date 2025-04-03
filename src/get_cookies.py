import pathlib, shutil, sqlite3


# cookies part -------------------------------------------------------------

# Define the path to the Firefox profile's cookies database
profile_path = pathlib.Path.home() / ".mozilla/firefox" / "fsaqzro1.default-esr"
cookies_db = profile_path / "cookies.sqlite"


# Copy the locked database to a temporary file
temp_db = profile_path / "temp_cookies.sqlite"
shutil.copy2(cookies_db, temp_db)

# Connect to the SQLite database
conn = sqlite3.connect(temp_db)
cursor = conn.cursor()

# Query to get all cookies
cursor.execute("SELECT host, name, path, value, expiry FROM moz_cookies")

cookies = cursor.fetchall() # simple list of tuples
conn.close()

# Optionally, remove the temporary file after use
temp_db.unlink()

#print(cookies)  # This prints extracted cookies

# cookies part end -----------------------------------------------------------

