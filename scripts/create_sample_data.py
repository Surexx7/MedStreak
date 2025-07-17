"""
Script to create sample data for MediScope Django application
Run this script to populate the database with sample cases, quizzes, and other data
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/path/to/your/project')  # Update this path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediscope.settings')
django.setup()

from cases.models import Case, CaseStep, Choice
from django.contrib.auth.models import User
from core.models import UserProfile

def create_sample_case():
    """Create a sample medical case"""
    
    # Create the main case
    case = Case.objects.create(
        title="Emergency Room Crisis - Dizziness Case",
        description="A 26-year-old female presents with acute dizziness",
        difficulty="medium",
        category="Emergency Medicine",
        patient_info="Age: 26, Gender: Female, Chief Complaint: Dizziness",
        total_xp=200
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
    
    print(f"Created sample case: {case.title}")
    return case

def create_sample_users():
    """Create sample users for testing"""
    
    # Create admin user
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
        UserProfile.objects.create(
            user=admin_user,
            total_xp=5000,
            level=5,
            current_streak=15,
            cases_completed=25,
            quiz_accuracy=92.5
        )
        print(f"Created admin user: {admin_user.username}")
    
    # Create sample student users
    sample_users = [
        {'username': 'sarah_m', 'first_name': 'Sarah', 'last_name': 'Miller', 'xp': 3245, 'level': 3},
        {'username': 'alex_k', 'first_name': 'Alex', 'last_name': 'Kim', 'xp': 3120, 'level': 3},
        {'username': 'mike_r', 'first_name': 'Mike', 'last_name': 'Rodriguez', 'xp': 2756, 'level': 2},
        {'username': 'emma_j', 'first_name': 'Emma', 'last_name': 'Johnson', 'xp': 2234, 'level': 2},
    ]
    
    for user_data in sample_users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': f"{user_data['username']}@example.com",
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            UserProfile.objects.create(
                user=user,
                total_xp=user_data['xp'],
                level=user_data['level'],
                current_streak=5,
                cases_completed=10,
                quiz_accuracy=85.0
            )
            print(f"Created sample user: {user.username}")

def main():
    """Main function to create all sample data"""
    print("Creating sample data for MediScope...")
    
    # Create sample users
    create_sample_users()
    
    # Create sample case
    create_sample_case()
    
    print("Sample data creation completed!")

if __name__ == '__main__':
    main()
