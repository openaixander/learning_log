from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.


def index(request):
    """
    The home page for learning log
    """
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """
    Show all topics
    # 1. THE QUERY(THE 'ORM' MAGIC)
    # Translation: "Hey Database, give me ALL Topic objects, 
    # and sort them by date_added (newest last).
    """

    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')


    context = {
        'topics':topics,
        }

    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """
    Show a single topic and all its entries
    :param topic_id: selects a single topic with its entry
    """

    # 1. GET THE TOPIC
    # We use .get() because we want exactly one.
    # The 'id' in the database must match the 'topic_id' from the URL.
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    # show list of entries
    # from child to parent in django
    entries = topic.entry_set.order_by('-date_added')

    context = {
        'topic':topic,
        'entries':entries
        }
    
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """
    Add a new topic
    """

    if request.method != 'POST':
        # No data is submitted to the database
        # create a blank form
        form = TopicForm()
    else:
        # it is a post data
        form = TopicForm(data=request.POST)
        # check whether form is valid
        if form.is_valid:
            # save form to the database
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    

    context = {
        'form': form
        }

    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """
    Allows new entries for a specific topic
    """

    # we need to get the topic asap!
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    # since we have the topic now, we start to create the form

    if request.method != 'POST':
        # return an empty form
        form = EntryForm()
    else:
        # this is a post data
        # we need to post the new entry

        form = EntryForm(data=request.POST)
        # we check if the form is valid
        if form.is_valid():
            # if yes, we store that info to the database temporary
            new_entry = form.save(commit=False)
            # now we need to assign that new entry to the whatever topic
            new_entry.topic = topic

            new_entry.save()

            return redirect('learning_logs:topic', topic_id=topic_id)
        

    context = {
        'topic': topic,
        'form': form
        }

    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """
    Edit the prefilled textbox of a specific entry
    
    
    :param entry_id: the id of the entry
    """

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic 
    # now since we have them entries, we need to know the request method

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            # just save the form
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        
    
    context = {
        'entry':entry,
        'form': form,
        'topic': topic
        }
    return render(request, 'learning_logs/edit_entry.html', context)