from django.db import models
from section.models import Division, Department, Title, Classification
from PIL import Image
import requests

data = requests.get("https://restcountries.com/v3.1/all").json()
countries = [(d['name']['common'], d['name']['common']) for d in data]

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Employee(models.Model):
    # Personal details
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    employee_name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=[('F', 'F'), ('M', 'M')])
    nationality = models.CharField(max_length=50, null=True, blank=True)
    marital_status = models.CharField(max_length=50, choices=[('Single', 'Single'), 
                                                            ('Married', 'Married'), ('Widowed', 'Widowed'), ('Divorced', 'Divorced')])
    spouse = models.CharField(max_length=50, null=True, blank=True)
    staff_id = models.CharField(max_length=50, null=True, blank=True)
    tin = models.CharField(max_length=50, null=True, blank=True)
    sshfc = models.CharField(max_length=50, null=True, blank=True)
    national_id = models.BigIntegerField(null=True, blank=True)
    passport = models.CharField(max_length=6, null=True, blank=True)
    drivers_license = models.CharField(max_length=10, null=True, blank=True)
    voters_id = models.BigIntegerField(null=True, blank=True)
    account_name = models.CharField(max_length=50, null=True, blank=True)
    bank = models.CharField(max_length=50, null=True, blank=True, choices=[('Yonna Islamic Microfinance', 'Yonna Islamic Microfinance')])
    swift_code = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.BigIntegerField(null=True, blank=True)

    skills = models.ManyToManyField(Skill)

    # Social media links
    facebook_link = models.CharField(max_length=200, null=True, blank=True)
    instagram_link = models.CharField(max_length=200, null=True, blank=True)
    twitter_link = models.CharField(max_length=200, null=True, blank=True)
    linkedin_link = models.CharField(max_length=200, null=True, blank=True)

    # Contact details
    country = models.CharField(max_length=100, null=True, blank=True, choices=sorted(countries, key=lambda x: x[0]))
    street = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.IntegerField()
    cug_number = models.CharField(max_length=12, null=True, blank=True)
    mobile_1 = models.CharField(max_length=12, null=True, blank=True)
    mobile_2 = models.CharField(max_length=12, null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True)
    work_email = models.EmailField(null=True, blank=True)

    # Job details
    hired_date = models.DateField()
    resigned_date = models.DateField(null=True, blank=True)
    contract_commence = models.DateField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    e_status = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Probation', 'Probation'),
        ('Temporary', 'Temporary'),
        ('Contract', 'Contract'),
        ('Independent Contract', 'Independent Contract'),
        ('Intern', 'Intern'),
        ('Attachment', 'Attachment'),
        ('On Leave', 'On Leave'),
        ('On Suspension', 'On Suspension'),
        ('Resigned', 'Resigned'),
        ('Fired', 'Fired'),
    ]
    employment_status = models.CharField(max_length=50, choices=sorted(e_status, key=lambda x: x[0]))
    probation_commence = models.DateField(null=True, blank=True)
    probation_end = models.DateField(null=True, blank=True)
    warning = models.IntegerField(default=0)

    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True, blank=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.employee_name
    

    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)

        image = Image.open(self.image.path)
        if image.height > 264 or image.width > 191:
            output_size = (264, 191)
            image.thumbnail(output_size)
            image.save(self.image.path)