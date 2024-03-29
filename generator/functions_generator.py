import os
import fnmatch
import random


def find(pattern, path):
    """Finds files with a matching name in a directory
    """
    result = []
    for _, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(name)
    return result


def makePlayerCard(name, rank, country, twitch, youtube, twitter, steam):
    """Creates a roster card
    needs to be given all the info on the player
    """

    # find the guardian pictures and shuffle them
    chars = find(name.lower()+"*.jpg", '../images/roster/')
    random.shuffle(chars)

    print(name, rank, country, twitch, youtube,
          twitter, steam, chars, "\n")

    # create the roster card
    rosterCard = "<article class=\""+rank+" "+country+" col\">\n"
    # if no characters found choose a random from the template
    if len(chars) == 0:
        rand = random.choice('wth')
        rosterCard += "<img class=\"player-bg\" src=\"images/roster/0placeholder_"+rand+".jpg\">\n"
    # if one character is found create a simple image
    elif len(chars) == 1:
        rosterCard += "<img class=\"player-bg\" src=\"images/roster/" + \
            chars[0]+"\">\n"
    # if 2+ are found then create the carousel
    else:
        rosterCard += "<div id=\""+name.lower()+"-carousel\" class=\"carousel slide player-bg\" data-ride=\"carousel\"\
        data-interval=\"12000\">\n\
        <div class=\"carousel-inner\">\n\
        <div class=\"carousel-item active\">\n\
        <img src=\"images/roster/"+chars[0]+"\">\n\
        </div>\n\
        <div class=\"carousel-item\">\n\
        <img src=\"images/roster/"+chars[1]+"\">\n\
        </div>\n"
        # if 3 are found then add the 3rd image to the carousel
        if len(chars) == 3:
            rosterCard += "<div class=\"carousel-item\">\n\
            <img src=\"images/roster/"+chars[2]+"\">\n\
            </div>\n"
        rosterCard += "</div>\n\
        <a class=\"carousel-control-prev\" href=\"#"+name.lower()+"-carousel\" data-slide=\"prev\">\n\
        <span class=\"carousel-control-prev-icon\"></span>\n\
        </a>\n\
        <a class=\"carousel-control-next\" href=\"#"+name.lower()+"-carousel\" data-slide=\"next\">\n\
        <span class=\"carousel-control-next-icon\"></span>\n\
        </a>\n\
        </div>"
    rosterCard += "<div class=\"roster-container\">\n\
    <h3 class=\"roster-title\">\n\
    <a target=\"_blank\" href=\"https://steamcommunity.com/"+steam+"\">\n"+name+"</a>\n\
    <img class=\"flag icon\" src=\"images/flags/"+country+".svg\">\n\
    </h3>\n\
    <ul>\n"
    # create each social link if they exist
    if twitch:
        rosterCard += "<li>\n\
        <a target=\"_blank\" href=\"https://www.twitch.tv/"+twitch+"\">\n\
        <img src=\"images/player-card-logos/GlitchBadge_Purple_256px.png\" class=\"icon\">\n\
        </a>\n\
        </li>\n"
    if twitter:
        rosterCard += "<li>\n\
        <a target=\"_blank\" href=\"https://twitter.com/"+twitter+"\">\n\
        <img src=\"images/player-card-logos/Twitter_Social_Icon_Square_Color.png\" class=\"icon\">\n\
        </a>\n\
        </li>\n"
    if youtube:
        rosterCard += "<li>\n\
        <a target=\"_blank\" href=\"https://www.youtube.com/"+youtube+"\">\n\
        <img src=\"images/player-card-logos/youtube_social_square_red.png\" class=\"icon\">\n\
        </a>\n\
        </li>\n"
    rosterCard += "</ul>\n\
    </div>\n\
    </article>\n"
    return rosterCard


def makeHTMLcheckboxes(countries, countriesFull):
    """Creates the html part of the checkboxes
    needs a list of countries which has been cleaned of duplicates. 
    """
    htmlCheckboxes = "<p>Country</p>"
    if len(countries) >= 3:
        htmlCheckboxes = "<input type=\"checkbox\" value=\"all\" id=\"all\">\n\
        <label for=\"all\" class=allnone>\n\
        <p>All</p>\n\
        </label>\n"
    for country in countries:
        count = countriesFull.count(country)
        htmlCheckboxes += "<input type=\"checkbox\" value=\""+country+"\" id=\""+country+"\">\n\
        <label for=\""+country+"\">\n\
        <img src=\"images/flags/"+country+".svg\"><p>"+str(count)+"</p>\n\
        </label>\n"
    if len(countries) >= 3:
        htmlCheckboxes += "<input type=\"checkbox\" value=\"none\" id=\"none\">\n\
        <label for=\"none\" class=allnone>\n\
        <p>None</p>\n\
        </label>\n"
    return htmlCheckboxes


def makeCheckboxVars(countries):
    """Creates the JS variables used for the checkboxes
    """
    checkboxVars = ""
    if len(countries) >= 3:
        checkboxVars += "var all = $(\"input[type='checkbox'][value='all']\");\n\
        all.prop('checked', true);\n\
        var none = $(\"input[type='checkbox'][value='none']\");\n\
        none.prop('checked', false);\n"
    for country in countries:
        checkboxVars += "var "+country+"= $(\"input[type='checkbox'][value='"+country+"']\");\n"\
            + country+".prop('checked', true);\n"
    return checkboxVars


def makePlayerClassVars(countries):
    """Creates JS variables for player card class and sets their default visibility state
    """
    playerClassVars = ""
    for country in countries:
        playerClassVars += "var "+country+"_card = $('."+country+"');\n"\
            + country+"_card.fadeIn();\n"
    return playerClassVars


def makeAllNoneCheck(countries):
    """Creates the JS to check and uncheck all countries at once
    """
    allNoneCheck = ""
    if len(countries) >= 3:
        allNoneCheck += "// if everything is checked this will recheck 'all'\n\
        function allChecked() {\n if("
        for i, country in enumerate(countries):
            if i == 0:
                allNoneCheck += country+".prop('checked')\n"
                continue
            allNoneCheck += "&& "+country+".prop('checked')\n"
        allNoneCheck += "){all.prop('checked', true);} }\n"

        allNoneCheck += "// if everything is unchecked this will recheck 'none'\n\
        function noneChecked() {\n if ("
        for i, country in enumerate(countries):
            if i == 0:
                allNoneCheck += country+".prop('checked') == false\n"
                continue
            allNoneCheck += "&& "+country+".prop('checked') == false\n"
        allNoneCheck += "){none.prop('checked', true);} }\n"
    return allNoneCheck


def makeJScheckboxes(countries):
    """Creates the JS to check or uncheck specific countries
    """
    jsCheckboxes = ""
    if len(countries) >= 3:
        jsCheckboxes += "all.on('change', function () {\n\
        if (all.prop('checked')) {\n none.prop('checked', false);"
        for country in countries:
            jsCheckboxes += country + \
                ".prop('checked', true);\n"+country+"_card.fadeIn();\n"
        jsCheckboxes += "} });\n"

        jsCheckboxes += "none.on('change', function () {if (none.prop('checked')) {\n\
        all.prop('checked', false);\n"
        for country in countries:
            jsCheckboxes += country + \
                ".prop('checked', false);\n"+country+"_card.fadeOut();\n"
        jsCheckboxes += "} });\n"

    for country in countries:
        jsCheckboxes += country+".on('change', function () {\n\
        if ("+country+".prop('checked')) {\n\
        none.prop('checked', false);\n"\
        + country+"_card.fadeIn();\n\
        allChecked();\n\
        } else {\n\
        all.prop('checked', false);\n"\
        + country+"_card.fadeOut();\n\
        noneChecked();\n\
        } });\n"
    return jsCheckboxes
