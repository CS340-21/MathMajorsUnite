# Contains functions for calling processing code in views.py
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from .forms import ImagesForm, TextForm
from .models import Images, Text

# BACKEND IMPORT
import sys, os; sys.path.append('backend')
import reduce_and_normalize
from read import Read

import pandas as pd
import matplotlib.pyplot as plt

def merge(request):

    if request.method == 'POST':
        merge_fname = request.POST.getlist('merge_fname')
        pk_to_merge = request.POST.getlist('merge_files', default = ['BUG'])

        pk_to_merge = [int(pk) for pk in pk_to_merge]

        print('Printing to Test until merge functions implemented')
        print(merge_fname)
        print(pk_to_merge)

        # Collect the files
        df_list = []
        for pk in pk_to_merge:
           # Retrieves the requested file:
            f = Text.objects.get(pk=pk)

            #Computes report for dataframe:
            df = pd.read_csv(f.filename())
            df_list.append(df)

        # Merge files on backend:
        #merge(df_list, merge_fname)

        # Register saved with a model instance

    return redirect('process_text')

def rename(request, pk):

    if request.method == 'POST':
        new_name = request.POST.get('new_name', -1)
        old_name = request.POST.get('c', -1)

        f = Text.objects.get(pk=pk)
        fname = f.filename()

        # Edit file:
        if old_name == -1 or new_name == -1:
            print('early exit')
            return redirect('edit_file', pk=pk)

        r = Read()
        r.new_rename_column(fname, old_name, new_name)
        f.save()

    # Actually renaming the columns

    return redirect('edit_file', pk=pk)

def drop_cols(request, pk):
    print('indrop')

    if request.method == 'POST':
        to_drop = request.POST.getlist('cols_to_drop')

        f = Text.objects.get(pk=pk)
        fname = f.filename()

        r = Read()
        r.new_drop_column(fname, to_drop)
        f.save()

    return redirect('edit_file', pk=pk)

def pass_visualizations(request, pk):
    '''Gets data from visualization call, call visualizer function'''

    if request.method == 'POST':
        col = request.POST.get('chosen_col', None)
        tech = request.POST.get('reduce_technique', None)
        
        f = Text.objects.get(pk=pk)
        df = pd.read_csv(f.filename())
        name = f.title

        if int(tech) >= 0 and col != -1:
            img_path = reduce_and_normalize.get_reduction(df, col, int(tech), name)
            # if f.is_valid():
            #     f.cleaned_data['']
            f.assign_image_name(img_path)

    # Redirects to initial visualization page
    return redirect('visualize', pk=pk)

def redirect_text_process(request, fn_code = 0):
    '''Idea: pass a function code (int) to fn_code, call the function based off its code'''
    #print(fn_code)
    if request.method == "POST":
        content = {}
        content['code'] = True
        content['fn_code'] = str(fn_code)
    # Does nothing with content for now
    #return render(request, 'preprocessing/process_text.html', content)
    return redirect('process_text')

def redirect_img_process(request, fn_code):

    return render(request, 'preprocessing/process_image.html')

