from django.core.management.base import BaseCommand
from cases.models import Case, CaseStep, Choice

class Command(BaseCommand):
    help = 'Creates advanced medical simulation cases'
    
    def handle(self, *args, **options):
        print("Creating advanced medical cases...")
        
        # ========== TRAUMA CASE ==========
        trauma_case, created = Case.objects.get_or_create(
            title='Trauma: Multi-System Injury',
            defaults={
                'description': 'A 25-year-old motorcyclist involved in high-speed collision. Manage multiple traumatic injuries.',
                'patient_info': 'Patient: Marcus Johnson, 25-year-old male\nMechanism: Motorcycle vs car at 60 mph\nVital Signs: BP 90/60, HR 130, RR 28, GCS 13\nPrimary Survey: Airway patent, breath sounds decreased on left, abdomen distended\nSecondary: Obvious left femur fracture, multiple abrasions',
                'difficulty': 'hard',
                'category': 'Emergency Medicine',
                'total_xp': 250,
            }
        )
        
        if created:
            # Create trauma case steps
            step1 = CaseStep.objects.create(
                case=trauma_case,
                step_number=1,
                title='Emergency Department Presentation',
                description='Patient arrives via ambulance. Primary survey shows decreased breath sounds on left. What is your immediate priority?',
                patient_info='Airway patent, breath sounds decreased on left, abdomen distended'
            )
            
            # Add choices for step1
            Choice.objects.bulk_create([
                Choice(step=step1, text='Chest tube insertion for pneumothorax', xp_reward=40, is_correct=True, consequence='Correct! Tension pneumothorax is life-threatening and requires immediate decompression.'),
                Choice(step=step1, text='IV access and fluid resuscitation', xp_reward=0, is_correct=False, consequence='In trauma, airway and breathing issues take priority.'),
                Choice(step=step1, text='X-ray of chest and pelvis', xp_reward=0, is_correct=False, consequence='Imaging should not delay life-saving interventions.'),
                Choice(step=step1, text='Intubation immediately', xp_reward=0, is_correct=False, consequence='Airway is patent, breathing issue should be addressed first.')
            ])
            
            step2 = CaseStep.objects.create(
                case=trauma_case,
                step_number=2,
                title='Investigation Phase',
                description='After chest tube placement, patient remains hypotensive. Abdomen is distended and tender. Next step?',
                patient_info='BP 85/55, HR 135, RR 24'
            )
            
            # Add choices for step2
            Choice.objects.bulk_create([
                Choice(step=step2, text='FAST exam (Focused Assessment with Sonography)', xp_reward=45, is_correct=True, consequence='Excellent! FAST exam quickly identifies intra-abdominal bleeding.'),
                Choice(step=step2, text='CT scan of abdomen', xp_reward=0, is_correct=False, consequence='CT is inappropriate for unstable patients.'),
                Choice(step=step2, text='Diagnostic peritoneal lavage', xp_reward=0, is_correct=False, consequence='FAST has replaced this invasive technique.'),
                Choice(step=step2, text='More IV fluids', xp_reward=0, is_correct=False, consequence='Fluids alone won\'t address the bleeding.')
            ])
            
            step3 = CaseStep.objects.create(
                case=trauma_case,
                step_number=3,
                title='Surgical Decision',
                description='FAST exam shows free fluid in abdomen. Patient BP drops to 80/50 despite fluids. What now?',
                patient_info='Positive FAST exam, worsening hypotension'
            )
            
            # Add choices for step3
            Choice.objects.bulk_create([
                Choice(step=step3, text='Emergency laparotomy', xp_reward=50, is_correct=True, consequence='Perfect! Unstable patient needs immediate surgery.'),
                Choice(step=step3, text='More IV fluids and blood', xp_reward=0, is_correct=False, consequence='Resuscitation should continue during transport to OR.'),
                Choice(step=step3, text='CT scan for better imaging', xp_reward=0, is_correct=False, consequence='Unstable patients should go directly to OR.'),
                Choice(step=step3, text='Angiography for embolization', xp_reward=0, is_correct=False, consequence='Not appropriate for abdominal trauma.')
            ])
        
        # ========== STROKE CASE ==========
        stroke_case, created = Case.objects.get_or_create(
            title='Neurology: Acute Stroke Protocol',
            defaults={
                'description': 'A 68-year-old woman with sudden onset weakness and speech difficulty. Time is brain!',
                'patient_info': 'Patient: Helen Rodriguez, 68-year-old female\nChief Complaint: Sudden left-sided weakness and slurred speech\nOnset: 90 minutes ago, witnessed by husband\nVital Signs: BP 180/100, HR 88, RR 16, Temp 98.6°F\nNIHSS: 12 (moderate stroke)\nHistory: Atrial fibrillation, not on anticoagulation',
                'difficulty': 'hard',
                'category': 'Neurology',
                'total_xp': 220,
            }
        )
        
        if created:
            # Create stroke case steps
            step1 = CaseStep.objects.create(
                case=stroke_case,
                step_number=1,
                title='Emergency Assessment',
                description='Patient presents with acute stroke symptoms. Last known well 90 minutes ago. First priority?',
                patient_info='Left-sided weakness, slurred speech, NIHSS 12'
            )
            
            # Add choices for step1
            Choice.objects.bulk_create([
                Choice(step=step1, text='Stat CT head without contrast', xp_reward=35, is_correct=True, consequence='Correct! CT is essential to rule out hemorrhage.'),
                Choice(step=step1, text='MRI brain with DWI', xp_reward=0, is_correct=False, consequence='MRI takes too long in acute stroke setting.'),
                Choice(step=step1, text='Carotid ultrasound', xp_reward=0, is_correct=False, consequence='Not the first priority in acute stroke.'),
                Choice(step=step1, text='Echocardiogram', xp_reward=0, is_correct=False, consequence='This can wait until after initial management.')
            ])
            
            step2 = CaseStep.objects.create(
                case=stroke_case,
                step_number=2,
                title='Treatment Decision',
                description='CT shows no hemorrhage. Patient is within 3-hour window. NIHSS is 12. What treatment?',
                patient_info='BP 175/95, no hemorrhage on CT'
            )
            
            # Add choices for step2
            Choice.objects.bulk_create([
                Choice(step=step2, text='IV tPA (tissue plasminogen activator)', xp_reward=40, is_correct=True, consequence='Excellent! IV tPA within 3 hours improves outcomes.'),
                Choice(step=step2, text='Aspirin 325mg', xp_reward=0, is_correct=False, consequence='Not sufficient for acute ischemic stroke.'),
                Choice(step=step2, text='Heparin infusion', xp_reward=0, is_correct=False, consequence='Not standard for acute stroke management.'),
                Choice(step=step2, text='Mechanical thrombectomy only', xp_reward=0, is_correct=False, consequence='tPA should be given first if eligible.')
            ])
            
            step3 = CaseStep.objects.create(
                case=stroke_case,
                step_number=3,
                title='Rescue Therapy',
                description='After tPA, patient shows minimal improvement. CTA shows large vessel occlusion. Next step?',
                patient_info='NIHSS still 10, right MCA occlusion on CTA'
            )
            
            # Add choices for step3
            Choice.objects.bulk_create([
                Choice(step=step3, text='Mechanical thrombectomy', xp_reward=45, is_correct=True, consequence='Perfect! Large vessel occlusion warrants thrombectomy.'),
                Choice(step=step3, text='Wait and observe', xp_reward=0, is_correct=False, consequence='Time is brain! Intervention is needed.'),
                Choice(step=step3, text='Increase tPA dose', xp_reward=0, is_correct=False, consequence='tPA dosing is standardized and should not be increased.'),
                Choice(step=step3, text='Start dual antiplatelet therapy', xp_reward=0, is_correct=False, consequence='Not appropriate immediately after tPA.')
            ])
        
        # (Repeat similar pattern for cardiac_case and tox_case)
        # ... [Add cardiac and tox cases following same pattern] ...
        
        self.stdout.write(self.style.SUCCESS('Successfully created advanced cases!'))