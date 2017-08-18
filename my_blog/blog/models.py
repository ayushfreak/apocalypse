from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from .utils import get_read_time
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib
#https://docs.djangoproject.com/en/1.11/topics/db/managers/#modifying-a-manager-s-initial-queryset
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


def user_directory_path(instance, filename):
    # https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.FileField.upload_to
    return '%s/%s' %(instance.title, filename)

def user_profile_path(instance, filename):
    return '%s/%s' %(instance.user, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    user_info=models.TextField(max_length=300,null=True)
    image=models.ImageField(upload_to=user_profile_path,null=True,blank=True)

    def __str__(self):
        return "{}'s profile".format(self.user.username)

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False


    def profile_image_url(self):
        if self.image:
            print (self.image.url)
            return self.image.url
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
        go_uid= SocialAccount.objects.filter(user_id=self.user.id, provider='google')
        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
        elif len(go_uid):
            return self.user.socialaccount_set.filter(provider='google')[0].extra_data['picture']
        else:
            mail=self.user.email.encode('utf-8')
            return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(mail).hexdigest())
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = RichTextField()
    image=models.ImageField(upload_to=user_directory_path,null=True,blank=True,
        width_field='width_field',height_field='height_field')
    height_field=models.IntegerField(default=0,null=True)
    width_field=models.IntegerField(default=0,null=True)
    STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'),)
    #provides choices to the text field
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,related_name='blog_posts')
#why related_name is used
#http://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django
    publish = models.DateTimeField(default=timezone.now)
#effectively doing the same thing as auto_now_add (the default value for the field
#will be the current date), but you can also set the field manually on the model and save it.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
#auto_now_add tells Django that when you add a new row,you want the current date & time added.
#auto_now tells Django to add the current date & time will be added EVERY time the record is saved.
    objects = models.Manager()
# The default manager which is explicitly declared if modification are done as in published.
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,
            self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
#https://docs.djangoproject.com/en/1.8/ref/models/instances/#get-absolute-url
#https://docs.djangoproject.com/en/1.8/ref/urlresolvers/#reverse
#https://www.tutorialspoint.com/python/time_strftime.htm


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    @property
    def read_time(self):
        "Returns the time to read"
        time=get_read_time(self.body)
        return time
# using property we can call read_time without () as () can not be used in template
