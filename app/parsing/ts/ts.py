from io import BytesIO

from bs4 import BeautifulSoup
from fastapi import UploadFile


class TSFormatParser:

    async def from_ts_to_json(self, file_content: bytes) -> dict:
        final_json = {}

        soup = BeautifulSoup(file_content, "xml")
        ts = soup.find("TS")
        final_json["language"] = ts["language"]
        final_json["sourcelanguage"] = ts["sourcelanguage"]
        final_dict = []
        contexts = soup.find_all("context")

        for context in contexts:
            json = {}
            name = context.find("name").get_text(strip=True)

            messages = context.find_all("message")
            dict = []
            for message in messages:
                source = message.find("source").get_text(strip=True)
                translation = message.find("translation").get_text(strip=True)
                location = message.find("location")
                dict.append(
                    {
                        "source": source,
                        "translation": translation,
                        "filename": location["filename"],
                        "line": location["line"],
                    }
                )
            json[name] = dict
            final_dict.append(json)

        final_json["contexts"] = final_dict

        return final_json

    def normalize_text(self, text: str) -> str:
        return "".join(text.split())

    async def from_list_to_ts(self, lines: list, file_content: bytes, file_name: str):
        soup = BeautifulSoup(file_content, "xml")
        contexts = soup.find_all("context")

        line_dict = {
            (line.group, self.normalize_text(line.meaning)): line.translation
            for line in lines
        }

        for context in contexts:
            name = context.find("name").get_text(strip=True)
            messages = context.find_all("message")

            for message in messages:
                source = message.find("source")
                translation = message.find("translation")

                if not (source and translation):
                    continue

                source_text = source.get_text(strip=False)
                translation_text = translation.get_text(strip=False)

                if not (source_text and translation_text):
                    continue

                key = (name, self.normalize_text(source_text))
                if key in line_dict:
                    new_translation = line_dict[key]

                    if self.normalize_text(translation_text) != self.normalize_text(
                        new_translation
                    ):
                        source.clear()
                        source.append(source_text)

                        translation.clear()
                        translation.append(new_translation)

        modified_xml = soup.prettify().encode("utf-8")
        file_like = BytesIO(modified_xml)

        return UploadFile(file=file_like, filename=file_name)


ts_format_parser = TSFormatParser()
