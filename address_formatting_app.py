from flask import Flask, request, jsonify
from waitress import serve
import os
import json
import pandas as pd
import numpy as np
import regex as re

# dictionary of  non-essential acronyms
acr = {'po': 1, 'ps': 1, 'p.o.': 1, 'p.s.': 1, 'g.p.o.': 1, 'gpo': 1, 'a.p.o.': 1, 'apo': 1, 'fpo': 1, 'f.p.o.': 1,
       'h.p.o.': 1, 'hpo': 1, 'policestation': 1, 'postoffice': 1, 'city': 1, 'town': 1, 'village': 1, 'tehsil': 1}
ind= ['nearby','nearto','oppositeto','opposite','oppto','opp','behind','near','beside','sideof','eastof','westof',
      'northof','southof','nextto','rightof','leftof']
# Boolean function to check if characters are in english
def isEnglish(s):
    #Simple trick, if string decodes to ascii, it is pure english, otherwise it is of some other language
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except:
        return False
    else:
        return True

#Transliteration of a string from detect-language to english. Here we have used translate to avoid confusion
#NOTE : Only transliteration is taking place
def translate(string):
    if (isEnglish(string) == False):
        language_id = gs.detect(string)
        translated = gs.translate(string,language_id)
        return translated
    return string

# function for formatting address file
#inputs json outputs json
def format(json_file):
    #Read dataframe using pandas
    df = pd.io.json.read_json(json_file, orient="records",encoding='utf-8')
    colmn = list(df.columns)
    df.replace({'NULL': ''}, inplace=True)
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    #converting all data to lowercase for simplicity
    # for columns in df.columns:
    #     df[columns] = df[columns].str.lower()


    #We are using variable/dummy strings for comparision, no operations on original data except if it needs to be removed
    #running a row-wise loop through the dataframe
    for index, row in df.iterrows():
        #parent string->string that is used to compare with other strings for duplication

        #1. for district as parent string
        # removing the word city from the string for better comparisons
        if row['district'] != None:
            # base string ->the string of a column that will be compared with all other columns
            base_string = re.sub(" city", '', translate(row['district']).strip()).strip()

            # now, we have the improved string, we will compare it with column strings
            # comparasion of district will only take place with sub-district,vtc,locality and landmark
            if 'sub-district' in df:
                if row['sub-district'] != None:
                    string=translate(row['sub_district'])
                    if len(string.split(","))>1:
                        df.at[index, 'sub-district'] = remove_dup(base_string, string)

                    if check_dup(string, base_string) == 1:
                        df.at[index, 'sub-district'] = None

            if row['vtc'] != None:
                string = translate(row['vtc'])
                if len(string.split(",")) > 1:
                    df.at[index, 'vtc'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'vtc'] = None

            if row['locality'] != None:
                string = translate(row['locality'])
                if len(string.split(",")) > 1:
                    df.at[index, 'locality'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'locality'] = None

        #2. for sub-district as parent string
        if 'sub-district' in df:
            if row['sub-district'] != None:
                base_string = re.sub(" city", '', translate(row['sub-district']).strip()).strip()

                #sub-district is compared with vtc,locality,landmark,street
                if row['vtc'] != None:
                    string = translate(row['vtc'])
                    if len(string.split(",")) > 1:
                        df.at[index, 'vtc'] = remove_dup(base_string, string)

                    if check_dup(string, base_string) == 1:
                        df.at[index, 'vtc'] = None

                if row['locality'] != None:
                    string = translate(row['locality'])
                    if len(string.split(",")) > 1:
                        df.at[index, 'locality'] = remove_dup(base_string, string)

                    if check_dup(string, base_string) == 1:
                        df.at[index, 'locality'] = None

                if row['landmark'] != None:
                    string = translate(row['landmark'])
                    if len(string.split(",")) > 1:
                        df.at[index, 'landmark'] = remove_dup(base_string, string)

                    if check_dup(string, base_string) == 1:
                        df.at[index, 'landmark'] = None

                if row['street'] != None:
                    string = translate(row['street'])
                    if len(string.split(",")) > 1:
                        df.at[index, 'street'] = remove_dup(base_string, string)

                    if check_dup(string, base_string) == 1:
                        df.at[index, 'street'] = None

        #3. for vtc as parent string
        if row['vtc'] != None:
            base_string = re.sub(" city", '', translate(row['vtc']).strip()).strip()

            #vtc will be compared with locality, landmark, street, building
            if row['locality'] != None:
                string = translate(row['locality'])
                if len(string.split(",")) > 1:
                    df.at[index, 'locality'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'locality'] = None

            if row['landmark'] != None:
                string = translate(row['landmark'])
                if len(string.split(",")) > 1:
                    df.at[index, 'landmark'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'landmark'] = None

            if row['street'] != None:
                string = translate(row['street'])
                if len(string.split(",")) > 1:
                    df.at[index, 'street'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'street'] = None

            if row['building'] != None:
                string = translate(row['building'])
                if len(string.split(",")) > 1:
                    df.at[index, 'building'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'building'] = None

        #4. for Locality as parent string
        if row['locality'] != None:
            base_string = translate(row['locality']).strip()

            #locality is compared with street, landmark and building
            if row['street'] != None:
                string = translate(row['street'])
                if len(string.split(",")) > 1:
                    df.at[index, 'street'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'street'] = None

            if row['landmark'] != None:
                string = translate(row['landmark'])
                if len(string.split(",")) > 1:
                    df.at[index, 'landmark'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'landmark'] = None

            if row['building'] != None:
                string = translate(row['building'])
                if len(string.split(",")) > 1:
                    df.at[index, 'building'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'building'] = None

        #5. for landmark as parent string
        if row['landmark'] != None:
            base_string = translate(row['landmark']).strip()

            # additional query for landmark, removes commas and other special characters
            #Also removes indicator words like next to, beside, north of, south of, etc. full list above in indicator.
            base_string = ''.join(e for e in base_string if e.isalnum())
            for indicator in ind:
                base_string = re.sub(indicator, '', base_string)

            #landmark is compared with street and building
            if row['street'] != None:
                string = translate(row['street'])
                if len(string.split(",")) > 1:
                    df.at[index, 'street'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'street'] = None

            if row['building'] != None:
                string = translate(row['building'])
                if len(string.split(",")) > 1:
                    df.at[index, 'building'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'building'] = None


        #6. for street as parent string
        if row['street'] != None:
            base_string = translate(row['street']).strip()

            #street is compared with building
            if row['building'] != None:
                string = translate(row['building'])
                if len(string.split(",")) > 1:
                    df.at[index, 'building'] = remove_dup(base_string, string)

                if check_dup(string, base_string) == 1:
                    df.at[index, 'building'] = None

    # return dataframe

    return df

#Function to remove a base_string from another string
def remove_dup(base_string,string):
    strings= string.split(",")
    for a in strings:
        b=a.strip()
        strings[strings.index(a)]= b
    if base_string in strings:
        return re.sub(base_string,'',string).strip(',')
    return string

#function to check for duplication
def check_dup(string, base_string):
    #remove special characters
    base_string = ''.join(e for e in base_string if e.isalnum())
    base_string = ''.join(base_string.split())
    string = ''.join(e for e in string if e.isalnum())
    # removing spaces for better comparasion
    string = ''.join(string.split())
    # regex to remove the base_string part to see remaining part
    new_string = re.sub(base_string, '', string).strip()
    # new_string is the product of substitution. if it is not equal to the original string,
    # it means base string was present in the current string
    if new_string != string:
        # it means the base_string is present in this string
        # in this case, we run a non essential check
        ne = check_non_essential(new_string.strip())
        # ne = 1 means the remaining string is non essential and the total address is a duplication
        if ne == 1:
            return 1
        # ne=0 means the remaining part is essential and cannot be removed
        else:
            return 0
    return 0


def check_non_essential(string):
    # any two letter word or lesser is non essential. An empty string is less than 2 letters too,
    # an empty string is also non essential
    if len(string) < 3:  # and string.isupper():
        return 1
    # run it in a dict of saved non-essential acronyms and if it exists, return 1
    elif string in acr:
        return 1
    return 0


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/output', methods=['POST'])
def json_output():
    json_file = request.get_json()
    output = format(json_file)
    return jsonify(output.to_json(force_ascii=False,orient="records"))


if (__name__ == "__main__"):
    app.run(host='0.0.0.0',debug=True)
    serve(app, host='0.0.0.0', port=5000, url_scheme='https')
# @app.route('/success', methods = ['POST'])
# def success():
#     global output_file
#     if request.method == 'POST':
#         f = request.files['file']
#         json_file=f.filename
#         output_file=format(json_file)
#         # f.save(f.filename)
#         # output_file.save(output_file)
#         return render_template("success.html", name = f.filename)
#
# @app.route('/download')
# def download_file():
#     output=output_file
#     return output
#     return (send_file(output,attachment_filename="formatted_address.json", as_attachment = True))
#     # return 'hello google app engine!'
#
# @app.route('/view')
# def view_file():
#     # p= M
# #     data_file = open('D:\flask\output_file.csv', 'w', newline='')
# # csv_writer = csv.writer(data_file)
#
#     return send_file(output_file, as_attachment = True)
