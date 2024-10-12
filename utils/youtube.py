from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

# Function to turn youtube into Langchain Documents
def youtube_to_docs(youtube_url):
    youtube_url = youtube_url.split('&')[0]
    transcripts = YoutubeLoader.from_youtube_url(
        youtube_url, 
        add_video_info=True,
        transcript_format=TranscriptFormat.CHUNKS,
    )
    return transcripts.load()