import openreview

# API V2
email = ""
client = openreview.api.OpenReviewClient(  # type: ignore
    baseurl="https://api2.openreview.net", username=email, password=""
)
# venue_id = "ICLR.cc/2024/Conference"
venue_id = "ICML.cc/2024/Conference"
venue_group = client.get_group(venue_id)


def get_submissions():
    submissions = client.get_all_notes(content={"venueid": venue_id}, details="replies")
    return submissions


review_name = venue_group.content["review_name"]["value"]
submission_name = venue_group.content["submission_name"]["value"]


def get_reviews(s):
    reviews = [
        openreview.api.Note.from_json(reply).content  # type: ignore
        for reply in s.details["replies"]
        if f"{venue_id}/{submission_name}{s.number}/-/{review_name}"
        in reply["invitations"]
    ]
    return reviews
