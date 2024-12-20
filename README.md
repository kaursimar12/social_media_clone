# Social Media Clone

A social media clone inspired by Instagram, built using **Next.js** for the frontend, **Django** for the backend, and **PostgreSQL** as the database. The platform allows users to sign up, log in, post feeds, share posts, comment, like, follow/unfollow others, post threads, view and post stories, save posts, and more.

## Features

### 1. User Authentication
- **Signup**: Users can create a new account using their email and password.
- **Login**: Users can log into their existing account.

### 2. Feed and Post Interaction
- **Create Feed Posts**: Users can post feeds with multiple photos.
- **Like and Comment**: Users can like, comment, and reply to comments on posts.
- **Share Post**: Users can share a post by copying the post link.
  
### 3. User Interaction
- **Follow/Unfollow**: Users can follow and unfollow other users.
- **Visit Profiles**: Users can visit their own profile as well as other users’ profiles.
- **Tagging**: Users can tag others in posts. Tagged posts are viewable in the profile section.

### 4. Threads
- **Post Threads**: Users can post text-only threads (image support coming soon).
- **Like, Comment, and Reply**: Users can interact with threads through likes, comments, and replies.
- **Repost Threads**: Users can repost threads of others.
- **Share Thread**: Threads can be shared via a link.

### 5. Stories
- **Post Stories**: Users can post single or multiple stories.
- **View Stories**: Users can view their own stories and others’ stories.
- **Highlight Stories**: Users can highlight stories to keep them on their profile page.

### 6. Saved Posts
- **Save Posts**: Users can save posts.
- **View Saved Posts**: Saved posts can be viewed on the profile page.

### 7. Tagged Posts
- **Tagged Posts Section**: A section in the profile page where users can view all posts they've been tagged in, as well as posts they’ve tagged others in.

## Tech Stack

- **Frontend**: Next.js
- **Backend**: Django
- **Database**: PostgreSQL
- **Authentication**: Django REST Framework, JWT
- **Styling**: Tailwind CSS

## Setup

### Prerequisites
- Node.js
- Python 3.x
- PostgreSQL

### Frontend Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-folder>```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

   Your app should be running at http://localhost:3000.

### Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Setup the database:
   ```bash
   python manage.py migrate
   ```
5. Run the backend server:
   ```bash
   python manage.py runserver
   ```

This social media clone project provides a comprehensive set of features similar to popular platforms, allowing users to interact through feeds, threads, stories, and profiles. Built using Next.js, Django, and PostgreSQL, the application demonstrates a full-stack approach to creating an interactive social platform. While the project covers essential social media functionalities, there are still opportunities for further enhancements, such as supporting images in threads or improving the UI/UX.

