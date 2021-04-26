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

    # Records date that data was added:
    added = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def filename(self):
        name = os.path.join(os.getcwd(), 'media/media/text', os.path.basename(self.txt.name))
        return name

    def save(self, *args, **kwargs):
        # Calls save on the model:
        super(Text, self).save(*args, **kwargs)
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
