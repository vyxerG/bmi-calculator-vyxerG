from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
# from django.contrib.messages import constants as messages

""" 
Units of measurement:
    There are two main systems for measuring distances and weight, the imperial system of measurement and the metric system of measurement. In the Imperial Knowledgebase, all constants and measures are based on the imperial units. Whereas most countries use the metric system which includes measuring units of meters(height) and grams(wieght), in the United States, the imperial system is used where things are measured in feet, inches, and pounds. 

--------------------------
What Is the Metric System?
The metric system is defined as:

“A decimal system of units based on the meter as a unit length, the kilogram as a unit mass, and the second as a unit time.”

Today, it is commonly referred to as SI, which stands for the Système International. It is also known as the International System of Units.
Countries Using the Metric System:
    All but three countries in the entire world use the metric system of measurement. Some of the major countries using the metric system include:

    Australia
    Canada
    France
    India
    Italy
    Japan
    Mexico
    South Africa
    Spain
    United Kingdom

-----------------------------
What Is the Imperial System?
The imperial system is defined as:

“A system of measurement in use in the United Kingdom and other Commonwealth countries consisting of units such as the inch, the mile and the pound (a unit of weight).”

Countries Using the Imperial System:
    So many countries use the metric system, it might leave you wondering, “Who still uses the Imperial system?” Only three countries in the world use an Imperial system of measurement:

    Liberia
    Myanmar
    United States of America

Is the Metric System Better Than the Imperial System?
You could argue that the metric system is better in today’s world because it is an almost universal standard that is understood no matter where you are. The metric system is also easier to use because of the way all measurements relate to each other. However, if you’re used to using the imperial system, you could argue it is more familiar and therefore easier to use.
    """
# Create your views here.
import re
import traceback
from . models import Bmi

from math import pi
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource
# from numpy import pi
# import  pandas as pd
# from bokeh.resources import CDN
# from bokeh.palettes import Category20c, Spectral6
# from bokeh.transform import cumsum


def home(request):
    try:
        context = {}
        bmi = 0
        state = ""
        if request.method == 'POST':
            weight_metric = request.POST.get('weight-metric')
            weight_imperial = request.POST.get('weight-imperial')
            
        
            if weight_metric:
                weight = request.POST.get('weight-metric')
                height = request.POST.get('height-metric')

                validW = re.match('^[0-9.]+$', weight)
                validH = re.match('^[0-9.]+$', height)

                hasWhiteSpaceW = re.match('^\s+$',weight)
                hasWhiteSpaceH = re.match('^\s+$',height)

                if hasWhiteSpaceW or hasWhiteSpaceH:
                    messages.error(request, "Fields can't be left blank.")
                elif not validW:
                    messages.error(request,f"Unexpected Input for '{weight}'.")
                elif not validH:
                    messages.error(request,f"Unexpected Input for '{height}'.")
                else:
                    weight = float(weight)
                    height = float(height)
                    messages.success(
                    request, "Successfully calculated your BMI in (Metric)")
                    print("Weight: ", weight)
                    print("Height: ", height)
                    bmi = weight / (height**2)
                    

            elif weight_imperial:
                # Convert weight to kilogram
                weight = request.POST.get('weight-imperial') 
                feet = request.POST.get('feet') 
                inches = request.POST.get('inches')

                validW = re.match('^[0-9.]+$', weight)
                validF = re.match('^[0-9.]+$', feet)
                validI = re.match('^[0-9.]+$', inches)

                hasWhiteSpaceW = re.match('^\s+$', weight)
                hasWhiteSpaceF = re.match('^\s+$', feet)
                hasWhiteSpaceI = re.match('^\s+$', inches)

                if hasWhiteSpaceW or hasWhiteSpaceF or hasWhiteSpaceI:
                    messages.error(request, "Fields can't be left blank.")
                elif not validW:
                    messages.error(
                        request, f"Unexpected Input for '{weight}'.")
                elif not validF:
                    messages.error(
                        request, f"Unexpected Input for '{feet}'.")
                elif not validI:
                    messages.error(
                        request, f"Unexpected Input for '{inches}'.")
                else:
                    weight  = float(weight) / 2.205
                    feetValid = float(feet) * 30.48 # convert feet to centimeter
                    inchesValid = float(inches) * 2.54 # convert inches to centimeter
                    height = (feetValid + inchesValid) / 100 # gives us height then convert to meter by dividing by 100.
                    messages.success(
                    request, "Successfully calculated your BMI in (Imperial)")
                    print("Weight: ", weight)
                    print("Height: ", height)
                    bmi = weight / (height**2)

            
            save = request.POST.get('save') # get save input
            print("BMI: ", bmi)
            if save == 'on':
                Bmi.objects.create(user=request.user, weight=weight, height=height, bmi=round(bmi))
            if bmi < 16:
                state = "Severe Thinness"
            elif bmi > 16 and bmi < 17:
                state = "Moderate Thinness"
            elif bmi > 17 and bmi < 18:
                state = "Mild Thinness"
            elif bmi > 18 and bmi < 25:
                state = "Normal"
            elif bmi > 25 and bmi < 30:
                state = "Overweight"
            elif bmi > 30 and bmi < 35:
                state = "Obese Class I"
            elif bmi > 35 and bmi < 40:
                state = "Obese Class II"
            elif bmi > 40:
                state = "Obese Class III"
            print(state)
            # context['bmi'] = bmi
            # context['state'] = state
        dates = []
        bmis = []
        num = 1
        script = ""
        div = ""
        if request.user.is_authenticated:
            dates_queryset = Bmi.objects.all().filter(user = request.user)
            for qr in dates_queryset:
                dates.append(str(qr.date)+"("+str(num)+")")
                bmis.append(int(qr.bmi))
                num += 1

            plot = figure(x_range=dates, plot_height=600, plot_width=600, title="Bmi Statistics",
            toolbar_location="right", tools="pan, wheel_zoom, box_zoom, reset, hover, tap, crosshair")
            plot.title.text_font_size = "20pt"

            plot.xaxis.major_label_text_font_size = "14pt"

            # add a step renderer
            plot.step(dates, bmis, line_width=2)
            plot.legend.lable_text_font_size = '14pt'

            plot.xaxis.major_label_orientation = pi/4
            script, div = components(plot)

        context = {
            "bmi": round(bmi), # Round to the nearest whole number
            "state": state,
            "script": script,
            "div": div,
        }
    except Exception as e:
        messages.error(request, "An Error Occurred: "+str(e))
        print("An Error Occurred: ", traceback.format_exc())
    return render(request, "bmi/index.html", context)