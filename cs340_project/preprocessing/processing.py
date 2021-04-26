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

        # Actually renaming the columns
        r = Read()
        r.new_rename_column(fname, old_name, new_name)
        f.save()

    return redirect('edit_file', pk=pk)

def drop_cols(request, pk):

    if request.method == 'POST':
        to_drop = request.POST.getlist('cols_to_drop')

        f = Text.objects.get(pk=pk)
        fname = f.filename()

        r = Read()
        r.new_drop_column(fname, to_drop)
        f.save()

    return redirect('edit_file', pk=pk)

def redirect_text_process(request, fn_code = 0):
    '''Idea: pass a function code (int) to fn_code, call the function based off its code'''
    if request.method == "POST":
        content = {}
        content['code'] = True
        content['fn_code'] = str(fn_code)
    # Does nothing with content for now
    return redirect('process_text')

