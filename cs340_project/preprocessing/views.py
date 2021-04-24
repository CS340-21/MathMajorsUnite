from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from .forms import ImagesForm, TextForm
from .models import Images, Text

import pandas as pd
import sys; sys.path.append('media')
import os
import json

def index(request):
  return render(request, 'preprocessing/index.html')

def about(request):
  return render(request, 'preprocessing/about.html')

def image(request):
  # Allows us to send data back to the page
  context = {}

  # Image loading code:
  if request.method == "POST":
    form = ImagesForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      
  else: # If not a post request, instantiate empty form
    form = ImagesForm()

  #  uploaded_file = request.FILES['img_data']
  #  fs = FileSystemStorage()
  #  name = fs.save(uploaded_file.name, uploaded_file)
  #  context['url'] = fs.url(name)

  imgs = Images.objects.all()
  context['images'] = imgs

  # Get form
  context['form'] = form

  return render(request, 'preprocessing/image.html', context)

def delete_image(request, pk):
  if request.method == 'POST':
    img = Images.objects.get(pk=pk)
    img.delete()
  return redirect('preprocessing-image')

def text(request):
  # Allows us to send data back to the HTML page
  context = {}

  # # Image loading code:
  # if request.method == "POST":
  #   form = TextForm(request.POST, request.FILES)
  #   if form.is_valid():
  #     form.save()
      
  # else: # If not a post request, instantiate empty form
  #   form = TextForm()

  txts = Text.objects.all()
  context['texts'] = txts

  # Get form
  # context['form'] = form
  return render(request, 'preprocessing/text.html', context)

def upload_text(request):
  # Image loading code:
  if request.method == "POST":
    form = TextForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('preprocessing-text')  
  else:
    form = TextForm()
  return render(request, 'preprocessing/upload_text.html', {'form':form})


def delete_text(request, pk):
  '''Allows you to delete text from database'''
  if request.method == 'POST':
    img = Text.objects.get(pk=pk)
    img.delete()
  return redirect('preprocessing-text')

#def start_text_button(request):
#  return redirect('preprocessing-text')

def process_text(request):
  # Processing text data (i.e. user interaction)

  context = {}

  # # Image loading code:
  # if request.method == "POST":
  #   form = TextForm(request.POST, request.FILES)
  #   if form.is_valid():
  #     form.save()
      
  # else: # If not a post request, instantiate empty form
  #   form = TextForm()

  txts = Text.objects.all()
  context['texts'] = txts
  context['nfiles'] = Text.objects.count()

  # fs = Text.objects.values('txt')[0]['txt']

  # file_list = list(Text.objects.values('txt'))
  # for f in file_list:
  #   temp_df = pd.read_csv(os.path.join('media', f['txt']))
  #   Text.objects.update_or_create(
  #     txt = f['txt'], 
  #     rows = temp_df.shape[0], 
  #     cols = temp_df.shape[1]
  #   )

  # #sys.path.append('media')
  # df = pd.read_csv(os.path.join('media', fs))
  # #df = pd.read_csv(fs)
  # #df = pd.read_csv('../media/text/upec_meta.csv')
  # print(df.shape)

  # Get form
  #context['form'] = form

  #df = pd.DataFrame(txts)
  #print(df)

  return render(request, 'preprocessing/process_text.html', context)

def process_image(request):
  # Processing image data (i.e. user interaction)
  return render(request, 'preprocessing/process_image.html')

def generate_report(request, pk):
  '''Generates report for a given model'''
  context = {}

  if request.method == 'POST':
    # Retrieves the requested file:
    f = Text.objects.get(pk=pk)

    #Computes report for dataframe:
    df = pd.read_csv(f.filename())
    report = df.describe().T
    report['Column Name'] = report.index
    cols = report.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    report = report[cols]

    json_records = report.reset_index().to_json(orient = 'records')
    data = []
    data = json.loads(json_records)
    #context['report'] = data
    context['report'] = report
    context['columns'] = [str(c) for c in report.columns]

    context['name'] = f.title

  return render(request, 'preprocessing/report.html', context)

def edit_file(request):
  '''Edits data for one individual file'''
  context = {}

  if request.method == 'POST':
    pk = request.POST.getlist('pk')[0]

  # Retrieve file from database:
  f = Text.objects.get(pk=pk)
  context['name'] = f.title

  # Make pandas dataframe of file:
  df = pd.read_csv(f.filename())
  context['columns'] = df.columns

  context['pk'] = pk

  return render(request, 'preprocessing/edit_file.html', context)

def visualize_data(request, pk):
  context = {}

  # if request.method == 'POST':
  #   pk = request.POST.getlist('pk')[0]

  # Retrieve file from database:
  f = Text.objects.get(pk=pk)
  context['name'] = f.title

  # Make pandas dataframe of file:
  df = pd.read_csv(f.filename())
  context['columns'] = df.columns

  context['pk'] = pk

  return render(request, 'preprocessing/visualize.html', context)
