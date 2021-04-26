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

import sys, os; sys.path.append('backend')
import reduce_and_normalize
from read import Read

# -----------------------------
import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

import io
import urllib, base64
# -----------------------------

def index(request):
  return render(request, 'preprocessing/index.html')

def about(request):
  return render(request, 'preprocessing/about.html')

def text(request):
  # Allows us to send data back to the HTML page
  context = {}

  txts = Text.objects.all()
  context['texts'] = txts

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

def process_text(request):
  # Processing text data (i.e. user interaction)
  context = {}

  txts = Text.objects.all()
  context['texts'] = txts
  context['nfiles'] = Text.objects.count()

  return render(request, 'preprocessing/process_text.html', context)

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
    
    context['report'] = report
    context['columns'] = [str(c) for c in report.columns]

    context['name'] = f.title

  return render(request, 'preprocessing/report.html', context)

def edit_file(request, pk):
  '''Edits data for one individual file'''
  context = {}

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

  # Retrieve file from database:
  f = Text.objects.get(pk=pk)
  context['name'] = f.title

  # Make pandas dataframe of file:
  df = pd.read_csv(f.filename())
  context['columns'] = df.columns

  context['pk'] = pk

  if request.method == 'POST':
    col = request.POST.get('chosen_col', -1)
    tech = request.POST.get('reduce_technique', -1)
    if int(tech) >= 0 and col != "-1":
      df = pd.read_csv(f.filename())
      name = f.title

      myplot = reduce_and_normalize.get_reduction(df, col, tech, name)
      if myplot is None:
        context['hist_error'] = -1
      else:
        context['img'] = myplot

  return render(request, 'preprocessing/visualize.html', context)

def regression_main(request):
  # Loads the regression page
  context = {}

  context['texts'] = Text.objects.all()

  if request.method == 'POST':
    pk = request.POST.get('pk', -1)
    if pk == -1:
      return render(request, 'preprocessing/regression_main.html', context)

    f = Text.objects.get(pk=pk)
    context['pk'] = pk
    context['name'] = f.title

  return render(request, 'preprocessing/regression_main.html', context)

def regression_file(request, pk):

  context = {}

  f = Text.objects.get(pk=pk)
  context['name'] = f.title
  context['pk'] = pk

  if request.method == 'POST':

    cols = pd.read_csv(f.filename()).columns
    context['columns'] = cols

    chosen_col = request.POST.get('chosen_col', -1)
    if chosen_col != "-1":
      r = Read()
      out1, out2, out_dict, r2 = r.regress(f.filename(), chosen_col)
      if out1 != -1 and \
          out2 != -1 and \
          (out_dict != -1 and out_dict != 0) and\
          r2 != -1:
        context['ccol'] = chosen_col
        context['reg_dict'] = out_dict
        context['r2'] = r2
        context['reg_message1'] = out1
        context['reg_message2'] = out2
      elif out_dict == 0:
        context['error_message'] = 1

  return render(request, 'preprocessing/regression_file.html', context)
