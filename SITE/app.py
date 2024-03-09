from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

class PositionCalculatorApp:
    def __init__(self):
        self.load_datasets()

    def load_datasets(self):
        try:
            self.kanji_df = pd.read_excel("jpwords.xlsx")
            self.hanzi_df = pd.read_excel("cnwords.xlsx")
        except FileNotFoundError:
            print("One or both datasets not found.")
            raise SystemExit

    def calculate_position_percentages(self, words_df, character_input):
        total_words = len(words_df)
        total_first = words_df.apply(lambda row: 1 if row.str.contains(character_input).values[0] else 0, axis=1).sum()
        total_last = words_df.apply(lambda row: 1 if row.str.endswith(character_input).values[0] else 0, axis=1).sum()
        total_middle = total_words - total_first - total_last

        first_percent = (total_first / total_words) * 100
        middle_percent = (total_middle / total_words) * 100
        last_percent = (total_last / total_words) * 100

        middle_percent = max(middle_percent, 0)

        result_message = f"Position of {character_input} in words:\n\n"
        result_message += f"FIRST={first_percent:.2f}%, MIDDLE={middle_percent:.2f}%, LAST={last_percent:.2f}%"

        return result_message

position_calculator = PositionCalculatorApp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    character_input = request.form.get('character_input')
    result_message = ""

    if not character_input:
        result_message = "Please enter a character."
    else:
        try:
            kanji_words = position_calculator.kanji_df[position_calculator.kanji_df['words'].str.contains(character_input, na=False, case=False)]
            hanzi_words = position_calculator.hanzi_df[position_calculator.hanzi_df['word'].str.contains(character_input, na=False, case=False)]

            if kanji_words.empty and hanzi_words.empty:
                result_message = f"No words found with {character_input}."
            else:
                result_message += "Kanji Positions:\n"
                if not kanji_words.empty:
                    result_message += position_calculator.calculate_position_percentages(kanji_words, character_input)

                result_message += "\n\nHanzi Positions:\n"
                if not hanzi_words.empty:
                    result_message += position_calculator.calculate_position_percentages(hanzi_words, character_input)

        except Exception as e:
            result_message = f"An error occurred: {str(e)}"

    return jsonify({'result_message': result_message})

if __name__ == "__main__":
    app.run(debug=True)
