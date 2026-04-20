# School Management System Dashboard

A modern, professional, and fully responsive School Management System Dashboard built with Django and Bootstrap 5.

## Features

### Modules
- **Dashboard** - Overview with statistics, charts, and recent activities
- **Students Management** - Complete student record management
- **Teachers Management** - Teacher profiles and assignments
- **Classes & Streams** - Class organization and management
- **Subjects** - Subject management and teacher assignments
- **Attendance Tracking** - Daily attendance monitoring
- **Exams & Results** - Examination management and grading
- **Fees Management** - Fee collection and tracking
- **Reports & Analytics** - Comprehensive reporting system
- **Settings** - System configuration and preferences

### UI Features
- Modern, clean admin panel design
- Responsive layout (mobile, tablet, desktop)
- Collapsible sidebar navigation
- Interactive charts (Chart.js)
- Data tables with pagination
- Modal forms for adding/editing records
- Toast notifications
- Search functionality
- Export capabilities (PDF/Excel ready)

## Tech Stack

- **Backend**: Django 4.0+
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **JavaScript**: Vanilla JS + Chart.js
- **Icons**: Font Awesome 6.4
- **Charts**: Chart.js

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd High_Profile
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Open your browser and navigate to:
   - Dashboard: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## Project Structure

```
High_Profile/
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── High_Profile/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   └── dashboard/
│       ├── base.html
│       ├── dashboard.html
│       ├── students.html
│       ├── teachers.html
│       ├── classes.html
│       ├── subjects.html
│       ├── attendance.html
│       ├── exams.html
│       ├── fees.html
│       ├── reports.html
│       └── settings.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── dashboard.js
│   └── img/
├── manage.py
└── README.md
```

## Customization

### Adding Django Models

Create models in `core/models.py`:

```python
from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

### Extending Views

Update views in `core/views.py`:

```python
from django.shortcuts import render
from .models import Student

def students(request):
    students = Student.objects.all()
    return render(request, 'dashboard/students.html', {'students': students})
```

### Adding Forms

Create forms in `core/forms.py`:

```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
```

## Placeholder Variables

The templates use Django template tags for backend integration:

- `{{ total_students }}` - Total number of students
- `{{ total_teachers }}` - Total number of teachers
- `{{ total_classes }}` - Total number of classes
- `{{ fees_collected }}` - Total fees collected
- `{{ pending_fees }}` - Pending fees amount
- `{{ attendance_rate }}` - Current attendance percentage
- `{{ male_students }}` - Number of male students
- `{{ female_students }}` - Number of female students
- `{{ recent_activities }}` - List of recent activities
- `{{ students_by_class }}` - Student distribution by class

## Screenshots

The dashboard includes:
- Statistic cards with visual indicators
- Bar charts for student distribution
- Pie/doughnut charts for demographics
- Interactive data tables
- Quick action buttons
- Activity feeds
- Progress indicators

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is open-source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Support

For support, email support@school.edu or create an issue in the repository.

# High_Profile