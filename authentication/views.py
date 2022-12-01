from datetime import datetime
from email import message
import re
from django.http import HttpResponse,HttpRequest
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from authentication.forms import UserRegisterForm
from authentication.models import wordSentiment,p_testd,t_testd
from textblob import TextBlob
from datetime import datetime
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
import re
import joblib
import nltk
import os
import numpy
from catboost import CatBoostClassifier
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,"home.html")

def register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Hi {username},your account was created sucessfully')
            return redirect('home')
    else:
        form=UserRegisterForm()
    return render(request,'register.html',{'form':form})

def profile(request):
    return render(request,'profile.html')

def sentiment_analysis(text):
    blob=TextBlob(text)
    sent_polarity=blob.sentiment.polarity
    if(sent_polarity<-0.1):
        return "Sad"
    elif(sent_polarity>0.1):
        return "Happy"
    else:
        return "Neutral"


def languagetrans(request):
    if request.method=="POST":
        text=request.POST.get('text1')
        if len(text)>=5:
            blob=TextBlob(text)
            result=blob.translate(from_lang="en",to="kn")
            p_testdbb=t_testd(user=request.user,t_text=text,t_result=result,date=datetime.today())
            p_testdbb.save()
            messages.success(request, result)
        else:
            messages.success(request,"Please Enter character more than 5")
    return render(request,'languagetrans.html')

def sentimentWord(request):
    if request.method=="POST":
        text=request.POST.get('text1')
        if len(text)>=20:
            result=sentiment_analysis(text)
            wordsentiemt=wordSentiment(user=request.user,text=text,result=result,date=datetime.today())
            wordsentiemt.save()
            messages.success(request, result)
        else:
            messages.error(request,"Please Enter character more than 20")
    return render(request,'sentiment1.html')
# Create your views here.





def p_test(request):
    if request.method=="POST":
        text=request.POST.get('text1')
        if len(text)<=50:
            messages.success(request,"Enter the text greater than 50")
            return render(request,'p_test.html')
        list_text=[text]
        
        def Lemmatizer():
            lemmatizer=WordNetLemmatizer()
        def clear_text1(data):
            data_length=[]
            lemmatizer=WordNetLemmatizer()
            cleaned_text=[]
            for sentence in tqdm(data):
                sentence=sentence.lower()
                sentence=re.sub('https?://[^\s<>"]+|www\.[^\s<>"]+','',sentence)
                sentence=re.sub('[^0-9a-z]',' ',sentence)
                data_length.append(len(sentence.split()))
                cleaned_text.append(sentence)
            return cleaned_text
        
        text_data=clear_text1(list_text)
        target=joblib.load(os.path.join('./model/target_enc1.pkl'))
        vector=joblib.load(os.path.join('./model/vectorizertext1.pkl'))
        main_model=joblib.load(os.path.join('./model/catboostmodel1.pkl'))
        text_v=vector.transform(text_data).toarray()
        a=main_model.predict(text_v)
        result=target.classes_[a[0][0]]
        p_testdbb=p_testd(user=request.user,p_text=text,p_result=result,date=datetime.today())
        p_testdbb.save()
        str1=""
        
        if result=='ISTJ':
            str1="ISTJ - The Inspector: Reserved and practical, they tend to be loyal, orderly, and traditional.Person: George Washington, Henry Ford"
        elif result=='ISTP':
            str1="ISTP - The Crafter: Highly independent, they enjoy new experiences that provide first-hand learning.Person: Ernest Hemingway"
        elif result=='ISFJ':
            str1="ISFJ - The Protector: Warm-hearted and dedicated, they are always ready to protect the people they care about.Person: William H. Taft"
        elif result=='ISFP':
            str1="ISFP - The Artist: Easy-going and flexible, they tend to be reserved and artistic.Person: Marie Antoineete"
        elif result=='INFJ':
            str1="INFJ - The Advocate: Creative and analytical, they are considered one of the rarest Myers-Briggs types.Person: Adolf Hitler, Plato"
        elif result=='INFP':
            str1="INFP - The Mediator: Idealistic with high values, they strive to make the world a better place. Person: Willian Shakespeare"
        elif result=="INTJ":
            str1="INTJ - The Architect: High logical, they are both very creative and analytical. Peron: Augustus Caesar"
        elif result=="INTP":
            str1="INTP - The Thinker: Quiet and introverted, they are known for having a rich inner world.Person: Albert Einstein, Abraham Lincoln"
        elif result=="ESTP":
            str1="ESTP - The Persuader: Out-going and dramatic, they enjoy spending time with others and focusing on the here-and-now.Person: Malcolm X, Steve Jobs"
        elif result=="ESTJ":
            str1="ESTJ - The Director: Assertive and rule-oriented, they have high principles and a tendency to take charge.Person: Andrew Jackson, Saddam Hussein"
        elif result=="ESFP":
            str1="ESFP - The Performer: Outgoing and spontaneous, they enjoy taking center stage.Person: Ronal Reagan"
        elif result=="ESFJ":
            str1="ESFJ - The Caregiver: Soft-hearted and outgoing, they tend to believe the best about other people.Person: William McKinley"
        elif result=="ENFP":
            str1="ENFP - The Champion: Charismatic and energetic, they enjoy situations where they can put their creativity to work.Person: Charles Dickens, Dr. Seuss"
        elif result=="ENFJ":
            str1="ENFJ - The Giver: Loyal and sensitive, they are known for being understanding and generous.Person: Martin Luther King, Jr, Nelson Mandela"
        elif result=="ENTP":
            str1="ENTP - The Debater: Highly inventive, they love being surrounded by ideas and tend to start many projects (but may struggle to finish them).Person: Leonardo da Vinci"
        else:
            str1="ENTJ - The Commander: Outspoken and confident, they are great at making plans and organizing projects. Person: Alexander Hamilton, Elizabeth I"
        messages.success(request, str1)
    return render(request,'p_test.html')