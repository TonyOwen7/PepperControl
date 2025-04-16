from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Speech
from .forms import SpeechForm
from control.module.pepper_speach.pepper_speach import pepper_speak


@login_required
def set_favorite_speech(request, speech_id):
    print("set favoririte speech")
    # Get all user's speeches
    user_speeches = Speech.objects.filter(user=request.user)

    # Unset favorite flag for all speeches first
    user_speeches.update(is_favorite=False)
    
    # Get the specific speech object
    speech = get_object_or_404(Speech, id=speech_id, user=request.user)
    print(speech)
    # Set this speech as favorite
    speech.is_favorite = True
    speech.save()
    
    # Redirect back to the speeches list
    return redirect('user_speeches')

@login_required
def speech_list(request):
    speeches = Speech.objects.filter(user=request.user)
    return render(request, 'speech/user_speeches.html', {'speeches': speeches})

@login_required
def create_speech(request):
    if request.method == 'POST':
        form = SpeechForm(request.POST)
        if form.is_valid():
            speech = form.save(commit=False)
            speech.user = request.user
            speech.is_favorite = False
            speech.save()
            return redirect('/speech/user_speeches')
    else:
        form = SpeechForm()
    return render(request, 'speech/speech_form.html', {'form': form})

@login_required
def edit_speech(request, speech_id):
    speech = get_object_or_404(Speech, id=speech_id, user=request.user)
    if request.method == 'POST':
        form = SpeechForm(request.POST, instance=speech)
        if form.is_valid():
            speech.is_favorite = False
            form.save()
            return redirect('/speech/user_speeches')
    else:
        form = SpeechForm(instance=speech)
    return render(request, 'speech/speech_form.html', {'form': form})

@login_required
def delete_speech(request, speech_id):
    speech = get_object_or_404(Speech, id=speech_id, user=request.user)
    speech.delete()
    return redirect('/speech/user_speeches')

@login_required
def play_speech(request, speech_id):
    speech = get_object_or_404(Speech, id=speech_id, user=request.user)
    pepper_speak(speech.content)
    return redirect('/speech/user_speeches')

@login_required
def toggle_favorite_speech(request, speech_id):
    user_speeches = Speech.objects.filter(user=request.user)
    
    # Get the speech object
    speech = get_object_or_404(Speech, id=speech_id, user=request.user)
    
    # Toggle favorite status
    if speech.is_favorite:
        speech.is_favorite = False
    else:
        # Unfavorite all other speeches first
        user_speeches.update(is_favorite=False)
        speech.is_favorite = True
        
    speech.save()
    return redirect('user_speeches')

