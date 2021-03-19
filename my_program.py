from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import textract
import sys
import json

def process_file(filepath):
    data = {}
    for page_layout in extract_pages(filepath):
        numbered_elements = dict(enumerate(page_layout))

        element = numbered_elements[0]
        data['name'] = element.get_text().strip()

        element = numbered_elements[2]
        section = element.get_text().strip()
        parts = section.strip().split('|')
        data['address'] = ','.join([parts[0].strip(), parts[2].strip()])
        data['email'] = parts[1].strip()

        # # For debugging
        # for number, element in enumerate(page_layout):
        #     if isinstance(element, LTTextContainer):
        #         print('><'*10)
        #         print(element.get_text())
        #         # print(element.bbox)
        #         try:
        #             print(element.index)
        #         except:
        #             print('Not this ..', element)
        #         print(number)
        #         print('><'*10)
        #         pass
        #     else:
        #         pass
        #         # print('Other type ..')
        #         # print(element.bbox)
        #         # print(numbefilepathr)

    full_content = textract.process(filepath)
    text = str(full_content)
    def find_in_text(left, right):
        # https://stackoverflow.com/a/51456576/3001007
        return text[text.index(left)+len(left):text.index(right)]

    def do_cleanup(raw):
        return raw.replace('_','').replace('\n ','').replace('\n','').replace('  ','').replace('\\n','')

    # Output: 'string'
    education = do_cleanup(find_in_text('Education','Leadership'))
    leadership = do_cleanup(find_in_text('Leadership Experience','Professional Experience'))
    professional_experience = do_cleanup(find_in_text('Professional Experience','Additional Projects'))
    additional_projects = do_cleanup(find_in_text('Additional Projects','Skills & Interests'))
    skills_n_interests = do_cleanup(str(full_content).split('Skills & Interests')[1])

    data['Education'] = education
    data['Leadership Experience'] = leadership
    data['Professional Experience'] = professional_experience
    data['Additional Projects'] = additional_projects
    data['Skills & Interests'] = skills_n_interests

    return data

def write_json(data,json_file_path):
    with open(json_file_path,"w", encoding='utf-8') as jsonfile:
        json.dump(data,jsonfile,ensure_ascii=False,indent=2, sort_keys=False)


if __name__ == "__main__":
    input_pdf = sys.argv[2]
    print(f'Processing {input_pdf}')
    data = process_file(input_pdf)
    print(f'Processing {input_pdf} ... Completed')
    print(data)
    json_file = sys.argv[-1]
    print(f'Writeing {json_file} ... Started')
    write_json(data,json_file)
    print(f'Writeing {json_file} ... Completed')