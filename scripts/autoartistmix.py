import gradio as gr
import os
from typing import Dict, List, Tuple
import csv
import modules.scripts as scripts
from modules.processing import (
    StableDiffusionProcessingTxt2Img,
    StableDiffusionProcessingImg2Img,
)

class AutoArtistMix(scripts.Script):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "artist_weights.csv")

    def title(self):
        return "AutoArtistMix"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion('AutoArtistMix', open=False):
            with gr.Row():
                enabled = gr.Checkbox(label='Enabled', value=False)
                method = gr.Radio(label='Method', choices=['Average', 'Min'], value='Min')
                max_tag_weight = gr.Slider(
                    label='Max Tag Weight',
                    minimum=0,
                    maximum=2,
                    step=0.1,
                    value=1
                )
        return enabled, method, max_tag_weight

    def process(self, p: StableDiffusionProcessingTxt2Img | StableDiffusionProcessingImg2Img, enabled: bool, method: str, max_tag_weight: float):
        if not enabled:
            return

        # Convert method to lowercase for consistent comparison
        method = method.lower()

        # Get current prompts and process each one
        new_all_prompts = []
        for prompt in p.all_prompts:
            processed_prompt = self.process_input(
                input_string=prompt,
                max_tag_weight=max_tag_weight,
                weighting_method=method
            )
            new_all_prompts.append(processed_prompt)

        # Update all prompts
        p.all_prompts = new_all_prompts

        # Handle HR prompts if enabled
        if hasattr(p, "all_hr_prompts") and getattr(p, "enable_hr", False):
            new_all_hr_prompts = []
            for hr_prompt in p.all_hr_prompts:
                processed_hr_prompt = self.process_input(
                    input_string=hr_prompt,
                    max_tag_weight=max_tag_weight,
                    weighting_method=method
                )
                new_all_hr_prompts.append(processed_hr_prompt)
            p.all_hr_prompts = new_all_hr_prompts

    def process_input(self, input_string, max_tag_weight=1, weighting_method='min'):
        # Read CSV file and create a dictionary mapping triggers to counts
        with open(AutoArtistMix.csv_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            trigger_counts = {row[0]: float(row[1]) for row in reader}

        # Split input into words while preserving the original order
        words = [word.strip() for word in input_string.split(',')]

        # Separate known and unknown words
        known_words = []
        unknown_words = []

        for i, word in enumerate(words):
            count = trigger_counts.get(word, None)
            if count is not None:
                known_words.append((i, word, count))
            else:
                unknown_words.append(i)

        if len(known_words) == 0:
            # No known words; return all words unchanged
            return ', '.join(words)

        if weighting_method == 'min':
            # Use minimum count method (from processtext5.py)
            min_count = min(count for i, word, count in known_words)

            results = []
            for i, word, count in known_words:
                weight = max_tag_weight / (count / min_count)
                formatted_weight = "{0:.10g}".format(weight)
                results.append(f"({word}:{formatted_weight})")

        elif weighting_method == 'average':
            # Use average count method (from processtext3.py)
            total_sum = sum(count for i, word, count in known_words)
            num_known_words = len(known_words)
            average_per_word = total_sum / num_known_words

            results = []
            for i, word, count in known_words:
                weight = average_per_word / count
                if weight > max_tag_weight:
                    weight = max_tag_weight
                formatted_weight = "{0:.10g}".format(weight)
                results.append(f"({word}:{formatted_weight})")

        # Rebuild the final list maintaining original order
        result_list = words.copy()
        for i, word_info in enumerate(known_words + unknown_words):
            if isinstance(word_info, tuple) and len(word_info) > 1:
                _, word, _ = word_info
                result_list[word_info[0]] = results[i]
            else:
                result_list[word_info] = words[word_info]

        return ', '.join(result_list)