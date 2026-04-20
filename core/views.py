from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from functools import wraps


def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='student_login')
        def wrapper(request, *args, **kwargs):
            user = request.user
            allowed = False

            if 'admin' in roles and user.is_admin:
                allowed = True
            elif 'teacher' in roles and user.is_teacher:
                allowed = True
            elif 'student' in roles and not user.is_teacher and not user.is_admin:
                allowed = True

            if not allowed:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('student_portal')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def can_edit_students(view_func):
    @wraps(view_func)
    @login_required(login_url='student_login')
    def wrapper(request, *args, **kwargs):
        if not request.user.can_edit_students():
            messages.error(request, 'You do not have permission to edit students.')
            return redirect('student_portal')
        return view_func(request, *args, **kwargs)
    return wrapper


def can_edit_teachers(view_func):
    @wraps(view_func)
    @login_required(login_url='student_login')
    def wrapper(request, *args, **kwargs):
        if not request.user.can_edit_teachers():
            messages.error(request, 'You do not have permission to manage teachers.')
            return redirect('student_portal')
        return view_func(request, *args, **kwargs)
    return wrapper


def landing(request):
    return render(request, 'landing.html')


def student_login(request):
    is_teacher_login = '/teacher/' in request.path

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('settings')
            elif user.is_teacher:
                return redirect('dashboard')
            return redirect('student_portal')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('student_login')

    template = 'portal/teacher_login.html' if is_teacher_login else 'portal/student_login.html'
    return render(request, template)


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_admin:
            login(request, user)
            return redirect('settings')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
            return redirect('admin_login')

    return render(request, 'portal/admin_login.html')


def student_logout(request):
    logout(request)
    return redirect('landing')


@login_required(login_url='student_login')
def student_portal(request):
    context = {
        'page_title': 'Student Portal',
        'student': request.user,
    }
    return render(request, 'portal/student_portal.html', context)


@role_required(['admin', 'teacher'])
def dashboard(request):
    context = {
        'page_title': 'Dashboard',
        'total_students': 624,
        'total_teachers': 86,
        'total_classes': 8,
        'fees_collected': 2450000,
        'pending_fees': 185000,
        'attendance_rate': 94.5,
        'male_students': 320,
        'female_students': 304,
        'recent_activities': [
            {'type': 'enrollment', 'message': 'New student enrolled: Sarah Johnson', 'time': '2 hours ago'},
            {'type': 'payment', 'message': 'Fee payment received: $2,500 from John Doe', 'time': '3 hours ago'},
            {'type': 'result', 'message': 'Exam results published: Mathematics Unit Test', 'time': '5 hours ago'},
            {'type': 'enrollment', 'message': 'New student enrolled: Michael Chen', 'time': '6 hours ago'},
            {'type': 'payment', 'message': 'Fee payment received: $3,000 from Jane Smith', 'time': '8 hours ago'},
        ],
        'students_by_form': {
            'labels': ['Form 1', 'Form 2', 'Form 3', 'Form 4'],
            'data': [155, 157, 159, 153]
        }
    }
    return render(request, 'dashboard/dashboard.html', context)


@can_edit_students
def students(request):
    context = {
        'page_title': 'Students Management',
    }
    return render(request, 'dashboard/students.html', context)


@can_edit_teachers
def teachers(request):
    context = {
        'page_title': 'Teachers Management',
    }
    return render(request, 'dashboard/teachers.html', context)


@role_required(['admin', 'teacher'])
def classes(request):
    context = {
        'page_title': 'Forms & Streams',
    }
    return render(request, 'dashboard/classes.html', context)


@role_required(['admin', 'teacher'])
def subjects(request):
    context = {
        'page_title': 'Subjects',
    }
    return render(request, 'dashboard/subjects.html', context)


@role_required(['admin', 'teacher'])
def attendance(request):
    context = {
        'page_title': 'Attendance Tracking',
    }
    return render(request, 'dashboard/attendance.html', context)


@role_required(['admin', 'teacher'])
def exams(request):
    context = {
        'page_title': 'Exams & Results',
    }
    return render(request, 'dashboard/exams.html', context)


@role_required(['admin', 'teacher'])
def fees(request):
    context = {
        'page_title': 'Fees Management',
    }
    return render(request, 'dashboard/fees.html', context)


@role_required(['admin', 'teacher'])
def reports(request):
    context = {
        'page_title': 'Reports & Analytics',
    }
    return render(request, 'dashboard/reports.html', context)


@role_required(['admin'])
def settings(request):
    context = {
        'page_title': 'Settings',
    }
    return render(request, 'dashboard/settings.html', context)


@role_required(['admin'])
def save_settings(request):
    if request.method == 'POST':
        import json
        from django.conf import settings as django_settings
        try:
            data = json.loads(request.body)
            settings_type = data.get('type')
            settings_data = data.get('data')

            if settings_type == 'general':
                return JsonResponse({'success': True, 'message': 'General settings saved successfully'})
            elif settings_type == 'appearance':
                return JsonResponse({'success': True, 'message': 'Appearance settings saved successfully'})
            elif settings_type == 'notifications':
                return JsonResponse({'success': True, 'message': 'Notification settings saved successfully'})
            elif settings_type == 'security':
                current_password = data.get('current_password')
                new_password = data.get('new_password')
                user = request.user
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    return JsonResponse({'success': True, 'message': 'Password changed successfully'})
                return JsonResponse({'success': False, 'message': 'Current password is incorrect'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid settings type'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required(login_url='student_login')
def create_user(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            from .models import Student

            user_type = data.get('user_type')
            username = data.get('username')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            student_id = data.get('student_id')
            form_level = data.get('form_level')
            stream = data.get('stream')

            if not request.user.is_admin:
                return JsonResponse({'success': False, 'message': 'Only admins can create users'})

            if Student.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'})

            if email and Student.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists'})

            if user_type == 'student':
                if not student_id:
                    last_student = Student.objects.filter(student_id__startswith='STU').order_by('-student_id').first()
                    if last_student:
                        num = int(last_student.student_id.replace('STU', '')) + 1
                        student_id = f'STU{num:04d}'
                    else:
                        student_id = 'STU0001'
            else:
                if not student_id:
                    if user_type == 'admin':
                        prefix = 'ADM'
                    else:
                        prefix = 'EMP'
                    last_user = Student.objects.filter(student_id__startswith=prefix).order_by('-student_id').first()
                    if last_user:
                        num = int(last_user.student_id.replace(prefix, '')) + 1
                        student_id = f'{prefix}{num:04d}'
                    else:
                        student_id = f'{prefix}0001'

            user = Student.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                form_level=form_level or '',
                stream=stream or '',
                phone=phone or '',
                is_teacher=True if user_type == 'teacher' else False,
                is_admin=True if user_type == 'admin' else False
            )

            return JsonResponse({'success': True, 'message': 'User created successfully', 'user_id': student_id})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
