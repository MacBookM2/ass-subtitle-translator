import os
from google.cloud import translate

BASE_DIR = os.getcwd()

class Translator():

    def __init__(self):
        self.service_key = os.path.join(BASE_DIR, 'gcloud', 'service_account.json')

    def translate_text(self, text, source_language_code, target_language_code, project_id="newagent-2efa9"):
        client = translate.TranslationServiceClient.from_service_account_json(self.service_key)
        parent = client.location_path(project_id, "global")

        # Detail on supported types can be found here:
        # https://cloud.google.com/translate/docs/supported-formats
        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",  # mime types: text/plain, text/html
            source_language_code=source_language_code,
            target_language_code=target_language_code,
        )
        # Display the translation for each input text provided
        # print(response.translations)
        for translation in response.translations:
            # print(u"Translated text: {}".format(translation.translated_text))
            return u"{}".format(translation.translated_text)

def get_subtitle_file_lines(filepath):
    lines = []
    file = open(filepath, encoding='utf-8')
    for line in file:
        lines.append(line)
    file.close()
    return lines

def generate_output_file(filepath, lines):
    output_file = open(filepath, "w", encoding="utf-8")
    output_file.writelines(lines)
    output_file.close()

def main():
    translator = Translator()
    translated_subtitle_lines = []
    demo_file_path = os.path.join(BASE_DIR, "data", "PM2019 Episode 29.ass")
    file_lines = get_subtitle_file_lines(demo_file_path)
    header_lines = list(filter(lambda line: "Dialogue:" not in line, file_lines))
    subtitle_lines = list(filter(lambda line: "Dialogue:" in line, file_lines))
    for subtitle_line in subtitle_lines:
        translated_subtitle_lines.append(translator.translate_text(subtitle_line, 'ja', 'en-US'))
    generate_output_file(os.path.join(BASE_DIR, "output", "translated_subtitles.ass"), header_lines + translated_subtitle_lines)

if __name__ == "__main__":
    main()