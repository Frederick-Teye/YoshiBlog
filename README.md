# YoshiBlog

A modern, scalable blog application built with Django, featuring user authentication, social logins, and serverless deployment on AWS Lambda.

## 🚀 Features

- **User Management**: Registration, login, and profile management with Django Allauth
- **Social Authentication**: Login with Google and GitHub
- **Blog CRUD**: Create, read, update, and delete blog posts with rich text support
- **Comments & Likes**: Interactive commenting system with like functionality
- **Tagging System**: Organize posts with tags for easy discovery
- **Responsive Design**: Mobile-first UI using Bootstrap 5
- **Security**: Input sanitization, CSRF protection, and secure password handling
- **Serverless Deployment**: AWS Lambda with API Gateway for scalable hosting

## 🌐 Live Demo

Check out the live version of YoshiBlog: [https://k5tb26hid6.execute-api.us-east-1.amazonaws.com/](https://k5tb26hid6.execute-api.us-east-1.amazonaws.com/)

## 🛠 Tech Stack

- **Backend**: Django 5.1, Python 3.11
- **Database**: PostgreSQL (hosted on Neon)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript (jQuery)
- **Authentication**: Django Allauth with social providers
- **Deployment**: AWS SAM, Lambda, API Gateway, S3
- **Containerization**: Docker
- **Other**: Redis (caching), boto3 (AWS SDK), nh3 (HTML sanitization)

## 🏗 Architecture

YoshiBlog follows a serverless architecture for high scalability and low maintenance:

- **Frontend**: Static files served from S3
- **Backend**: Django app running on AWS Lambda
- **Database**: Managed PostgreSQL instance
- **API**: RESTful endpoints via API Gateway
- **Security**: Secrets managed in AWS SSM Parameter Store

## 📦 Installation & Setup

### Prerequisites

- Python 3.11+
- Docker
- AWS CLI configured
- PostgreSQL database (e.g., Neon)

### Local Development

1. Clone the repository:

   ```bash
   git clone git@github.com:Frederick-Teye/YoshiBlog.git
   cd yoshiblog
   ```

2. Create virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables:

   ```bash
   export DJANGO_ENV=local
   export DATABASE_URL=your_postgres_url
   export SECRET_KEY=your_secret_key
   # Add other vars as needed
   ```

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Collect static files:

   ```bash
   python manage.py collectstatic
   ```

7. Start development server:
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` to view the application.

## 🚀 Deployment

### AWS Serverless Deployment

1. Install AWS SAM CLI
2. Configure AWS credentials
3. Build and deploy:
   ```bash
   sam build
   sam deploy --guided
   ```

The app will be deployed to AWS Lambda with API Gateway endpoints.

### Environment Variables for Production

Set the following in AWS SSM Parameter Store:

- `/yoshiblog/secret_key`
- `/yoshiblog/database_url`
- `/yoshiblog/admin_email`
- `/yoshiblog/admin_password`
- Social auth credentials

## 📖 Usage

- **Home**: Browse latest blog posts
- **Create Blog**: Authenticated users can write and publish posts
- **Tags**: Filter posts by tags
- **Comments**: Engage with posts through comments and likes
- **Admin Panel**: Manage users and content at `/admin/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request


## 👨‍💻 About the Author

I'm a Computer Science student with over 3 years of programming experience, specializing in web development and cloud technologies. I completed the AWS Cloud Practitioner (CCP) training through AmaliTech and hold the certification. Currently preparing for the AWS Developer Associate exam, I built YoshiBlog to demonstrate practical skills in full-stack development, serverless architecture, and DevOps practices.

Connect with me on [LinkedIn](https://www.linkedin.com/in/frederick-teye-61627b248/) or check out my other projects!
