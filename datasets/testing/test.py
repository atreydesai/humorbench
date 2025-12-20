import pandas as pd
import sys

def process_jokes(input_file, output_file):
    # 1. Load the Data
    # Assuming standard CSV format. 
    # If your input uses tabs, change sep=',' to sep='\t'
    try:
        df = pd.read_csv(input_file, encoding='utf-8', sep='\t')
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred reading the file: {e}")
        return

    # Ensure columns act as strings and fill NaNs to prevent errors
    df['Joke'] = df['Joke'].astype(str).fillna('')
    df['Task 1 Label'] = df['Task 1 Label'].astype(str).fillna('')
    df['Task 2 Label'] = df['Task 2 Label'].astype(str).fillna('')

    # 2. Configuration for the "Climax Latch" Algorithm
    jokes = []
    current_joke_rows = []
    climax_reached = False
    prev_video_id = None
    
    # Labels that indicate a joke has reached its peak
    climax_labels = {'Punchline', 'Wrap-up', 'Callback', 'Meta-humor'}
    # Label that indicates a clean start of a NEW joke
    start_label = 'Establishing context'

    # Helper function to finalize a specific joke block
    def finalize_joke_block(rows):
        if not rows:
            return None
        
        joke_df = pd.DataFrame(rows)
        
        # A. Join Text with literal "\n" string (escaped newline)
        # We use "\\n" so it writes the characters \ and n, not an actual line break.
        joined_text = "\\n".join(joke_df['Joke'].tolist())
        joined_task2 = "\\n".join(joke_df['Task 2 Label'].tolist())
        
        # B. Logic: "Punchline Inheritance" for Task 1 Label
        # We prefer the Task 1 label associated with the 'Punchline' row.
        punchline_rows = joke_df[joke_df['Task 2 Label'] == 'Punchline']
        
        if not punchline_rows.empty:
            # Use the label from the first punchline found in this block
            assigned_task1 = punchline_rows.iloc[0]['Task 1 Label']
        else:
            # Fallback: Use the most frequent Task 1 label in the block
            # If the block is empty or weird, handle gracefully
            try:
                assigned_task1 = joke_df['Task 1 Label'].mode()[0]
            except IndexError:
                assigned_task1 = ""

        return {
            "Joke": joined_text,
            "Task 1 Label": assigned_task1,
            "Task 2 Label": joined_task2
        }

    # 3. Iterate through rows
    print("Processing jokes...")
    for index, row in df.iterrows():
        video_id = row['Video #']
        label = row['Task 2 Label']

        # --- SPLIT LOGIC ---
        # Split if: 
        # 1. Video ID changes
        # 2. OR We encounter "Establishing context" AND the previous joke hit a climax
        is_new_video = (prev_video_id is not None and video_id != prev_video_id)
        is_new_bit = (label == start_label and climax_reached)

        if is_new_video or is_new_bit:
            processed_joke = finalize_joke_block(current_joke_rows)
            if processed_joke:
                jokes.append(processed_joke)
            
            # Reset state for next joke
            current_joke_rows = []
            climax_reached = False

        # --- BUILD LOGIC ---
        current_joke_rows.append(row)
        prev_video_id = video_id

        # Update Climax Flag
        if label in climax_labels:
            climax_reached = True

    # 4. Append the final buffer
    final_joke = finalize_joke_block(current_joke_rows)
    if final_joke:
        jokes.append(final_joke)

    # 5. Export to TSV
    output_df = pd.DataFrame(jokes)
    
    # Reorder columns
    output_df = output_df[['Joke', 'Task 1 Label', 'Task 2 Label']]
    
    # Write to TSV. 
    # escapechar is not strictly necessary for \\n but good practice if text contains tabs.
    output_df.to_csv(output_file, sep='\t', index=False, encoding='utf-8')
    
    print(f"Success! Processed {len(jokes)} jokes.")
    print(f"Output saved to: {output_file}")

# --- EXECUTION ---
if __name__ == "__main__":
    input_csv = 'filename.csv'         # Input file name
    output_tsv = 'processed_jokes.tsv' # Output file name
    
    process_jokes(input_csv, output_tsv)