import pandas as pd
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
import pandas as pd
import time
from itertools import cycle
from youtube_transcript_api.proxies import WebshareProxyConfig

def gather_data():
    url = "https://raw.githubusercontent.com/Standup4AI/dataset/main/CSV_clean/StandUp4AI_v1.csv"
    df = pd.read_csv(url)

    df_es = df[df['lang'] == 'es']

    output_path = "../../datasets/standup4ai_es.csv"
    df_es.to_csv(output_path, index=False)

    print(f"{len(df_es)} Spanish entries and saved to {output_path}")

def data_profiling():
    df = pd.read_csv("../../datasets/standup4ai_es.csv")

    total_duration = df['duration'].sum()
    unique_channels = df['channel_id'].unique()
    print(f"Total duration: {total_duration}")
    print(f"Unique channels: {unique_channels}")
    print(f"Total rows: {len(df)}")
    return unique_channels

def get_transcripts(csv_file, languages=['es']):
    df = pd.read_csv(csv_file)
    transcripts_dir = os.path.join("..", "..", "datasets", "standup4ai_es_transcripts")
    os.makedirs(transcripts_dir, exist_ok=True)
    ytt_api = YouTubeTranscriptApi()

    for url in df['url']:
        video_id = url.split("v=")[-1]
        output_file = os.path.join(transcripts_dir, f"{video_id}.txt")
        if os.path.exists(output_file):
            print(f"Transcript already exists for {video_id}, skipping.")
            continue
        try:
            transcript_obj = ytt_api.fetch(video_id, languages=languages)
            lines = [snippet.text for snippet in transcript_obj.snippets]
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            print(f"saved transcript for {video_id}")
        except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript) as e:
            print(f"transcript not available for {video_id}: {e}")
        except Exception as e:
            print(f"error for {video_id}: {e}")
        
        time.sleep(10)


if __name__ == "__main__":
    # unique_channels = data_profiling()
    get_transcripts("../../datasets/standup4ai_es.csv")

