from django.db import models
from django.db.models.base import Model
from django.db.models.fields import related
from django.urls import reverse
from django.contrib.auth.models import User
from django.views import generic
from PIL import Image

from django.core.cache import cache 
import datetime
from MonkeyBook import settings



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=32, help_text="Никнейм")
    name = models.CharField(max_length=64, help_text="Имя", blank = True)
    surname = models.CharField(max_length=64, help_text="Фамилия", blank = True)
    date_of_birth=models.DateField(help_text="Дата рождения", null=True)
    status = models.CharField(max_length=64, help_text="Статус", blank = True)
    photo = models.ImageField(upload_to = "images" , height_field = None , width_field = None , max_length = 100, null=True, blank=True, help_text="Фото профиля")
    sex = models.BooleanField(default = False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])

    def get_nickname(self):
        return self.nickname

    def get_photo(self):
        return self.photo

    def get_user(self):
        return self.user

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                        seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False 

    def crop_center(self,pil_img, crop_width: int, crop_height: int):
        """
        Функция для обрезки изображения по центру.
        """
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                            (img_height - crop_height) // 2,
                            (img_width + crop_width) // 2,
                            (img_height + crop_height) // 2))
 
 
    def crop_max_square(self,pil_img):
        return self.crop_center(pil_img, min(pil_img.size), min(pil_img.size))

    def save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        try:
            img = Image.open(self.photo.path)
            img = self.crop_max_square(img)
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
        except: pass

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(help_text="Текст поста")
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    note_image = models.ImageField(upload_to = "images" , height_field = None , width_field = None , max_length = 100, null=True, blank=True)

    def get_author(self):
        return self.author

    def get_text(self):
        return self.text

    def get_image(self):
        return self.note_image

    def get_middle_vote(self):
        sum = 0.0
        for vote in self.likes.all():
            sum += vote.vote
        if len(self.likes.all()) != 0:
            sum/=len(self.likes.all())
            if sum.is_integer():
                return int(sum)
            else:
                return str(round(sum,1)).replace(",", ".")
        else:
            return 'Без рейтинга'   

    def get_color(self):

        def avg_color(first, second, ratio):
                fp = [i * (1.0 - ratio) for i in first]
                sp = [i * ratio for i in second]
                return [fp[0] + sp[0], fp[1] + sp[1], fp[2] + sp[2]]

        test = self.get_middle_vote()
        

        if test == 'Без рейтинга': mainRgb = [128, 128, 128] #808080
        else:
            average =  float(test)

            one = [150, 100, 40] #966428
            two = [240, 170, 30] #f0aa1e
            three = [250, 220, 0] #fadc00
            four = [200, 220, 40] #c8dc28
            five = [150, 180, 10] #96b40a

            if average == 1.0: mainRgb = one
            elif average > 1.0 and average < 2.0: mainRgb = avg_color(one, two, (average - 1.0))

            elif average == 2.0: mainRgb = two
            elif average > 2.0 and average < 3.0: mainRgb = avg_color(two, three, (average - 2.0))

            elif average == 3.0: mainRgb = three
            elif average > 3.0 and average < 4.0: mainRgb = avg_color(three, four, (average - 3.0))

            elif average == 4.0: mainRgb = four
            elif average > 4.0 and average < 5.0: mainRgb = avg_color(four, five, (average - 4.0))

            elif average == 5.0: mainRgb = five

        mainColor = '{:02x}{:02x}{:02x}'.format( int(mainRgb[0]), int(mainRgb[1]), int(mainRgb[2]) )

        helpRgb = [i * 0.6 for i in mainRgb]

        helpColor = '{:02x}{:02x}{:02x}'.format( int(helpRgb[0]), int(helpRgb[1]), int(helpRgb[2]) )

        return [str(mainColor), str(helpColor)]

class Friend(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    current_user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, null=True)

    def get_users(self):
        return self.users

    def get_current_user(self):
        return self.current_user

    @classmethod
    def make_friend(cls,current_user,new_friend):
        friend, create = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.remove(new_friend)


class Like(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='likes')

    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

    BANANA_CHOICES = [
    (one, '1'),
    (two, '2'),
    (three, '3'),
    (four, '4'),
    (five, '5'),
    ]

    vote = models.IntegerField(default=three, choices=BANANA_CHOICES)

    class Meta:
        unique_together = ('user', 'note')

class FriendRequest(models.Model):
    sender=models.ForeignKey(User, null=True,related_name='sender', on_delete=models.CASCADE)
    receiver=models.ForeignKey(User, null=True, related_name = 'receiver', on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)

class Dialog(models.Model):
    member1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member1')
    member2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member2')

    class Meta:
        unique_together = ('member1', 'member2')

class Message(models.Model):
    chat = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(help_text="Сообщение")
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_readed = models.BooleanField(default=False)
