import json
import os
import time

from openai import OpenAI
from rdf_converter import build_init_struct
# Replace 'YOUR_API_KEY' (as an ENV variable) with your actual GPT-3 API key
from pathlib import Path
class GptCodeConverter():

    MODEL_CHOICE_1 = "gpt-3.5-turbo-1106"
    MODEL_CHOICE_2 = "code-davinci-002",
    MODEL_CHOICE_3 = "gpt-3.5-turbo",
    # max_tokens=500,  # Adjust as needed
    # temperature=0.7  # Adjust the temperature for creativity

    MAX_TOKENS = 10000  # Maximum number of tokens that can be used with the OPENAI model (model dependant)

    def __init__(self, language="Java", model=MODEL_CHOICE_1):
        self.client = OpenAI(
                                # defaults to os.environ.get("OPENAI_API_KEY")
                                # api_key=api_key,
                            )
        self.model_name = model
        self.language = language
        self.results = ''
        self.system_instructions = """You will be an expert of the Common Information Model (CIM) prepared by the Technical Committee 57 of the IEC."""
    def create_rdf(self,  instructions):
        """
        Convert the given code snippet using GPT-3.
        """
        # Call the GPT-3 API to generate the converted code
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self.system_instructions
                    },
                    {
                        "role": "user",
                        "content": instructions
                    }

                ],
                model=self.model_name,

            )

            # Extract and return the generated code from the response

            results = chat_completion.choices[0].message.content
        except Exception as e:
            print(e)
            results = ''
        self.results = results


if __name__ == "__main__":
    directory_path = f"{os.path.expanduser('~')}/Documents/Git/GitHub/GOSS-GridAPPS-D-PYTHON/gov_pnnl_goss/cimhub/CIM/"
    current_time = int(time.time())
    cim_types = "CIMtypes.txt"
    converter = GptCodeConverter("RDF")
    rdf_failcount = 0
    rdf_fail_files = []
    json_failcount = 0
    json_fail_files = []
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    with open(directory_path + cim_types, 'r') as f:
        lines = f.readlines()
    for line in lines:
        cim_type = line.strip()
        instructions = f"Show me an example of a {cim_type} rdf model, in parsable turtle format. Do not include the xsd schema."
        print(f"Building an example rdf file for {cim_type}")
        converter.create_rdf(instructions)
        results = converter.results
        # clean up the results here
        resultant_lines = results.split('\n')
        clean_lines = []
        enclosure = False
        for r in resultant_lines:
            if enclosure and r.find("```") == 0:
                enclosure = False
                break
            if enclosure:
                clean_lines.append(r)
            if not enclosure and r.find("```") == 0:
                enclosure = True
        clean_results = '\n'.join(clean_lines)
        rdf_directory_path = f"{directory_path}rdf/"
        Path(rdf_directory_path).mkdir(parents=True, exist_ok=True)
        output_filename = f"{rdf_directory_path}{cim_type}{current_time}.rdf"
        try:
            with open(output_filename, 'w') as f2:
                f2.write(clean_results)
        except UnicodeEncodeError as e:
            rdf_failcount += 1
            print(e)

        try:
            json_directory_path = f"{directory_path}json/"
            Path(json_directory_path).mkdir(parents=True, exist_ok=True)
            output_filename = f"{json_directory_path}{cim_type}{current_time}.json"
            struct_dict = build_init_struct(cim_type, clean_results)
            json_text = json.dumps(struct_dict, indent=2)
            with open(output_filename, 'w') as f2:
                f2.write(json_text)
            pjson = f"@startjson\n{json_text}\n@endjson\n"
            output_filename = f"{directory_path}puml/{cim_type}{current_time}.puml"
            with open(output_filename, 'w') as f2:
                f2.write(pjson)
        except Exception as e:
            print(f"{cim_type} error: {e}")
            json_failcount += 1
            json_fail_files.append(cim_type)

    print(f"RDF fails: {rdf_failcount}, JSON fails: {json_failcount}")
    print(json_fail_files)