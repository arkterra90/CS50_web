from django.shortcuts import render
from markdown2 import Markdown
import random
from . import util

# converts html to markdown
def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

# renders homepage for user
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# renders an entry page upon user request. First checks to see
# if the entry page exist and sends error if None. Renders entry 
# page if entry exist.
def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request,"encyclopedia/error.html",{
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": html_content
        })
    
# Using the search input if a user inputs an exact match to an entry the user
# is rendered the matching entry page. If the users search has similarities to 
# an entry the user is presented with a list of possible matches using the 
# rocommendation variable.
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        entryExist = convert_md_to_html(entry_search)
        if entryExist is not None:
            return render(request, "encyclopedia/entry.html",{
            "title": entry_search,
            "content": entryExist
        })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })
        
# If method is GET a blank new entry page is render for user input. If method is POST the title is checked to see
# if the entry already exist using util function get_entry. An error message is displayed if content already exist.
# Once a new entry title is verified a new entry is created using util function save_entry and the new entries
# entry page is rendered to the user.
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exist"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content":  html_content
            })

# Renders edit.html page with title and textarea boxes pre-populated with
# content from the page the user is attempting to edit using the title and content variables.
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })
    
# Saves content entered on edit.html using the util function save_entry.
# Then renders updated entry page.
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": html_content
        })

# Loads a random page by creating allEntries list, choosing a random entry
# using the random library, and then rendering the entry page populated
# by the rand_entry selection.
def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert_md_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
    })