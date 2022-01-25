from django.shortcuts import render
from django.core.files.storage import default_storage
from django import forms

from . import util

import markdown
import random

import encyclopedia


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#The following function renders a random article. Please consider that in the urls.py
#file, it must be located UNDER the one that says <str:title>. Notice that markdown functions are used in the
#following two functions, because they both need to decode a markdown content. 

def random_page(request):
    entries = util.list_entries() 
    selected_page = random.choice(entries)
    return render(request, "encyclopedia/random_page.html", {
        "random_page": markdown.markdown(util.get_entry(selected_page)),
        "selected_page": selected_page
    })

#This function checks if the file exists or not and renders a page accordingly
#Markdown function renders the text as plain, not as html. Gotta check

def pages(request, title):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "text_content": markdown.markdown(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/not_found.html", {
            "title": title.capitalize()
        })

#Function for search and substring recognition

def search(request):
    #query_dict is our first variable. It is a dictionary with two values: q and the value itself. When we 
    #we tell Django request.GET, we're telling him to store this dict info in a variable.
    #Then, we create a new variable, query, that splits the value from its 'q' name in the dict. Thus
    #we're left with the part of the dict we care.
    #filename is a new variable that will use the info que obtained through calling query.
    query_dict = request.GET
    query = query_dict.get("q")
    filename = f"entries/{query}.md"
    if default_storage.exists(filename):
        return render(request, "encyclopedia/search.html", {
            "text_content": markdown.markdown(util.get_entry(query))
        })
    #This allows the search to recognize the query as a substring belonging to a value in your entries folder
    #It opens up a "Did you mean...?" template. As you can see, you need to create a dictionary to put the 
    #query in it, so that it can append it to the dict if it recognizes it (that's the if statement).
    #Then, it returns a renderized template whose value is that list.
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if query.upper() in entry.upper():
                subStringEntries.append(entry)

        return render(request, "encyclopedia/search_not_found.html", {
            "entries": subStringEntries,
            "query": query
        })

#Required for the link to the new entry page to work properly.

def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")

#Add_entry has some if clauses. First, it saves all the information taken from the POST request in the form
#back in the html form. Then it saves the title in a variable called new_title. The same with the content.
#First if: checks if any of the content gaps is empty.
#Elif: checks if the title already exists, using util.list_entries()
#Else: given that the content is not empty or the title doesn't exist, it will save the entry.

def add_entry(request):
    entry_dict = request.POST
    new_title = entry_dict.get("new_title")
    new_content = entry_dict.get("new_content")
    filename = f"entries/{new_title}.md"
    if new_title == "" or new_content == "":
        return render(request, "encyclopedia/empty.html")
    elif default_storage.exists(filename):
        return render(request, "encyclopedia/page_exists.html", {
            "title": new_title
        })
    else: 
        util.save_entry(new_title, new_content)
        return render(request, "encyclopedia/added_entry.html", {
        "new_title": new_title,
        "new_content": new_content
    })

#This function wants to do the editing process

def edit_entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/edit_entry.html", {'error': "404 Not Found"})

    if request.method == "POST":
        content = request.POST.get("content")
        if content == "":
            return render(request, "encyclopedia/edit_entry.html", {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit_entry.html", {'content': content, 'title': title})

#Still shows a mistake!!!! It says "object of type 'NoneType' has no len()." What the fuck is that!!!!!!

def save_edited_entry(request):
    entry_dict = request.POST
    title = entry_dict.get("titleRead")
    edited_content = entry_dict.get("contentEdit")
    if edited_content == "":
        return render(request, "encyclopedia/empty.html")
    else: 
        util.save_entry(title, edited_content)
        return render(request, "encyclopedia/edited_entry.html", {
        "title": title,
        "content": markdown.markdown(edited_content)
    })
