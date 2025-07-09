# Recipe_Generator
## 🧠🍽️ AI-Powered Recipe Generator (Django + OpenAI)

Generate personalized recipes along with image just by telling the app what ingredients you have!  
This AI-powered Django app uses the OpenAI API to craft complete recipes—optionally filtered by cuisine, cook time, difficulty, or other preferences.  
The app also allows user interactions like likes, comments, and notifications.

---
## Tech Stack

- Backend: Python, Django, PostgreSQL

- AI Integration: OpenAI API

- Frontend: HTML, CSS

- Auth: Django built-in authentication

- Image Generation: AI-generated image API 


## 🚀 Features

- 🤖 **AI Recipe Generation**
  - Input ingredients + preferences
  - Receive a complete recipe and image
- 👥 **User System**
  - Register, login, manage your recipes
  - Get notifications for comments and likes
- 💬 **Social Interactions**
  - Like and comment on others' recipes
- 📋 **Preferences**
  - Cuisine type, prep time, difficulty, dietary needs

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Vidya-GM/recipe-generator.git
cd Recipe_Generator
```

### 2. Create & Activate Virtual Environment 
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements/base.txt
```

### 4. Create .env File
OPENAI_API_KEY=your_openai_api_key  
DJANGO_SECRET_KEY=your_django_secret_key  
DEBUG=True  
DATABASE_NAME=your_db_name  
DATABASE_USER=your_db_user  
DATABASE_PASSWORD=your_db_password  
DATABASE_HOST=localhost  
DATABASE_PORT=5432   

⚠️ Make sure you have PostgreSQL installed and your database created.

### 5. Run Migrations
```bash
make dev-migrate
```

### 6. Create Superuser (optional)

### 7. Start the Project
```bash
make dev-start
```
🛡️ License
This project is licensed under the MIT License.

