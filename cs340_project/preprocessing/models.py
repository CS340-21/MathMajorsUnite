import os
import pandas as pd
from django.db import models

# Create your models here.

# Class for the image directory zips
class Images(models.Model):
    title = models.CharField(max_length = 100)
    img_zip = models.FileField(upload_to = 'media/images/')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Makes sure this class deletes the file from local storage
        self.img_zip.delete()
        super().delete(*args, **kwargs)

class Text(models.Model):
    title = models.CharField(max_length = 100)
    txt = models.FileField(upload_to = 'media/text/', help_text = 'CSV File',
        verbose_name = 'CSV')

    rows = models.PositiveIntegerField(default = 0)
    cols = models.PositiveIntegerField(default = 0)

    # Image name:
    img_location = models.CharField(max_length = 100, default = None)
    #img_location = ""

    # Records date that data was added:
    added = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def filename(self):
        name = os.path.join(os.getcwd(), 'media/media/text', os.path.basename(self.txt.name))
        return name

    # Functionality to deal with images:
    def assign_image_name(self, name):

        # if self.img_location is not None:
        #     os.remove(self.img_location)

        self.img_location = name
        print(name)
        print(self.img_location)
        self.save()

    def get_image_name(self):
        if self.img_location is not None:
            return self.img_location
        else:
            print(self.img_location)
            return -1 # No image

    def save(self, *args, **kwargs):
        # Calls save on the model:
        super(Text, self).save(*args, **kwargs)
        #if self.txt.name is not None:
        fname = self.filename()

        df = pd.read_csv(fname)

        self.rows = df.shape[0]
        self.cols = df.shape[1]

        # Saves the new data for the model again
        super(Text, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Makes sure this class deletes the file from local storage
        self.txt.delete(save = False) # Doesn't save, avoids errors
        super().delete(*args, **kwargs)
