import feedparser
from MWG_Site.models import Event, Address, MWGUser, Tag
from time import mktime
from datetime import datetime
from django.utils import timezone
import re

def scrape():
	feed = feedparser.parse("http://calendar.activedatax.com/ncstate/RSSSyndicator.aspx?type=N&binary=Y&ics=Y")
	for entry in feed.entries:
		address, created = Address.objects.get_or_create(
            line_1="North Carolina State University",
            line_2='',
            city="Raleigh",
            state_abbrev="NC",
            zipcode="27695",
    	)
		time = timezone.datetime(*entry.published_parsed[:-3])
		time = timezone.make_aware(time, timezone.get_current_timezone())

		#description = re.sub('<[^<]+?>', '', entry.description)

		mwg_user = MWGUser.objects.get(pk=1)
		event, create = Event.objects.get_or_create (
		    name=entry.title,
		    description=entry.description,
		    price=0,
		    time=time,
		    address=address,
		    created_by=mwg_user,
		)

		tag, tagCreated = Tag.objects.get_or_create(
			name = "University Event"
			)
		if create:
			event.tags.add(tag)
			event.save()