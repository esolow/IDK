import fnmatch
import os.path
from os import walk, path
import subprocess, sys, json, glob, random
from datetime import date

outputdir = r"C:\Users\eitan\OneDrive\מסמכים\IDK\output"
mode = {'a': 'mode a', 'A': 'mode a', 'b': 'mode b', 'B': 'mode b'}
cipher = "-aes-256-cbc"
pk = 'dlB6WZF6rWoBysnUbnLC0v8N5OunsoEyq/QkrP3cmEY='
json_file = r"C:\Users\eitan\OneDrive\מסמכים\IDK\json_file.JSON"


class Toni:
    def __init__(self, inputdir, mode):
        self.inputdir = inputdir
        self.mode = mode
        self.index = 0
        self.change()

    def change(self):
        if os.path.isfile(self.inputdir):
            if fnmatch.fnmatch(self.inputdir, '*.txt'):
                self.index = 1
                self.process_me(self.inputdir)
        else:
            self.split_folder()

    def get_ref(self):
        try:
            with open(json_file) as configf:
                ConfigData = json.load(configf)
        except IOError:
            ConfigData = {'mode_a': 0, 'mode_b': 0}
        if self.mode == 'mode_a':
            ConfigData['mode_a'] += 1
            with open(json_file, 'w') as num:
                json.dump(ConfigData, num)
            return ConfigData['mode_a']
        else:
            ConfigData['mode_b'] += 1
            with open(json_file, 'w') as num:
                json.dump(ConfigData, num)
                return ConfigData['mode_b']

    def formatting(self):
        current_year = date.today().year
        current_day = date.today().timetuple()[-2]
        if len(str(current_day)) == 1:
            current_day = '00' + str(current_day)
        elif len(str(current_day)) == 2:
            current_day = '0' + str(current_day)

        if os.path.isfile(self.inputdir):
            files_in_folder = 1
        else:
            files_in_folder = len(glob.glob(os.path.join(self.inputdir, "*.txt")))
        output_title = os.path.join(outputdir,
                                    "a{}{}{}{}__{}".format(current_year, current_day, self.mode, self.get_ref(),
                                                           files_in_folder))
        return output_title

    def split_folder(self):
        for (dirpath, _, filenames) in walk(self.inputdir):
            for filename in filenames:
                if fnmatch.fnmatch(self.inputdir, '*.txt'):
                    self.index += 1
                    full_filename = inputdir + '/' + filename
                    self.process_me(full_filename)
            break  # This stops after the first round which is the top folder - remove to process subfolders

    def process_me(self, full_filename):
        just_title = os.path.basename(full_filename)
        output_title = self.formatting()
        IV = "%032x" % (random.getrandbits(128))
        output_file = output_title[:output_title.rfind("_")] + str(self.index) + output_title[
                                                                                      output_title.rfind("_"):]
        try:
            subprocess.check_call(
                ["openssl", "enc", cipher, "-in", full_filename, "-out", output_file, "-k", pk, "-iv", IV])
        except subprocess.CalledProcessError as ex:
            print("Error while calling openSSL", ex)

        with open(output_file, "rb") as rock:
            paper = rock.read()
        with open(output_file, "wb") as scissors:
            scissors.write(just_title.encode() + paper)


if len(sys.argv) > 1:
    inputdir = sys.argv[1]
else:
    inputdir = input("Enter the folder name: ")

mode = input("Enter the mode (A/B): ")
if mode not in mode:
    print("Error: wrong mode, choose a or b")
    sys.exit(1)

Kross = Toni(inputdir, mode)
print("Your file/s were placed in " + outputdir)
