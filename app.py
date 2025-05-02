from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pdfkit  # Install using `pip install pdfkit`
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Required for session management
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Download NLTK dependencies
nltk.download('punkt')
nltk.download('stopwords')

# MySQL Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chaitu895@",  # Change to your actual MySQL password
        database="resume_internship_matching"
    )

# Function to convert skills to numerical vectors
def skills_to_vector(skills):
    vector = [0] * len(skill_to_index)  # Initialize a vector of zeros
    for skill in skills.split():  # Split the string into individual skills
        if skill in skill_to_index:
            vector[skill_to_index[skill]] += 1  # Increment the count for the skill
    return vector

# Fetch data from MySQL
def fetch_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch resumes from resume_info table
    cursor.execute("SELECT * FROM resume_info")
    resumes = cursor.fetchall()
    
    # Get column names from MySQL tables
    cursor.execute("SHOW COLUMNS FROM resume_info")
    resume_columns = [column[0] for column in cursor.fetchall()]
    
    # Fetch internships
    cursor.execute("SELECT * FROM internship_info")
    internships = cursor.fetchall()
    cursor.execute("SHOW COLUMNS FROM internship_info")
    internship_columns = [column[0] for column in cursor.fetchall()]
    
    resume_info_df = pd.DataFrame(resumes, columns=resume_columns)
    internship_df = pd.DataFrame(internships, columns=internship_columns)
    
    cursor.close()
    conn.close()

    # Preprocessing
    resume_info_df.fillna('', inplace=True)
    internship_df.fillna('', inplace=True)

    resume_info_df['processed_Skills'] = resume_info_df['skills'].apply(preprocess_skills)
    internship_df['processed_Required_Skills'] = internship_df['skills_required'].apply(preprocess_skills)

    # Create a set of unique skills
    all_skills = ' '.join(resume_info_df['processed_Skills']) + ' ' + ' '.join(internship_df['processed_Required_Skills'])
    unique_skills = set(all_skills.split())  # Split the string into individual skills
    global skill_to_index  # Declare as global so it can be used in other functions
    skill_to_index = {skill: idx for idx, skill in enumerate(unique_skills)}  # Map each skill to an index

    # Vectorization
    resume_info_df['Skill_vector'] = resume_info_df['processed_Skills'].apply(skills_to_vector)
    internship_df['Required_Skill_vector'] = internship_df['processed_Required_Skills'].apply(skills_to_vector)

    return resume_info_df, internship_df

# Preprocessing function for skills
def preprocess_skills(skills):
    if not isinstance(skills, str) or skills.strip() == '':
        return ''
    tokens = word_tokenize(skills.lower())
    tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
    print(f"Original Skills: {skills} -> Processed Skills: {tokens}")  # Debugging
    return ' '.join(tokens)  # Return a single string

# Load data from database
resume_info_df, internship_df = fetch_data()

# Function to calculate similarity
def calculate_similarity(required_skills, applicant_skills):
    if isinstance(required_skills, list):
        required_skills = ' '.join(required_skills)
    if isinstance(applicant_skills, list):
        applicant_skills = ' '.join(applicant_skills)
    print(f"Required Skills: {required_skills}, Applicant Skills: {applicant_skills}")  # Debugging
    vectorizer = CountVectorizer().fit_transform([required_skills, applicant_skills])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity(vectors)[0][1]
    print(f"Similarity Score: {similarity}")  # Debugging
    return similarity

# Function to match internships
def match_internships(resume):
    results = []
    for index, internship in internship_df.iterrows():
        print(f"Internship: {internship}")  # Debugging
        print(f"Resume: {resume}")  # Debugging
        similarity_score = calculate_similarity(resume['processed_Skills'], internship['processed_Required_Skills'])
        if similarity_score > 0:  # Include all matches with a similarity score greater than 0
            results.append({
                'internship_title': internship['role'],
                'company': internship['company_name'],
                'type_of_internship': internship['type_of_internship'],
                'duration': internship['duration'],
                'location': internship['location'],
                'description': internship['description_of_internship'],
                'skills_required': internship['skills_required'],
                'salary': internship['expected_salary'],
                'start_date': internship['start_date'],
                'end_date': internship['end_date'],
                'posted_date': internship['posted_date'],
                'similarity_score': similarity_score * 100  # Convert to percentage
            })
    
    # Sort by highest similarity score and return the top 5 results
    results = sorted(results, key=lambda x: x['similarity_score'], reverse=True)[:5]
    return results

# Function to match resumes with internships
def match_resumes_with_internships():
    results = []

    # Iterate through each internship
    for _, internship in internship_df.iterrows():
        internship_skills = internship['skills_required']

        # Iterate through each resume
        for _, resume in resume_info_df.iterrows():  # Use resume_info_df instead of resume_df
            resume_skills = resume['skills']

            # Calculate similarity
            similarity_score = calculate_similarity(internship_skills, resume_skills)

            # If similarity score is greater than 0, add to results
            if similarity_score > 0:
                results.append({
                    'internship_id': internship['id'],
                    'internship_title': internship['role'],
                    'company': internship['company_name'],
                    'applicant_name': resume['name_of_applicant'],  # Updated column name
                    'applicant_email': resume['email'],
                    'similarity_score': round(similarity_score * 100, 2)  # Convert to percentage
                })

    # Sort results by similarity score in descending order
    results = sorted(results, key=lambda x: x['similarity_score'], reverse=True)

    return results

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['GET', 'POST'])
def match():
    if 'user_role' in session and session['user_role'] == 'intern':
        applicant_name = session['user_name']
        matching_resume = resume_info_df[resume_info_df['name_of_applicant'].str.contains(applicant_name, case=False)]
        if matching_resume.empty:
            flash("No resume found for the applicant.", "error")
            return redirect(url_for('intern_dashboard'))
        
        resume = matching_resume.iloc[0]
        results = match_internships(resume)  # Call the updated matching algorithm
        return render_template('results.html', results=results, applicant_name=applicant_name)
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']  # Get the role from the form

        # Recruiter-specific fields
        organization_name = request.form.get('organization_name', None)
        contact_details = request.form.get('contact_details', None)
        location = request.form.get('location', None)
        website_link = request.form.get('website_link', None)

        # Validate passwords
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('signup'))

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Store user details in the database
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, password, role, organization_name, contact_details, location, website_link)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, hashed_password, role, organization_name, contact_details, location, website_link))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Sign-up successful! Please log in.", "success")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate entry error
                flash("This email is already registered with us. Please use another email.", "error")
            else:
                flash("An error occurred while processing your request. Please try again.", "error")
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_role'] = user['role']  # Store the user's role in the session
                session['organization_name'] = user.get('organization_name', None)
                session['email'] = user.get('email', None)
                flash("Login successful!", "success")

                # Redirect to the appropriate dashboard
                if user['role'] == 'intern':
                    return redirect(url_for('intern_dashboard'))
                elif user['role'] == 'recruiter':
                    return redirect(url_for('recruiter_dashboard'))
            else:
                flash("Invalid email or password!", "error")
                return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

@app.route('/intern_dashboard')
def intern_dashboard():
    if 'user_role' in session and session['user_role'] == 'intern':
        applicant_name = session.get('user_name', '')
        print(f"Logged-in Intern: {applicant_name}")  # Debugging

        # Fetch the resume for the logged-in user
        matching_resume = resume_info_df[resume_info_df['name_of_applicant'].str.contains(applicant_name, case=False)]
        print(f"Matching Resume: {matching_resume}")  # Debugging

        if matching_resume.empty:
            flash("No resume found for the applicant. Please create one.", "error")
            return redirect(url_for('create_resume'))
        
        resume = matching_resume.iloc[0]  # Get the first matching resume row
        matched_internships = match_internships(resume)  # Pass the resume row to the function
        return render_template('intern_dashboard.html', user_name=applicant_name, matched_internships=matched_internships)
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

@app.route('/recruiter_dashboard')
def recruiter_dashboard():
    if 'user_role' in session and session['user_role'] == 'recruiter':
        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)

            # Fetch recruiter details
            cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
            recruiter = cursor.fetchone()

            # Fetch internships posted by the recruiter
            cursor.execute("""
                SELECT id, role, description_of_internship
                FROM internship_info
                WHERE company_name = %s
            """, (recruiter['organization_name'],))
            internships = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('recruiter_dashboard.html', recruiter=recruiter, internships=internships)
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "error")
            return redirect(url_for('login'))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

@app.route('/create_resume', methods=['GET', 'POST'])
def create_resume():
    if 'user_role' in session and session['user_role'] == 'intern':
        if request.method == 'POST':
            # Get resume details from the form
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            skills = request.form['skills']
            experience = request.form['experience']
            education = request.form['education']
            certifications = request.form.get('certifications', '')
            achievements = request.form.get('achievements', '')
            downloaded = False  # Initially, the resume is not downloaded

            # Save resume details to the database
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO resume_info (user_id, name_of_applicant, email, phone_number, skills, experience, education, certifications, achievements, downloaded)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (session['user_id'], name, email, phone, skills, experience, education, certifications, achievements, downloaded)
                )
                conn.commit()
                cursor.close()
                conn.close()
                flash("Resume created successfully!", "success")
                return redirect(url_for('intern_dashboard'))
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "error")
                return redirect(url_for('create_resume'))

        return render_template('create_resume.html')
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

@app.route('/edit_resume', methods=['GET', 'POST'])
def edit_resume():
    if 'user_role' in session and session['user_role'] == 'intern':
        if request.method == 'POST':
            # Update resume details in the database
            resume_id = request.form['resume_id']
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            skills = request.form['skills']
            experience = request.form['experience']
            education = request.form['education']
            certifications = request.form.get('certifications', '')
            achievements = request.form.get('achievements', '')

            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE resumes
                    SET name=%s, email=%s, phone=%s, skills=%s, experience=%s, education=%s, certifications=%s, achievements=%s
                    WHERE id=%s AND user_id=%s
                    """,
                    (name, email, phone, skills, experience, education, certifications, achievements, resume_id, session['user_id'])
                )
                conn.commit()
                cursor.close()
                conn.close()
                flash("Resume updated successfully!", "success")
                return redirect(url_for('intern_dashboard'))
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "error")
                return redirect(url_for('edit_resume'))

        # Fetch the user's resume details to pre-fill the form
        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM resumes WHERE user_id = %s", (session['user_id'],))
            resume = cursor.fetchone()
            cursor.close()
            conn.close()
            return render_template('edit_resume.html', resume=resume)
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "error")
            return redirect(url_for('intern_dashboard'))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

@app.route('/download_resume')
def download_resume():
    if 'user_id' not in session:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

    try:
        # Fetch the user's resume details from the database
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resumes WHERE user_id = %s", (session['user_id'],))
        resume = cursor.fetchone()
        cursor.close()
        conn.close()

        if not resume:
            flash("No resume found for the user.", "error")
            return redirect(url_for('intern_dashboard'))

        # Generate the HTML content for the PDF
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                }}
                h1 {{
                    color: #00796b;
                }}
                .section {{
                    margin-bottom: 20px;
                }}
                .section h2 {{
                    color: #005a4f;
                    border-bottom: 2px solid #00796b;
                    padding-bottom: 5px;
                }}
                .section p {{
                    margin: 5px 0;
                }}
            </style>
        </head>
        <body>
            <h1>{resume['name']}'s Resume</h1>
            <div class="section">
                <h2>Contact Information</h2>
                <p><strong>Email:</strong> {resume['email']}</p>
                <p><strong>Phone:</strong> {resume.get('phone', 'N/A')}</p>
            </div>
            <div class="section">
                <h2>Skills</h2>
                <p>{resume['skills']}</p>
            </div>
            <div class="section">
                <h2>Work Experience</h2>
                <p>{resume['experience']}</p>
            </div>
            <div class="section">
                <h2>Education</h2>
                <p>{resume['education']}</p>
            </div>
            <div class="section">
                <h2>Certifications</h2>
                <p>{resume.get('certifications', 'N/A')}</p>
            </div>
            <div class="section">
                <h2>Achievements</h2>
                <p>{resume.get('achievements', 'N/A')}</p>
            </div>
        </body>
        </html>
        """

        # Generate the PDF
        pdf_path = 'resume.pdf'
        pdfkit.from_string(html, pdf_path)

        # Update the downloaded status in the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE resumes SET downloaded = TRUE WHERE user_id = %s", (session['user_id'],))
        conn.commit()
        cursor.close()
        conn.close()

        # Serve the PDF file
        return send_file(pdf_path, as_attachment=True)

    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
        return redirect(url_for('intern_dashboard'))

@app.route('/apply_internship', methods=['POST'])
def apply_internship():
    if 'user_id' not in session:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

    internship_id = request.form.get('internship_id')
    print(f"Received internship_id: {internship_id}")  # Debugging statement

    if not internship_id:
        flash("Invalid internship ID.", "error")
        return redirect(url_for('match'))

    try:
        # Save the application to the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO applications (user_id, internship_id) VALUES (%s, %s)",
            (session['user_id'], internship_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("You have successfully applied for the internship!", "success")
        return redirect(url_for('match'))
    except mysql.connector.IntegrityError:
        flash("You have already applied for this internship.", "error")
        return redirect(url_for('match'))
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
        return redirect(url_for('match'))

@app.route('/applied_internships')
def applied_internships():
    if 'user_id' not in session:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

    try:
        # Fetch the list of applied internships for the logged-in user
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT internship_info.role AS internship_title,
                   internship_info.company_name AS company,
                   internship_info.type_of_internship,
                   internship_info.location,
                   internship_info.description_of_internship,
                   applications.applied_at
            FROM applications
            JOIN internship_info ON applications.internship_id = internship_info.id
            WHERE applications.user_id = %s
            ORDER BY applications.applied_at DESC
        """, (session['user_id'],))
        applied_internships = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('applied_internships.html', applied_internships=applied_internships)
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
        return redirect(url_for('intern_dashboard'))

@app.route('/register_internship', methods=['GET', 'POST'])
def register_internship():
    if 'user_role' in session and session['user_role'] == 'recruiter':
        if request.method == 'POST':
            # Get internship details from the form
            role = request.form['role']
            description_of_internship = request.form['description_of_internship']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            duration = request.form['duration']
            type_of_internship = request.form['type_of_internship']
            skills_required = request.form['skills_required']
            location = request.form['location']
            years_of_experience = request.form['years_of_experience']
            phone_number = request.form['phone_number']

            # Validate phone number length
            if len(phone_number) > 20:
                flash("Phone number is too long. Please enter a valid phone number.", "error")
                return redirect(url_for('register_internship'))

            try:
                # Save internship details to the database
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO internship_info (role, description_of_internship, start_date, end_date, duration, type_of_internship, skills_required, location, years_of_experience, phone_number, company_name, company_mail)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (role, description_of_internship, start_date, end_date, duration, type_of_internship, skills_required, location, years_of_experience, phone_number, session['organization_name'], session['email']))
                conn.commit()
                cursor.close()
                conn.close()

                flash("Internship registered successfully!", "success")
                return redirect(url_for('recruiter_dashboard'))
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "error")
                return redirect(url_for('register_internship'))

        # Fetch recruiter details to pre-fill the form
        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
            recruiter = cursor.fetchone()
            cursor.close()
            conn.close()
            return render_template('register_internship.html', recruiter=recruiter)
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "error")
            return redirect(url_for('recruiter_dashboard'))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

@app.route('/applied_applicants')
def applied_applicants():
    if 'user_role' in session and session['user_role'] == 'recruiter':
        try:
            # Fetch applicants for internships posted by the recruiter
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT users.name AS applicant_name,
                       users.email AS applicant_email,
                       internship_info.role AS internship_title,
                       applications.applied_at
                FROM applications
                JOIN internship_info ON applications.internship_id = internship_info.id
                JOIN users ON applications.user_id = users.id
                WHERE internship_info.company_name = %s
                ORDER BY applications.applied_at DESC
            """, (session['user_name'],))
            applicants = cursor.fetchall()
            cursor.close()
            conn.close()

            return render_template('applied_applicants.html', applicants=applicants)
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "error")
            return redirect(url_for('recruiter_dashboard'))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

@app.route('/top_matched_applicants/<int:internship_id>')
def top_matched_applicants(internship_id):
    if 'user_role' in session and session['user_role'] == 'recruiter':
        try:
            # Fetch the internship details
            internship = internship_df[internship_df['id'] == internship_id].iloc[0]
            required_skills = internship['processed_Required_Skills']

            # Fetch all applicants and calculate similarity scores
            matched_applicants = []
            for _, resume in resume_info_df.iterrows():
                similarity_score = calculate_similarity(required_skills, resume['processed_Skills'])
                if similarity_score > 0:
                    matched_applicants.append({
                        'name': resume['name_of_applicant'],
                        'email': resume['email'],
                        'skills': resume['skills'],
                        'similarity_score': round(similarity_score * 100, 2)  # Convert to percentage
                    })

            # Sort applicants by similarity score in descending order
            matched_applicants = sorted(matched_applicants, key=lambda x: x['similarity_score'], reverse=True)[:5]

            return render_template('top_matched_applicants.html', internship_title=internship['role'], matched_applicants=matched_applicants)

        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('recruiter_dashboard'))
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

@app.route('/edit_organization_profile', methods=['GET', 'POST'])
def edit_organization_profile():
    if 'user_role' in session and session['user_role'] == 'recruiter':
        if request.method == 'POST':
            # Update organization profile details
            organization_name = request.form['organization_name']
            email = request.form['email']
            phone_number = request.form['phone_number']

            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users
                    SET name = %s, email = %s, phone_number = %s
                    WHERE id = %s
                """, (organization_name, email, phone_number, session['user_id']))
                conn.commit()
                cursor.close()
                conn.close()

                flash("Organization profile updated successfully!", "success")
                return redirect(url_for('recruiter_dashboard'))
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "error")
                return redirect(url_for('edit_organization_profile'))

        return render_template('edit_organization_profile.html')
    else:
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)