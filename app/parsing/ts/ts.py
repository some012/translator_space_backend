from bs4 import BeautifulSoup
from starlette.datastructures import UploadFile


class TSFormatParser:

    async def from_ts_to_json(self, file: UploadFile) -> dict:
        final_json = {}

        file_content = await file.read()
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

    def from_json_to_ts(self, json):
        pass


ts_format_parser = TSFormatParser()
