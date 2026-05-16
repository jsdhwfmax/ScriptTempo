import os
import re
import unittest

# Core Functions

def read_script(filepath):
    """Read text file with error handling (Week 8 & 9)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"[Error] The file '{filepath}' is empty.")
                return None
            return content
    except FileNotFoundError:
        print(f"[Error] File '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"[Error] Unexpected error reading file: {e}")
        return None

def count_syllables(word):
    """Estimate syllables in a word for difficulty check."""
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def split_for_breath(sentence, max_words=15):
    """Recursively split long sentences into natural breath groups (Week 11)."""
    words = sentence.split()
    if len(words) <= max_words:
        return [sentence]
        
    split_points = [", ", " but ", " and ", " however ", " which ", " that "]
    
    for point in split_points:
        if point in sentence:
            parts = sentence.split(point, 1) 
            
            # If one half of the cut-out is empty, it means the cut-out point is at the edge of the sentence, so skip it directly.
            if len(parts[0].strip()) == 0 or len(parts[1].strip()) == 0:
                continue
                
            left = parts[0] + ("," if point == ", " else "")
            right = (point.strip() + " " if point != ", " else "") + parts[1]
            
            return split_for_breath(left.strip(), max_words) + split_for_breath(right.strip(), max_words)
    
    left = " ".join(words[:max_words]) + "..."
    right = "..." + " ".join(words[max_words:])
    return [left] + split_for_breath(right, max_words)

def analyze_script(text):
    """Analyze text and build a 2D array of paragraph metadata (Week 12)."""
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    data = []
    
    for para in paragraphs:
        words = re.findall(r'\b\w+\b', para)
        word_count = len(words)
        if word_count == 0:
            continue
            
        # Assuming 130 words per minute
        time_sec = round(word_count / 130 * 60) 
        
        complex_words = []
        for w in words:
            if len(w) > 9 or count_syllables(w) >= 4:
                if w not in complex_words:
                    complex_words.append(w)
                    
        # Multi-dimensional array implementation
        data.append([para, word_count, time_sec, complex_words])
        
    return data

def generate_cue_sheet(data, output_path):
    """Format and export the 2D array data to a text report (Week 8)."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("ScriptTempo: Academic Presentation Cue Sheet\n")
            f.write("="*60 + "\n\n")
            
            total_words = 0
            total_time = 0
            
            for i, para_data in enumerate(data, 1):
                text, word_count, time_sec, complex_words = para_data
                total_words += word_count
                total_time += time_sec
                
                f.write(f"--- [Paragraph {i}] | Time: ~{time_sec}s | Words: {word_count} ---\n")
                
                breath_groups = split_for_breath(text, 15)
                for group in breath_groups:
                    f.write(f"  > {group}\n")
                    
                if complex_words:
                    f.write("\n  [!] Pronunciation Alert (Practice these):\n")
                    f.write(f"      {', '.join(complex_words)}\n")
                f.write("\n\n")
                
            f.write("="*60 + "\n")
            f.write("OVERALL SUMMARY:\n")
            f.write(f"- Total Words: {total_words}\n")
            f.write(f"- Estimated Time: {total_time // 60} min {total_time % 60} sec\n")
            f.write("="*60 + "\n")
            
        print(f"[Success] Cue sheet saved to: {output_path}")
    except Exception as e:
        print(f"[Error] Failed to write file: {e}")

# Unit Testing (Week 10)

class TestScriptTempo(unittest.TestCase):
    """Automated tests for core algorithms."""
    
    def test_split_for_breath(self):
        long_sentence = "This is a very long sentence but we must also acknowledge the incredible opportunities."
        result = split_for_breath(long_sentence, max_words=10)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 1)
        
    def test_analyze_script_empty(self):
        result = analyze_script("   \n  ")
        self.assertEqual(result, [])


def main():
    print("=== ScriptTempo Execution Started ===")
    input_file = input('Location and name of txt')
    output_file = "output.txt"
    
    # Auto-generate a test file if missing
    if not os.path.exists(input_file):
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("Hello everyone, and thank you for joining me today.\n\n")
            f.write("Today, we are going to discuss the intricate and fascinating world of artificial intelligence and its unprecedented impact on our daily lives.\n")
    
    print(f"[Info] Reading '{input_file}'...")
    raw_text = read_script(input_file)
    
    if raw_text:
        print("[Info] Analyzing script structure and pacing...")
        processed_data = analyze_script(raw_text)
        
        print("[Info] Generating cue sheet...")
        generate_cue_sheet(processed_data, output_file)
        
    print("\n=== Running Unit Tests ===")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

if __name__ == "__main__":
    main()