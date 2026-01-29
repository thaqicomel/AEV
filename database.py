import sqlite3

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create content table (for single text items like 'Our Mission')
    # Removed UNIQUE constraint on key for flexibility, but we will enforce it logically for single-value items
    c.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT NOT NULL,
            section TEXT NOT NULL,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            type TEXT DEFAULT 'text'
        )
    ''')
    
    # Create gallery table (for lists of images)
    # Gallery/Images table
    # Added title and description to support enhanced gallery features
    # Added subsection to support sub-service specific images (e.g., warehouse-management, bund-enhancement)
    c.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT NOT NULL,
            section TEXT NOT NULL,
            subsection TEXT,
            image_path TEXT NOT NULL,
            title TEXT,
            description TEXT
        )
    ''')
    
    # Check if we need to add columns to existing table (migration)
    try:
        c.execute("ALTER TABLE gallery ADD COLUMN title TEXT")
    except sqlite3.OperationalError:
        pass # Column likely exists
        
    try:
        c.execute("ALTER TABLE gallery ADD COLUMN description TEXT")
    except sqlite3.OperationalError:
        pass # Column likely exists
        
    try:
        c.execute("ALTER TABLE gallery ADD COLUMN subsection TEXT")
    except sqlite3.OperationalError:
        pass # Column likely exists

    # Create team_members table
    c.execute('''
        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            linkedin_url TEXT,
            image_path TEXT
        )
    ''')

    # Create Services table (Level 1)
    c.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            image_path TEXT
        )
    ''')

    # Create Sub-Services table (Level 2)
    c.execute('''
        CREATE TABLE IF NOT EXISTS sub_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (service_id) REFERENCES services (id) ON DELETE CASCADE
        )
    ''')

    # Create Sub-Service Images table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sub_service_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sub_service_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            FOREIGN KEY (sub_service_id) REFERENCES sub_services (id) ON DELETE CASCADE
        )
    ''')
    
    # Check if admin exists
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
        print("Default admin user created.")
        
    # Seed Text Content
    text_seeds = [
        ('index', 'hero', 'hero_title', 'Arena Empire Ventures'),
        ('index', 'hero', 'hero_subtitle', 'Your trusted 100% Bumiputera partner for comprehensive property and facility maintenance solutions across Malaysia.'),
        ('index', 'who_we_are', 'our_commitment', 'As the facilities and property management industry continues to evolve in Malaysia, Arena Empire Ventures remains committed to growth, innovation, and service excellence. Backed by a dedicated and professional workforce, we are constantly exploring new opportunities while maintaining the highest standards in all areas of our business.\n\nWe are ready to compete, contribute, and lead in providing dependable services and solutions that support the development of businesses and communities nationwide.'),
        ('index', 'who_we_are', 'our_mission', 'Our mission at Arena Empire Ventures is to deliver exceptional maintenance and management services that empower businesses to operate efficiently, reduce costs, and focus on their core operations — all while upholding the highest standards of quality, reliability, and professionalism.')
    ]
    
    for page, section, key, value in text_seeds:
        try:
            c.execute("INSERT INTO content (page, section, key, value) VALUES (?, ?, ?, ?)", (page, section, key, value))
        except sqlite3.IntegrityError:
            pass # Already exists

    # Seed Team Members (if empty)
    c.execute("SELECT COUNT(*) FROM team_members")
    if c.fetchone()[0] == 0:
        team_seeds = [
            ('Ahmad Zaki', 'Managing Director', 'https://www.linkedin.com/in/luqman-zaharin/', '/static/images/property/image1.png'),
            ('Sarah Tan', 'Operations Manager', 'https://www.linkedin.com/in/thaqiyuddin-mizan-046458216/', '/static/images/property/image2.png'),
            ('Raj Kumar', 'Facility Head', '', '/static/images/property/image3.png'),
            ('Mei Ling', 'Finance Director', '', '/static/images/property/image4.png')
        ]
        c.executemany("INSERT INTO team_members (name, role, linkedin_url, image_path) VALUES (?, ?, ?, ?)", team_seeds)

    # Seed Team Slideshow (if empty)
    c.execute("SELECT COUNT(*) FROM gallery WHERE section='team_slideshow'")
    if c.fetchone()[0] == 0:
        slideshow_seeds = [
            ('index', 'team_slideshow', '/static/images/property/image1.png'),
            ('index', 'team_slideshow', '/static/images/property/image2.png'),
            ('index', 'team_slideshow', '/static/images/property/image3.png'),
            ('index', 'team_slideshow', '/static/images/property/image4.png')
        ]
        c.executemany("INSERT INTO gallery (page, section, image_path) VALUES (?, ?, ?)", slideshow_seeds)

    # Seed Services for Specialized Maintenance (if empty)
    c.execute("SELECT COUNT(*) FROM services WHERE page='specialized-maintenance'")
    if c.fetchone()[0] == 0:
        # 1. Create a Service
        c.execute("INSERT INTO services (page, name, description, image_path) VALUES (?, ?, ?, ?)", 
                 ('specialized-maintenance', 'Landscaping Services', 'Professional landscaping and garden maintenance.', '/static/images/property/image1.png'))
        service_id = c.lastrowid
        
        # 2. Create Sub-Services
        c.execute("INSERT INTO sub_services (service_id, name, description) VALUES (?, ?, ?)", 
                 (service_id, 'Tree Trimming', 'Expert tree trimming to ensure safety and aesthetics.'))
        sub_id_1 = c.lastrowid
        
        c.execute("INSERT INTO sub_services (service_id, name, description) VALUES (?, ?, ?)", 
                 (service_id, 'Lawn Care', 'Regular lawn mowing and maintenance for a pristine look.'))
        sub_id_2 = c.lastrowid
        
        # 3. Add Images to Sub-Services
        c.executemany("INSERT INTO sub_service_images (sub_service_id, image_path) VALUES (?, ?)", [
            (sub_id_1, '/static/images/property/image2.png'),
            (sub_id_1, '/static/images/property/image3.png'),
            (sub_id_2, '/static/images/property/image4.png')
        ])

    conn.commit()
    conn.close()
    print("Database initialized.")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    init_db()
