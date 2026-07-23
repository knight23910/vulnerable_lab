from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from database import db, User, Post
import re
import hashlib
import os
import subprocess
import platform
from datetime import datetime
import uuid
import json
import mimetypes
from werkzeug.utils import secure_filename

# ============================================
# APP INITIALIZATION
# ============================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vulnerable_secret_key_12345_change_this_in_production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnerable_lab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}  # For demo only

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'warning'

# ============================================
# USER LOADER
# ============================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============================================
# CONTEXT PROCESSOR - Makes user info available globally
# ============================================
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_file_size(file_path):
    """Get file size in human readable format"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    return "0 B"

def get_file_icon(filename):
    """Get appropriate icon for file type"""
    ext = os.path.splitext(filename)[1].lower()
    icons = {
        '.txt': 'fa-file-alt',
        '.pdf': 'fa-file-pdf',
        '.doc': 'fa-file-word',
        '.docx': 'fa-file-word',
        '.xls': 'fa-file-excel',
        '.xlsx': 'fa-file-excel',
        '.ppt': 'fa-file-powerpoint',
        '.pptx': 'fa-file-powerpoint',
        '.jpg': 'fa-file-image',
        '.jpeg': 'fa-file-image',
        '.png': 'fa-file-image',
        '.gif': 'fa-file-image',
        '.mp4': 'fa-file-video',
        '.mp3': 'fa-file-audio',
        '.zip': 'fa-file-archive',
        '.rar': 'fa-file-archive',
        '.php': 'fa-file-code',
        '.html': 'fa-file-code',
        '.js': 'fa-file-code',
        '.css': 'fa-file-code',
        '.py': 'fa-file-code',
    }
    return icons.get(ext, 'fa-file')

def get_command_suggestions():
    """Get command suggestions based on OS"""
    is_windows = platform.system().lower() == 'windows'
    if is_windows:
        return [
            ('whoami', 'Show current user'),
            ('ipconfig', 'Show network configuration'),
            ('dir', 'List directory contents'),
            ('systeminfo', 'Show system information'),
            ('tasklist', 'Show running processes'),
            ('echo Hacked! & whoami', 'Multiple commands'),
            ('whoami & ipconfig', 'Combine commands'),
            ('ping 127.0.0.1', 'Ping localhost')
        ]
    else:
        return [
            ('whoami', 'Show current user'),
            ('ifconfig', 'Show network configuration'),
            ('ls -la', 'List directory contents'),
            ('uname -a', 'Show system information'),
            ('ps aux', 'Show running processes'),
            ('echo "Hacked!" && whoami', 'Multiple commands'),
            ('whoami && ifconfig', 'Combine commands'),
            ('ping 127.0.0.1', 'Ping localhost')
        ]

# ============================================
# ROUTES: PUBLIC
# ============================================

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

# ============================================
# VULNERABILITY 1: SQL INJECTION (Login Bypass)
# ============================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # ⚠️ VULNERABLE: Direct SQL query without parameterization
        query = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        app.logger.info(f"SQL Query: {query}")
        
        try:
            result = db.session.execute(text(query)).fetchone()
            
            if result:
                user = User.query.get(result[0])
                login_user(user)
                flash(f'✅ Welcome {user.username}! You successfully logged in!', 'success')
                
                # Log the successful login
                app.logger.info(f"User {user.username} logged in via SQL Injection")
                return redirect(url_for('dashboard'))
            else:
                flash('❌ Invalid credentials! Try: admin\' OR \'1\'=\'1', 'danger')
                app.logger.warning(f"Failed login attempt for username: {username}")
        except Exception as e:
            flash(f'⚠️ SQL Error: {str(e)}', 'danger')
            app.logger.error(f"SQL Error: {e}")
    
    return render_template('login.html')

# ============================================
# VULNERABILITY 2: XSS (Cross-Site Scripting)
# ============================================
@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('q', '')
    results = []
    search_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_count = 0
    
    if query:
        # ⚠️ VULNERABLE: No sanitization, raw output in template
        # Also vulnerable to SQL injection in search
        search_query = f"SELECT * FROM post WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"
        try:
            results = db.session.execute(text(search_query)).fetchall()
            result_count = len(results)
            app.logger.info(f"Search performed: '{query}' - Found {result_count} results")
        except Exception as e:
            flash(f'Search Error: {str(e)}', 'danger')
            app.logger.error(f"Search Error: {e}")
    
    return render_template('search.html', 
                         query=query, 
                         results=results, 
                         search_time=search_time,
                         result_count=result_count)

# ============================================
# VULNERABILITY 3: Weak Authentication & Session Management
# ============================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        confirm_password = request.form.get('confirm_password', '')
        
        # Check if passwords match
        if password != confirm_password:
            flash('❌ Passwords do not match!', 'danger')
            return render_template('register.html')
        
        # ⚠️ VULNERABILITY: No password complexity requirements
        # Weak password storage (basic hashing without salt)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Check if username exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('❌ Username already exists!', 'danger')
            return render_template('register.html')
        
        # Check if email exists (but no validation)
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('❌ Email already registered!', 'danger')
            return render_template('register.html')
        
        # ⚠️ VULNERABILITY: No email validation
        new_user = User(
            username=username, 
            password=hashed_password, 
            email=email,
            is_admin=False  # Never allow admin registration
        )
        db.session.add(new_user)
        db.session.commit()
        
        app.logger.info(f"New user registered: {username} with email: {email}")
        flash('✅ Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# ============================================
# VULNERABILITY 4: Command Injection
# ============================================
@app.route('/ping', methods=['GET', 'POST'])
@login_required
def ping():
    result = ''
    command_executed = ''
    is_injection = False
    suggestions = get_command_suggestions()
    
    if request.method == 'POST':
        command = request.form.get('ip', '').strip()
        
        if command:
            is_windows = platform.system().lower() == 'windows'
            command_executed = command
            
            try:
                # ⚠️ VULNERABILITY: Direct command execution
                # The user input is executed directly in shell
                # This is DANGEROUS and for educational purposes only
                
                # Check if it's a simple command or includes injection characters
                injection_chars = ['&', '|', ';', '>', '<', '&&', '||', '`', '$']
                has_injection = any(char in command for char in injection_chars)
                is_injection = has_injection
                
                # Build the command
                if is_windows:
                    if not has_injection and re.match(r'^(\d{1,3}\.){3}\d{1,3}$', command):
                        full_cmd = f'ping -n 4 {command}'
                    else:
                        full_cmd = command
                else:
                    if not has_injection and re.match(r'^(\d{1,3}\.){3}\d{1,3}$', command):
                        full_cmd = f'ping -c 4 {command}'
                    else:
                        full_cmd = command
                
                # Add a header to the output
                result = f"🖥️ Executing: {full_cmd}\n"
                result += "=" * 70 + "\n\n"
                
                # Execute the command
                output = subprocess.check_output(
                    full_cmd,
                    shell=True,
                    stderr=subprocess.STDOUT,
                    timeout=15,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                result += output
                
                # Check if command injection was used
                if has_injection:
                    result = f"🔓 COMMAND INJECTION SUCCESSFUL!\n" + "=" * 40 + "\n\n" + result
                    app.logger.warning(f"Command Injection detected: {command}")
                
                app.logger.info(f"Command executed: {full_cmd}")
                
            except subprocess.CalledProcessError as e:
                result = f"❌ Command failed (Exit code: {e.returncode})\n\n"
                result += f"📝 Error Output:\n{e.output}"
                app.logger.error(f"Command failed: {command}")
            except subprocess.TimeoutExpired:
                result = "⏱️ Command timed out after 15 seconds"
                app.logger.warning(f"Command timeout: {command}")
            except Exception as e:
                result = f"❌ Error: {str(e)}"
                app.logger.error(f"Command error: {e}")
        else:
            flash('⚠️ Please enter a command', 'warning')
    
    return render_template('ping.html', 
                         result=result, 
                         command_executed=command_executed, 
                         is_injection=is_injection,
                         suggestions=suggestions)

# ============================================
# VULNERABILITY 5: IDOR (Insecure Direct Object Reference)
# ============================================
@app.route('/profile/<username>')
@login_required
def profile(username):
    # ⚠️ VULNERABILITY: No access control - users can view any profile
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('dashboard'))
    
    posts = Post.query.filter_by(user_id=user.id).all()
    is_own_profile = (current_user.username == username)
    
    if not is_own_profile:
        app.logger.warning(f"IDOR attempt: User {current_user.username} viewed profile of {username}")
    
    return render_template('profile.html', 
                         user=user, 
                         posts=posts, 
                         is_own_profile=is_own_profile)

# ============================================
# VULNERABILITY 6: IDOR - View Posts
# ============================================
@app.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    # ⚠️ VULNERABILITY: No authorization check
    # Users can view any post regardless of ownership
    post = Post.query.get(post_id)
    if not post:
        flash('Post not found!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get author
    author = User.query.get(post.user_id)
    
    # Log potential IDOR
    if author and current_user.id != author.id:
        app.logger.warning(f"IDOR attempt: User {current_user.username} viewed post {post_id} owned by {author.username}")
    
    return render_template('post.html', post=post, author=author)

# ============================================
# VULNERABILITY 7: File Upload (Unrestricted)
# ============================================
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    uploaded_files = []
    upload_dir = app.config['UPLOAD_FOLDER']
    
    # Get list of uploaded files
    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, f)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                uploaded_files.append({
                    'name': f,
                    'size': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2),
                    'size_human': get_file_size(file_path),
                    'uploaded': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M'),
                    'icon': get_file_icon(f),
                    'type': mimetypes.guess_type(f)[0] or 'Unknown'
                })
    
    # Sort by upload date (newest first)
    uploaded_files.sort(key=lambda x: x['uploaded'], reverse=True)
    
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            # ⚠️ VULNERABILITY: No file type validation
            # No size limit, no content validation
            filename = file.filename
            
            # Security issue: Direct save without validation
            # Use secure_filename but in a vulnerable way
            safe_filename = secure_filename(filename)
            if not safe_filename:
                safe_filename = f"upload_{uuid.uuid4().hex[:8]}_{filename}"
            
            file_path = os.path.join(upload_dir, safe_filename)
            file.save(file_path)
            
            app.logger.info(f"File uploaded: {safe_filename} by {current_user.username}")
            flash(f'✅ File {safe_filename} uploaded successfully!', 'success')
            return redirect(url_for('upload_file'))
        else:
            flash('❌ No file selected!', 'danger')
    
    return render_template('upload.html', uploaded_files=uploaded_files)

# ============================================
# FILE DOWNLOAD (for uploaded files)
# ============================================
@app.route('/download/<filename>')
@login_required
def download_file(filename):
    # ⚠️ VULNERABILITY: No access control, anyone can download any file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        app.logger.info(f"File downloaded: {filename} by {current_user.username}")
        return send_file(file_path, as_attachment=True)
    else:
        flash('File not found!', 'danger')
        return redirect(url_for('upload_file'))

# ============================================
# DELETE FILE
# ============================================
@app.route('/delete_file/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    # ⚠️ VULNERABILITY: No access control
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        app.logger.info(f"File deleted: {filename} by {current_user.username}")
        flash(f'✅ File {filename} deleted successfully!', 'success')
    else:
        flash('File not found!', 'danger')
    return redirect(url_for('upload_file'))

# ============================================
# ADMIN PANEL
# ============================================
@app.route('/admin')
@login_required
def admin_panel():
    # ⚠️ VULNERABILITY: Weak admin check (can be bypassed)
    if current_user.is_admin:
        users = User.query.all()
        posts = Post.query.all()
        
        # Get system stats
        total_users = len(users)
        total_posts = len(posts)
        admin_users = len([u for u in users if u.is_admin])
        
        # Get upload stats
        upload_dir = app.config['UPLOAD_FOLDER']
        upload_count = len([f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))]) if os.path.exists(upload_dir) else 0
        
        # Get database size
        db_path = os.path.join('instance', 'vulnerable_lab.db')
        db_size = get_file_size(db_path) if os.path.exists(db_path) else "0 B"
        
        return render_template('admin.html', 
                             users=users, 
                             posts=posts,
                             total_users=total_users,
                             total_posts=total_posts,
                             admin_users=admin_users,
                             upload_count=upload_count,
                             db_size=db_size)
    else:
        flash('⚠️ Admin access required! (Hint: Try SQL injection in login)', 'warning')
        app.logger.warning(f"Unauthorized admin access attempt by {current_user.username}")
        return redirect(url_for('dashboard'))

# ============================================
# API: GET USERS (for admin)
# ============================================
@app.route('/api/users')
@login_required
def api_users():
    if current_user.is_admin:
        users = User.query.all()
        return jsonify([{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'is_admin': u.is_admin
        } for u in users])
    return jsonify({'error': 'Unauthorized'}), 403

# ============================================
# DASHBOARD
# ============================================
@app.route('/dashboard')
@login_required
def dashboard():
    posts = Post.query.all()
    total_posts = len(posts)
    total_users = User.query.count()
    
    # Get user stats
    user_posts = Post.query.filter_by(user_id=current_user.id).count()
    
    # Get recent posts (last 5)
    recent_posts = posts[-5:] if len(posts) > 5 else posts
    recent_posts.reverse()
    
    # Get vulnerabilities summary
    vulnerabilities = [
        {'name': 'SQL Injection', 'severity': 'Critical', 'status': 'Active'},
        {'name': 'XSS', 'severity': 'High', 'status': 'Active'},
        {'name': 'Command Injection', 'severity': 'Critical', 'status': 'Active'},
        {'name': 'IDOR', 'severity': 'Medium', 'status': 'Active'},
        {'name': 'File Upload', 'severity': 'Critical', 'status': 'Active'},
        {'name': 'Weak Auth', 'severity': 'Medium', 'status': 'Active'}
    ]
    
    return render_template('dashboard.html', 
                         posts=posts,
                         recent_posts=recent_posts,
                         username=current_user.username,
                         total_posts=total_posts,
                         total_users=total_users,
                         user_posts=user_posts,
                         vulnerabilities=vulnerabilities)

# ============================================
# LOGOUT
# ============================================
@app.route('/logout')
def logout():
    username = current_user.username if current_user.is_authenticated else 'Unknown'
    logout_user()
    flash('You have been logged out.', 'info')
    app.logger.info(f"User {username} logged out")
    return redirect(url_for('login'))

# ============================================
# CREATE POST (for demo)
# ============================================
@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if title and content:
            post = Post(title=title, content=content, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('✅ Post created successfully!', 'success')
            app.logger.info(f"New post created by {current_user.username}: {title}")
            return redirect(url_for('dashboard'))
        else:
            flash('❌ Title and content are required!', 'danger')
    
    return render_template('create_post.html')

# ============================================
# DELETE POST
# ============================================
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        # ⚠️ VULNERABILITY: No ownership check
        db.session.delete(post)
        db.session.commit()
        flash('✅ Post deleted successfully!', 'success')
        app.logger.info(f"Post {post_id} deleted by {current_user.username}")
    else:
        flash('Post not found!', 'danger')
    return redirect(url_for('dashboard'))

# ============================================
# SYSTEM INFO (for admin)
# ============================================
@app.route('/system_info')
@login_required
def system_info():
    if not current_user.is_admin:
        flash('Admin access required!', 'danger')
        return redirect(url_for('dashboard'))
    
    info = {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'python_version': platform.python_version(),
        'hostname': platform.node(),
        'processor': platform.processor(),
        'architecture': platform.architecture(),
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'app_version': '2.0.0',
    }
    
    return render_template('system_info.html', info=info)

# ============================================
# ERROR HANDLERS
# ============================================
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal Server Error: {error}")
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

# ============================================
# DATABASE INITIALIZATION
# ============================================
def create_sample_data():
    """Create sample data if it doesn't exist"""
    # Create uploads directory
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('instance', exist_ok=True)
    
    # Create sample admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password=generate_password_hash('admin123', method='pbkdf2:sha256'),
            email='admin@example.com',
            is_admin=True
        )
        db.session.add(admin)
        
        # Create sample users
        users_data = [
            ('rahul', 'rahul123', 'rahul@example.com', False),
            ('alice', 'alice123', 'alice@example.com', False),
            ('bob', 'bob123', 'bob@example.com', False),
            ('charlie', 'charlie123', 'charlie@example.com', False),
        ]
        
        for username, password, email, is_admin in users_data:
            user = User(
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                email=email,
                is_admin=is_admin
            )
            db.session.add(user)
        
        db.session.commit()
        
        # Get user IDs
        admin_id = admin.id
        rahul = User.query.filter_by(username='rahul').first()
        rahul_id = rahul.id if rahul else admin_id
        
        # Create sample posts
        posts = [
            Post(
                title='🚀 Welcome to Vulnerable Lab',
                content='This is a deliberately vulnerable application for learning security testing. Try to exploit SQL injection, XSS, and other vulnerabilities!',
                user_id=admin_id
            ),
            Post(
                title='🛡️ Security Tip: Always Validate Input',
                content='Never trust user input! Always sanitize and validate data. This is a great example of why XSS is dangerous. Always use parameterized queries and escape output.',
                user_id=rahul_id
            ),
            Post(
                title='🔓 SQL Injection Demo',
                content='Try logging in with: admin\' OR \'1\'=\'1. See what happens! This demonstrates how dangerous SQL injection can be. It allows attackers to bypass authentication and access sensitive data.',
                user_id=admin_id
            ),
            Post(
                title='💻 Command Injection Example',
                content='On Windows, try: whoami or ipconfig in the ping tool! On Linux, try: whoami or ifconfig. Command injection allows attackers to execute arbitrary system commands.',
                user_id=admin_id
            ),
            Post(
                title='🔍 IDOR Vulnerability Explained',
                content='Try accessing /profile/admin or /post/1, /post/2. Notice how you can view any user\'s data without authorization! IDOR occurs when an application exposes internal object references.',
                user_id=rahul_id
            ),
            Post(
                title='📁 File Upload Risks',
                content='Try uploading a PHP file or HTML file. The application accepts any file type without validation! This can lead to remote code execution and complete system compromise.',
                user_id=admin_id
            ),
            Post(
                title='🔑 Understanding Weak Authentication',
                content='Try registering with password "123" or email "invalid". The application has no password complexity requirements or email validation. This makes it vulnerable to brute force attacks.',
                user_id=rahul_id
            ),
            Post(
                title='🛡️ How to Fix These Vulnerabilities',
                content='1. Use parameterized queries for SQL\n2. Sanitize/escape HTML output for XSS\n3. Use proper input validation\n4. Implement proper access controls\n5. Use secure password hashing (bcrypt)\n6. Validate file types before upload',
                user_id=admin_id
            )
        ]
        
        db.session.add_all(posts)
        db.session.commit()
        
        app.logger.info("✅ Sample data created successfully!")
        print("✅ Sample data created successfully!")
        print("📊 Users created: admin, rahul, alice, bob, charlie")
        print("📝 Posts created: 8")
    else:
        print("📊 Sample data already exists.")

# ============================================
# MAIN ENTRY POINT
# ============================================
with app.app_context():
    # Create tables
    db.create_all()
    # Create sample data
    create_sample_data()

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Starting Vulnerable Lab - Enhanced Edition")
    print("=" * 70)
    print(f"📍 Access at: http://localhost:5000")
    print(f"📊 Admin Credentials: admin / admin123")
    print(f"📊 User Credentials: rahul / rahul123")
    print("\n🔓 SQL Injection Payload: admin' OR '1'='1")
    print("💻 Command Injection (Windows): whoami, ipconfig, dir")
    print("🐧 Command Injection (Linux): whoami, ifconfig, ls")
    print("⚠️  This application is intentionally vulnerable!")
    print("=" * 70)
    print("📁 Uploaded files stored in: ./uploads/")
    print("🗄️  Database stored in: ./instance/vulnerable_lab.db")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)