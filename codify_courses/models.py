from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=30, verbose_name='language name')
    month_to_learn = models.IntegerField(verbose_name='month to learn')

    class Meta:
        db_table = 'Language'
        verbose_name = 'Language'
        verbose_name_plural = 'Language'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            self.name = str(self.name).title()
        super().save(*args, **kwargs)


class AbstractPerson(models.Model):
    name = models.CharField(max_length=100, verbose_name='FIO')
    email = models.EmailField(max_length=100, verbose_name='email')
    phone_number = models.CharField(max_length=13, verbose_name='phone number')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.phone_number[0] == [0]:
            self.phone_number[0] = ['+996']
        super().save(*args, **kwargs)
        return self.phone_number


class Student(AbstractPerson):
    work_study_place = models.CharField(max_length=255, null=True, blank=True, verbose_name='work study place')
    has_own_notebook = models.BooleanField(default=False, verbose_name='has own notebook')
    preferred_os_choices = [('windows', 'Windows'), ('macos', 'MacOS'), ('linux', 'Linux')]
    preferred_os = models.CharField(max_length=20, choices=preferred_os_choices, verbose_name='preferred_os')

    def __str__(self):
        return self.name


class Mentor(models.Model):
    student = models.ManyToManyField(Student, through='Course', verbose_name='student')
    main_work = models.CharField(max_length=40, null=True, blank=True, verbose_name='main work')
    experience = models.DateField(verbose_name='experience')

    def __str__(self):
        return self.main_work


class Course(models.Model):
    name = models.CharField(max_length=30)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    date_started = models.DateField()
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name='mentor')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='student')

    def __str__(self):
        return self.name

    # def get_end_date(self):
    #     res = self.month_to_learn + self.date_started
    #     return res

