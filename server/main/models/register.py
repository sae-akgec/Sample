from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone

from .workshop import Workshop, WorkshopPlan
from random import randint
from django.template.loader import render_to_string

upi_address = [
    '9560779366@paytm',
    '9560779366@ybl'
]
class WorkshopRegistrationManager(models.Manager):
    @transaction.atomic
    def do_registration(self, data, participants, fee_amount, send_email=True):
        """
        Create a new registration and its associated ``WorkshopParticipant``.
        Also, send mail to faculty.
        """
        
        # create instance of model
        m = WorkshopRegistration(**data)
        m.save()

        for participant in participants:
            participant['registration'] = m
            WorkshopParticipant.objects.create_participant(data=participant, send_email=False)

        if send_email:
            self.send_email(data, data.get('leader_email'), data.get('team_name'), fee_amount)

        return m

    def send_email(self, data, email, team_name, fee_amount):
        """
        Sends an verification email to particpant.
        """
        subject = "Innovacion'19 Registration Mail"

        mail_message = render_to_string('acc_active_email.html', {
                'upi_address': upi_address[randint(0, 1)],
                'team_name': team_name,
                'fee_amount': fee_amount
            })

        msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(mail_message, "text/html")
        msg.send()

class WorkshopRegistration(models.Model):
    college_name = models.CharField(max_length=130, null=False)
    team_name = models.CharField(max_length=50, null=False)
    ref_code = models.CharField(max_length=20, default="no", null=True, blank=True)
    enroll_date = models.DateField(default=timezone.now, editable=False, null=True)
    is_team_local = models.BooleanField(default=True)
    enroll_status = models.BooleanField(default=False)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    plan = models.ForeignKey(WorkshopPlan, on_delete=models.CASCADE)
    leader_email = models.EmailField(null=False)
    payment_by = models.CharField(max_length=50, null=True, blank=True, default="Not Yet")

    objects = WorkshopRegistrationManager()
    def __str__(self):
        return str(self.team_name) + " - " + str(self.workshop)

class WorkshopParticipantManager(models.Manager):
    @transaction.atomic
    def create_participant(self, data, send_email=True):
        """
        Create a new participant.
        Also, send mail to each student with registration id.
        """
        
        # create instance of model
        m = WorkshopParticipant(**data)
        m.save()

        if send_email:
            self.send_email(data, data.get('email'))

        return m
    
    def send_email(self, data, email):
        """
        Sends an verification email to particpant.
        """
        subject = "Registration Mail"

        message = "Succesfully registerded"

        msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(message, "text/html")
        msg.send()

class WorkshopParticipant(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    
    YEAR_CHOICES = (
        (1, '1st'),
        (2, '2nd'),
        (3, '3rd'),
        (4, '4th')
    )

    name = models.CharField(max_length=50, null=False)
    university_roll = models.CharField(max_length=15, null=False)
    branch = models.CharField(max_length=50, null=False)
    year = models.IntegerField(default=0, null=False, choices=YEAR_CHOICES)
    gender = models.CharField(max_length=10, null=False, choices=GENDER_CHOICES)
    phn_no = models.CharField(null=False, max_length=10, validators=[RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')])
    email = models.EmailField(null=False)
    registration = models.ForeignKey(WorkshopRegistration, on_delete=models.CASCADE, related_name="participants")


    objects = WorkshopParticipantManager()
    def __str__(self):
        return str(self.name + " - " + self.university_roll)

class AacarRegistrationManager(models.Manager):
    @transaction.atomic
    def do_registration(self, data, send_email=True):
        """
        Create a new participant.
        Also, send mail to each student with registration id.
        """
        
        # create instance of model
        m = AacarRegistration(**data)
        m.save()

        if send_email:
            self.send_email(data, data.get('email'), data.get('name'), 300)

        return m
    
    def send_email(self, data, email, name, fee_amount):
        """
        Sends an verification email to particpant.
        """
        subject = "Aacar'6.0 Registration Mail"

        mail_message = render_to_string('aacar_email.html', {
                'upi_address': upi_address[randint(0, 1)],
                'name': name,
                'fee_amount': fee_amount
            })

        msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(mail_message, "text/html")
        msg.send()

class AacarRegistration(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    
    YEAR_CHOICES = (
        (1, '1st'),
        (2, '2nd'),
        (3, '3rd'),
        (4, '4th')
    )

    name = models.CharField(max_length=50, null=False)
    university_roll = models.CharField(max_length=15, null=False)
    branch = models.CharField(max_length=50, null=False)
    year = models.IntegerField(default=0, null=False, choices=YEAR_CHOICES)
    gender = models.CharField(max_length=10, null=False, choices=GENDER_CHOICES)
    phn_no = models.CharField(null=False, max_length=10, validators=[RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')])
    email = models.EmailField(null=False)
    enroll_status = models.BooleanField(default=False)
    enroll_date = models.DateField(default=timezone.now, editable=False, null=True)
    payment_by = models.CharField(max_length=50, null=True, blank=True, default="Not Yet")
    amount = models.IntegerField(default=0, null=True, blank=True)

    objects = AacarRegistrationManager()
    def __str__(self):
        return str(self.name + " - " + self.university_roll)