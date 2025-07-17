"""
Enhanced script to create comprehensive student data for MediScope Django application
Run this script to populate the database with realistic student profiles and data

Usage:
1. Navigate to your Django project directory
2. Run: python manage.py shell
3. Then: exec(open('scripts/create_student_data.py').read())

Or run directly:
python scripts/create_student_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random
from django.db import models
from django.utils import timezone

# Setup Django environment
# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediscope.settings')

# Setup Django
django.setup()

# Now import Django models
from django.contrib.auth.models import User
from core.models import StudentProfile, Achievement, Activity, StudySession
from cases.models import Case, CaseStep, Choice

def create_admin_user():
    """Create admin superuser"""
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@mediscope.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        
        # Update admin profile
        profile = admin_user.studentprofile
        profile.student_id = 'ADMIN001'
        profile.university = 'MediScope Administration'
        profile.year_of_study = 'other'
        profile.specialization = 'general'
        profile.total_xp = 10000
        profile.level = 10
        profile.current_streak = 100
        profile.longest_streak = 100
        profile.cases_completed = 50
        profile.quiz_accuracy = 100.0
        profile.total_study_time = 5000
        profile.is_profile_complete = True
        profile.save()
        
        print(f"✅ Created admin user: {admin_user.username}")
    else:
        print(f"ℹ️  Admin user already exists: {admin_user.username}")

def create_demo_users():
    """Create demo users with complete profiles"""
    
    # Create demo student user
    demo_user, created = User.objects.get_or_create(
        username='demo_student',
        defaults={
            'email': 'demo@mediscope.com',
            'first_name': 'Demo',
            'last_name': 'Student',
        }
    )
    if created:
        demo_user.set_password('mediscope123')
        demo_user.save()
        
        # Update profile
        profile = demo_user.studentprofile
        profile.student_id = 'MS2024001'
        profile.university = 'MediScope University'
        profile.year_of_study = '3'
        profile.specialization = 'cardiology'
        profile.total_xp = 2847
        profile.level = 3
        profile.current_streak = 12
        profile.longest_streak = 25
        profile.cases_completed = 23
        profile.quiz_accuracy = 87.5
        profile.total_study_time = 1250
        profile.is_profile_complete = True
        profile.save()
        
        print(f"✅ Created demo user: {demo_user.username}")
    else:
        print(f"ℹ️  Demo user already exists: {demo_user.username}")

def create_sample_students():
    """Create a variety of sample students"""
    
    students_data = [
        {
            'username': 'sarah_miller',
            'first_name': 'Sarah',
            'last_name': 'Miller',
            'email': 'sarah.miller@university.edu',
            'student_id': 'SM2023045',
            'university': 'Harvard Medical School',
            'year_of_study': '4',
            'specialization': 'neurology',
            'total_xp': 4250,
            'level': 4,
            'current_streak': 18,
            'cases_completed': 35,
            'quiz_accuracy': 92.3
        },
        {
            'username': 'alex_kim',
            'first_name': 'Alex',
            'last_name': 'Kim',
            'email': 'alex.kim@medschool.edu',
            'student_id': 'AK2024012',
            'university': 'Johns Hopkins University',
            'year_of_study': '2',
            'specialization': 'surgery',
            'total_xp': 3120,
            'level': 3,
            'current_streak': 7,
            'cases_completed': 28,
            'quiz_accuracy': 88.7
        },
        {
            'username': 'mike_rodriguez',
            'first_name': 'Mike',
            'last_name': 'Rodriguez',
            'email': 'mike.r@stanford.edu',
            'student_id': 'MR2023089',
            'university': 'Stanford School of Medicine',
            'year_of_study': '3',
            'specialization': 'emergency',
            'total_xp': 2756,
            'level': 2,
            'current_streak': 5,
            'cases_completed': 22,
            'quiz_accuracy': 85.1
        },
        {
            'username': 'emma_johnson',
            'first_name': 'Emma',
            'last_name': 'Johnson',
            'email': 'emma.j@mayo.edu',
            'student_id': 'EJ2024067',
            'university': 'Mayo Clinic Alix School',
            'year_of_study': '1',
            'specialization': 'pediatrics',
            'total_xp': 1890,
            'level': 1,
            'current_streak': 14,
            'cases_completed': 15,
            'quiz_accuracy': 91.2
        },
        {
            'username': 'david_chen',
            'first_name': 'David',
            'last_name': 'Chen',
            'email': 'david.chen@ucsf.edu',
            'student_id': 'DC2023156',
            'university': 'UCSF School of Medicine',
            'year_of_study': '4',
            'specialization': 'radiology',
            'total_xp': 3890,
            'level': 3,
            'current_streak': 22,
            'cases_completed': 31,
            'quiz_accuracy': 89.8
        },
        {
            'username': 'lisa_wang',
            'first_name': 'Lisa',
            'last_name': 'Wang',
            'email': 'lisa.wang@yale.edu',
            'student_id': 'LW2024089',
            'university': 'Yale School of Medicine',
            'year_of_study': '2',
            'specialization': 'psychiatry',
            'total_xp': 2340,
            'level': 2,
            'current_streak': 9,
            'cases_completed': 19,
            'quiz_accuracy': 86.4
        },
        {
            'username': 'james_brown',
            'first_name': 'James',
            'last_name': 'Brown',
            'email': 'james.brown@duke.edu',
            'student_id': 'JB2023178',
            'university': 'Duke University School of Medicine',
            'year_of_study': '3',
            'specialization': 'pathology',
            'total_xp': 3456,
            'level': 3,
            'current_streak': 15,
            'cases_completed': 27,
            'quiz_accuracy': 90.1
        },
        {
            'username': 'maria_garcia',
            'first_name': 'Maria',
            'last_name': 'Garcia',
            'email': 'maria.garcia@northwestern.edu',
            'student_id': 'MG2024034',
            'university': 'Northwestern University',
            'year_of_study': '1',
            'specialization': 'general',
            'total_xp': 1567,
            'level': 1,
            'current_streak': 6,
            'cases_completed': 12,
            'quiz_accuracy': 83.7
        },
        {
            'username': 'robert_taylor',
            'first_name': 'Robert',
            'last_name': 'Taylor',
            'email': 'robert.taylor@upenn.edu',
            'student_id': 'RT2023067',
            'university': 'University of Pennsylvania',
            'year_of_study': '4',
            'specialization': 'surgery',
            'total_xp': 4567,
            'level': 4,
            'current_streak': 21,
            'cases_completed': 38,
            'quiz_accuracy': 94.2
        },
        {
            'username': 'jennifer_lee',
            'first_name': 'Jennifer',
            'last_name': 'Lee',
            'email': 'jennifer.lee@columbia.edu',
            'student_id': 'JL2024123',
            'university': 'Columbia University',
            'year_of_study': '2',
            'specialization': 'pediatrics',
            'total_xp': 2789,
            'level': 2,
            'current_streak': 11,
            'cases_completed': 21,
            'quiz_accuracy': 88.9
        }
    ]
    
    created_count = 0
    for student_data in students_data:
        user, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults={
                'email': student_data['email'],
                'first_name': student_data['first_name'],
                'last_name': student_data['last_name']
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            
            # Update student profile
            profile = user.studentprofile
            profile.student_id = student_data['student_id']
            profile.university = student_data['university']
            profile.year_of_study = student_data['year_of_study']
            profile.specialization = student_data['specialization']
            profile.total_xp = student_data['total_xp']
            profile.level = student_data['level']
            profile.current_streak = student_data['current_streak']
            profile.longest_streak = student_data['current_streak'] + random.randint(5, 15)
            profile.cases_completed = student_data['cases_completed']
            profile.quiz_accuracy = student_data['quiz_accuracy']
            profile.total_study_time = random.randint(800, 2000)
            profile.is_profile_complete = True
            profile.save()
            
            created_count += 1
            print(f"✅ Created student: {user.username}")
        else:
            print(f"ℹ️  Student already exists: {user.username}")
    
    print(f"📊 Created {created_count} new students")

def create_sample_achievements():
    """Create sample achievements for users"""
    
    achievement_types = [
        ('first_case', 'First Case Complete', 'Completed your first medical case', 50),
        ('case_master', 'Case Master', 'Completed 20 medical cases', 200),
        ('streak_7', 'Week Warrior', '7-day learning streak', 100),
        ('streak_30', 'Month Master', '30-day learning streak', 500),
        ('quiz_expert', 'Quiz Expert', 'Achieved 90%+ quiz accuracy', 150),
        ('early_bird', 'Early Bird', 'Studied before 8 AM', 25),
        ('night_owl', 'Night Owl', 'Studied after 10 PM', 25),
        ('anatomy_explorer', 'Anatomy Explorer', 'Explored 3D anatomy models', 75),
        ('ai_user', 'AI User', 'Used AI symptom checker', 50),
        ('perfect_quiz', 'Perfect Score', 'Achieved 100% on a quiz', 100),
        ('level_up', 'Level Up', 'Reached a new level', 50),
    ]
    
    users = User.objects.all()
    created_count = 0
    
    for user in users:
        # Give each user 2-5 random achievements based on their progress
        profile = user.studentprofile
        num_achievements = min(random.randint(2, 5), len(achievement_types))
        
        # Ensure achievements match user's progress
        eligible_achievements = []
        
        # Basic achievements for all users
        eligible_achievements.append(('first_case', 'First Case Complete', 'Completed your first medical case', 50))
        
        # Progress-based achievements
        if profile.cases_completed >= 20:
            eligible_achievements.append(('case_master', 'Case Master', 'Completed 20 medical cases', 200))
        
        if profile.current_streak >= 7:
            eligible_achievements.append(('streak_7', 'Week Warrior', '7-day learning streak', 100))
        
        if profile.current_streak >= 30:
            eligible_achievements.append(('streak_30', 'Month Master', '30-day learning streak', 500))
        
        if profile.quiz_accuracy >= 90:
            eligible_achievements.append(('quiz_expert', 'Quiz Expert', 'Achieved 90%+ quiz accuracy', 150))
        
        # Random achievements
        eligible_achievements.extend([
            ('early_bird', 'Early Bird', 'Studied before 8 AM', 25),
            ('night_owl', 'Night Owl', 'Studied after 10 PM', 25),
            ('anatomy_explorer', 'Anatomy Explorer', 'Explored 3D anatomy models', 75),
            ('ai_user', 'AI User', 'Used AI symptom checker', 50),
        ])
        
        # Level up achievements
        for level in range(2, profile.level + 1):
            eligible_achievements.append(('level_up', f'Level {level} Reached!', f'Congratulations on reaching level {level}!', 50))
        
        # Select random achievements
        selected_achievements = random.sample(
            eligible_achievements, 
            min(num_achievements, len(eligible_achievements))
        )
        
        for achievement_type, title, description, xp_reward in selected_achievements:
            achievement, created = Achievement.objects.get_or_create(
                user=user,
                achievement_type=achievement_type,
                defaults={
                    'title': title,
                    'description': description,
                    'xp_reward': xp_reward,
                    'earned_at': timezone.now() - timedelta(days=random.randint(1, 30))
                }
            )
            if created:
                created_count += 1
    
    print(f"🏆 Created {created_count} achievements")

def create_sample_activities():
    """Create sample activities for users"""
    
    activity_templates = [
        ('case_completed', [
            ('Completed Emergency Room Crisis', 'Successfully diagnosed hypoglycemia case', 150),
            ('Completed Cardiology Case', 'Diagnosed myocardial infarction', 180),
            ('Completed Neurology Case', 'Identified stroke symptoms', 160),
            ('Completed Pediatric Case', 'Diagnosed childhood asthma', 140),
            ('Completed Surgery Case', 'Planned appendectomy procedure', 170),
        ]),
        ('quiz_taken', [
            ('Cardiology Quiz Mastery', 'Scored 95% on cardiology fundamentals', 120),
            ('Anatomy Quiz Champion', 'Perfect score on heart anatomy', 100),
            ('Pharmacology Quiz', 'Scored 88% on drug interactions', 90),
            ('Pathology Quiz Success', 'Scored 92% on disease mechanisms', 110),
            ('Emergency Medicine Quiz', 'Scored 85% on trauma protocols', 95),
        ]),
        ('anatomy_explored', [
            ('Heart Anatomy Study', 'Explored 3D heart model for 15 minutes', 75),
            ('Brain Structure Analysis', 'Studied cerebral cortex anatomy', 80),
            ('Lung Function Exploration', 'Analyzed respiratory system', 70),
            ('Skeletal System Study', 'Explored bone structure', 65),
            ('Nervous System Deep Dive', 'Studied neural pathways', 85),
        ]),
        ('ai_checker_used', [
            ('AI Symptom Analysis', 'Used AI checker for chest pain symptoms', 50),
            ('Diagnostic AI Practice', 'Analyzed headache symptoms with AI', 45),
            ('AI-Assisted Diagnosis', 'Used AI for abdominal pain case', 55),
            ('Symptom Checker Training', 'Practiced with AI diagnostic tool', 40),
            ('AI Medical Consultation', 'Used AI for complex symptom analysis', 60),
        ]),
        ('achievement_earned', [
            ('New Achievement Unlocked!', 'Earned "Week Warrior" achievement', 100),
            ('Achievement Milestone!', 'Earned "Case Master" achievement', 200),
            ('Level Up Achievement!', 'Reached new level milestone', 50),
            ('Streak Achievement!', 'Earned streak-based achievement', 75),
            ('Quiz Achievement!', 'Earned quiz mastery achievement', 125),
        ]),
        ('login', [
            ('Daily Login Bonus', 'Logged in and ready to learn', 5),
            ('Morning Study Session', 'Started early morning learning', 10),
            ('Evening Study Time', 'Continued learning in the evening', 8),
            ('Weekend Learning', 'Dedicated weekend study time', 12),
            ('Consistent Learning', 'Maintained daily learning habit', 7),
        ]),
    ]
    
    users = User.objects.all()
    created_count = 0
    
    for user in users:
        # Create 5-12 activities per user over the last 14 days
        num_activities = random.randint(5, 12)
        
        for i in range(num_activities):
            # Select random activity type and template
            activity_type, templates = random.choice(activity_templates)
            title, description, xp_earned = random.choice(templates)
            
            # Random date within last 14 days
            days_ago = random.randint(0, 14)
            hours_ago = random.randint(0, 23)
            created_at = timezone.now() - timedelta(days=days_ago, hours=hours_ago)
            
            Activity.objects.create(
                user=user,
                activity_type=activity_type,
                title=title,
                description=description,
                xp_earned=xp_earned,
                created_at=created_at
            )
            created_count += 1
    
    print(f"📝 Created {created_count} activities")

def create_sample_study_sessions():
    """Create sample study sessions"""
    
    users = User.objects.all()
    created_count = 0
    
    for user in users:
        # Create 3-8 study sessions over the last 21 days
        num_sessions = random.randint(3, 8)
        
        for i in range(num_sessions):
            days_ago = random.randint(0, 21)
            hour = random.randint(6, 23)  # Study sessions between 6 AM and 11 PM
            start_time = timezone.now() - timedelta(days=days_ago, hours=24-hour, minutes=random.randint(0, 59))
            
            # Duration between 15 minutes and 4 hours
            duration = random.choices(
                [15, 30, 45, 60, 90, 120, 180, 240],  # minutes
                weights=[10, 20, 25, 20, 15, 7, 2, 1]  # probability weights
            )[0]
            
            end_time = start_time + timedelta(minutes=duration)
            activities_completed = random.randint(1, min(6, duration // 15))  # 1 activity per 15 min avg
            xp_earned = duration // 5  # 1 XP per 5 minutes
            
            StudySession.objects.create(
                user=user,
                start_time=start_time,
                end_time=end_time,
                duration_minutes=duration,
                activities_completed=activities_completed,
                xp_earned=xp_earned
            )
            created_count += 1
    
    print(f"⏱️  Created {created_count} study sessions")

def create_sample_medical_case():
    """Create a comprehensive sample medical case"""
    
    # Check if case already exists
    if Case.objects.filter(title="Emergency Room Crisis - Dizziness Case").exists():
        print("ℹ️  Sample medical case already exists")
        return
    
    # Create the main case
    case = Case.objects.create(
        title="Emergency Room Crisis - Dizziness Case",
        description="A 26-year-old female presents with acute dizziness and hypotension",
        difficulty="medium",
        category="Emergency Medicine",
        patient_info="Age: 26, Gender: Female, Chief Complaint: Dizziness",
        total_xp=200,
        is_active=True
    )
    
    # Step 1: Patient Arrival
    step1 = CaseStep.objects.create(
        case=case,
        step_number=1,
        title="Patient Arrival",
        description="A 26-year-old female walks into your clinic complaining of dizziness that started this morning. She appears anxious and is holding onto the wall for support.",
        patient_info="Age: 26, Gender: Female, Chief Complaint: Dizziness"
    )
    
    # Choices for Step 1
    Choice.objects.create(
        step=step1,
        text="Take vital signs (pulse, BP, temperature)",
        xp_reward=15,
        is_correct=True,
        consequence="Good choice! Vitals show: HR 110 bpm, BP 90/60 mmHg, Temp 98.6°F. The patient appears to have low blood pressure and elevated heart rate."
    )
    
    Choice.objects.create(
        step=step1,
        text="Ask about medical history first",
        xp_reward=10,
        is_correct=False,
        consequence="Patient reports no significant medical history, but mentions she hasn't eaten since yesterday evening. This could be relevant."
    )
    
    Choice.objects.create(
        step=step1,
        text="Order immediate blood work",
        xp_reward=5,
        is_correct=False,
        consequence="While blood work might be helpful, checking vital signs first would be more appropriate for initial assessment."
    )
    
    Choice.objects.create(
        step=step1,
        text="Have patient sit down and rest",
        xp_reward=12,
        is_correct=True,
        consequence="Excellent! Patient safety first. She sits down and reports feeling slightly better. Now you can proceed with assessment."
    )
    
    # Step 2: Further Assessment
    step2 = CaseStep.objects.create(
        case=case,
        step_number=2,
        title="Further Assessment",
        description="After initial stabilization, you need to gather more information. The patient is now seated and appears more comfortable, but still reports feeling lightheaded.",
        patient_info="Vitals: HR 110, BP 90/60, Temp 98.6°F, Patient is seated and stable"
    )
    
    # Choices for Step 2
    Choice.objects.create(
        step=step2,
        text="Take detailed history (eating, medications, symptoms)",
        xp_reward=20,
        is_correct=True,
        consequence="Excellent history taking! Patient reveals she hasn't eaten in 18 hours due to work stress, takes no medications, and the dizziness worsened when standing."
    )
    
    Choice.objects.create(
        step=step2,
        text="Perform focused physical examination",
        xp_reward=18,
        is_correct=True,
        consequence="Good examination technique! You note pale conjunctiva, dry mucous membranes, and positive orthostatic changes (HR increases by 20 bpm when standing)."
    )
    
    Choice.objects.create(
        step=step2,
        text="Check blood glucose immediately",
        xp_reward=25,
        is_correct=True,
        consequence="Excellent clinical thinking! Blood glucose is 65 mg/dL (normal: 70-100). This confirms hypoglycemia as a likely cause."
    )
    
    Choice.objects.create(
        step=step2,
        text="Order CT scan of head",
        xp_reward=0,
        is_correct=False,
        consequence="CT scan is expensive and not indicated for this presentation. The symptoms and findings suggest a metabolic cause rather than neurological."
    )
    
    # Step 3: Diagnosis and Treatment
    step3 = CaseStep.objects.create(
        case=case,
        step_number=3,
        title="Diagnosis and Treatment",
        description="Based on your assessment, the patient has hypoglycemia likely due to prolonged fasting. Blood glucose is 65 mg/dL. How do you proceed?",
        patient_info="Diagnosis: Hypoglycemia (Blood glucose: 65 mg/dL), Patient is conscious and able to swallow"
    )
    
    # Choices for Step 3
    Choice.objects.create(
        step=step3,
        text="Give oral glucose tablets or juice",
        xp_reward=30,
        is_correct=True,
        consequence="Perfect! You give the patient orange juice. Within 10 minutes, she reports feeling much better and her repeat glucose is 85 mg/dL."
    )
    
    Choice.objects.create(
        step=step3,
        text="Start IV and give IV dextrose",
        xp_reward=15,
        is_correct=False,
        consequence="IV dextrose would work, but since the patient is conscious and can swallow, oral glucose is less invasive and equally effective."
    )
    
    Choice.objects.create(
        step=step3,
        text="Recommend eating a full meal immediately",
        xp_reward=10,
        is_correct=False,
        consequence="While food is important, quick-acting glucose is needed first to rapidly correct the hypoglycemia, then followed by a meal."
    )
    
    Choice.objects.create(
        step=step3,
        text="Discharge with instructions to eat regularly",
        xp_reward=5,
        is_correct=False,
        consequence="You should treat the hypoglycemia first before discharge. Patient safety requires correcting the low blood sugar."
    )
    
    print(f"🏥 Created sample medical case: {case.title}")

def create_additional_medical_cases():
    """Create additional medical cases for variety"""
    
    cases_data = [
        {
            'title': 'Chest Pain Emergency',
            'description': 'A 55-year-old male presents with acute chest pain',
            'difficulty': 'hard',
            'category': 'Cardiology',
            'patient_info': 'Age: 55, Gender: Male, Chief Complaint: Chest Pain',
            'steps': [
                {
                    'title': 'Initial Assessment',
                    'description': 'Patient arrives with severe chest pain radiating to left arm',
                    'choices': [
                        ('Order immediate ECG', 25, True, 'ECG shows ST elevation - STEMI confirmed'),
                        ('Give aspirin first', 20, True, 'Good choice - aspirin given'),
                        ('Order chest X-ray', 10, False, 'ECG should be priority'),
                        ('Take detailed history', 5, False, 'Time is critical - ECG first')
                    ]
                }
            ]
        },
        {
            'title': 'Pediatric Fever Case',
            'description': 'A 3-year-old child with high fever and rash',
            'difficulty': 'medium',
            'category': 'Pediatrics',
            'patient_info': 'Age: 3, Gender: Female, Chief Complaint: Fever and Rash',
            'steps': [
                {
                    'title': 'Pediatric Assessment',
                    'description': 'Child has fever 102°F and petechial rash',
                    'choices': [
                        ('Check for neck stiffness', 20, True, 'No neck stiffness noted'),
                        ('Order blood cultures', 25, True, 'Blood cultures ordered'),
                        ('Give antibiotics immediately', 15, False, 'Need diagnosis first'),
                        ('Send home with fever reducer', 0, False, 'Dangerous - needs evaluation')
                    ]
                }
            ]
        }
    ]
    
    created_count = 0
    for case_data in cases_data:
        if not Case.objects.filter(title=case_data['title']).exists():
            case = Case.objects.create(
                title=case_data['title'],
                description=case_data['description'],
                difficulty=case_data['difficulty'],
                category=case_data['category'],
                patient_info=case_data['patient_info'],
                total_xp=150,
                is_active=True
            )
            
            for i, step_data in enumerate(case_data['steps'], 1):
                step = CaseStep.objects.create(
                    case=case,
                    step_number=i,
                    title=step_data['title'],
                    description=step_data['description'],
                    patient_info=case_data['patient_info']
                )
                
                for choice_text, xp, is_correct, consequence in step_data['choices']:
                    Choice.objects.create(
                        step=step,
                        text=choice_text,
                        xp_reward=xp,
                        is_correct=is_correct,
                        consequence=consequence
                    )
            
            created_count += 1
            print(f"🏥 Created medical case: {case.title}")
    
    print(f"📚 Created {created_count} additional medical cases")

def update_user_profiles():
    """Update user profiles with calculated data"""
    
    users = User.objects.all()
    updated_count = 0
    
    for user in users:
        profile = user.studentprofile
        
        # Update total study time from sessions
        total_study_time = StudySession.objects.filter(user=user).aggregate(
            total=models.Sum('duration_minutes')
        )['total'] or 0
        
        if total_study_time != profile.total_study_time:
            profile.total_study_time = total_study_time
            profile.save()
            updated_count += 1
    
    print(f"👤 Updated {updated_count} user profiles")

def print_summary():
    """Print summary of created data"""
    
    print("\n" + "="*60)
    print("🎓 MEDISCOPE STUDENT DATA CREATION SUMMARY")
    print("="*60)
    
    # User counts
    total_users = User.objects.count()
    total_students = StudentProfile.objects.count()
    print(f"👥 Total Users: {total_users}")
    print(f"🎓 Total Students: {total_students}")
    
    # Case counts
    total_cases = Case.objects.count()
    total_steps = CaseStep.objects.count()
    total_choices = Choice.objects.count()
    print(f"🏥 Medical Cases: {total_cases}")
    print(f"📋 Case Steps: {total_steps}")
    print(f"🔘 Choices: {total_choices}")
    
    # Activity counts
    total_achievements = Achievement.objects.count()
    total_activities = Activity.objects.count()
    total_sessions = StudySession.objects.count()
    print(f"🏆 Achievements: {total_achievements}")
    print(f"📝 Activities: {total_activities}")
    print(f"⏱️  Study Sessions: {total_sessions}")
    
    print("\n" + "="*60)
    print("🔑 LOGIN CREDENTIALS")
    print("="*60)
    print("🔧 Admin User:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n🎓 Demo Student:")
    print("   Username: demo_student")
    print("   Password: mediscope123")
    print("\n👥 Other Students:")
    print("   Password: password123")
    print("   Usernames: sarah_miller, alex_kim, mike_rodriguez, etc.")
    
    print("\n" + "="*60)
    print("🚀 NEXT STEPS")
    print("="*60)
    print("1. Run Django migrations: python manage.py migrate")
    print("2. Start the server: python manage.py runserver")
    print("3. Visit: http://localhost:8000")
    print("4. Login with demo credentials above")
    print("5. Explore the gamified medical learning platform!")
    print("="*60)

def main():
    """Main function to create all sample data"""
    
    print("🚀 Starting MediScope student data creation...")
    print("This will create users, profiles, cases, achievements, and activities.")
    print("-" * 60)
    
    try:
        # Create users
        create_admin_user()
        create_demo_users()
        create_sample_students()
        
        # Create medical content
        create_sample_medical_case()
        create_additional_medical_cases()
        
        # Create gamification data
        create_sample_achievements()
        create_sample_activities()
        create_sample_study_sessions()
        
        # Update profiles
        update_user_profiles()
        
        # Print summary
        print_summary()
        
        print("\n✅ Student data creation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during data creation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    if success:
        print("\n🎉 All done! Your MediScope platform is ready for students!")
    else:
        print("\n💥 Something went wrong. Please check the error messages above.")
