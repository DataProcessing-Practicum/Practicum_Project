###############################
#
# Authored by Grady Jenkins
#
# Modified by Louis Discenza
#
###############################
import time
from ftplib import FTP
from datetime import datetime, timedelta

class FTPDownloader: 
    """ Downloads reports from USDA FTP site. 
        Takes the updated reports and looks for them on the MARS API. 
        Change working directory to /mnreports/.
    """
    def __init__(self):
        self.updated_recent = []
        url = 'ftp.ams.usda.gov'
        self.ftp = FTP(url)
        self.ftp.login()      

    def login(self, username=None, password=None):
        """Log in to ftp server.
        Args:
            username (str): username to login with
            password (str): password to login with
        """
        self.ftp.login()

    def change_directory(self, curr_dir):
        """
        Args:
            curr_dir (str): path of directory
            Change working directory on FTP server
        """
        self.ftp.cwd(curr_dir)

    def get_directory_list(self):
        """
            List items in directory
        """
        lines = []
        self.ftp.retrlines('LIST', lines.append)
        return lines

    def monitor(self, interval=15):
        """
            Loops infinitely, pausing at a spceified interval
            Issues a query each iteration until interrupted
        """
        self.old_files = {}
        while True:
            try:
                self.query()
                time.sleep(interval)
                print("scanning")
            except KeyboardInterrupt:
                self.close()
            except:
                pass

    def query(self):
        """
            Get the reports from the directory
            Check which reports are new and process them
        """
        reports = self.get_relevant_reports()
        new_files = self.construct_report_dict(reports)
        updated, new_reports = self.is_updated(new_files, self.old_files)
        if len(self.old_files) != 0 and updated:
            self.process_changes(new_reports)
        self.old_files = new_files

    def is_updated(self, new_files, old_files):
        """
        Args:
            new_files, old_files (dict): Dictionary of files with format: {slug_name: date}
            Checks to see if the value (date) changed for each key
            Returns a dictionary of all reports that updated
        """
        updated = {}
        for key, value in new_files.items():
            if key in old_files and old_files[key] != value:
                updated[key] = value
        return len(updated) > 0, updated

    def get_relevant_reports(self):
        """
            Compiles a list of all the relevant reports and formats them
        """
        split_reports = [x.split(' ') for x in self.get_directory_list()]
        formatted_reps = [list(filter(None, line)) for line in split_reports]
        recent_reports = [line for line in formatted_reps if self.is_report_recent(line)]
        return recent_reports

    def construct_report_dict(self, reports):
        """
        Args:
            reports (list): formatted list of relevant reports
            Creates a dictionary from list by assembling report names as keys
            and formatted dates as values
        """
        dictionary = {}
        for item in reports:
            date = datetime.strptime(item[0]+' '+item[1], '%m-%d-%y %I:%M%p')
            name = item[len(item)-1]
            dictionary[name] = date
        return dictionary

    def is_report_recent(self, line):
        """
        Args:
            line (list): single item from list of reports
            Checks report date against current date to determine if it recent
            Return True if recent and None otherwise. False on Exception.
        """
        try:
            rep_date = datetime.strptime(line[0]+' '+line[1], '%m-%d-%y %I:%M%p')
            if rep_date > (datetime.now() - timedelta(days=365)):
                return True
        except Exception as e:
            print(e)
            return False

    def process_changes(self, updated):
        """
        Args:
            updated (dict): Dictionary of updated items with format: {slug_name: date}
        """
        for key in updated.keys():
            try:
                with open(r'.\downloaded_reports\%s' % key, 'wb') as f:
                    self.ftp.retrbinary('RETR %s'% key, f.write)
                    slug_name = key.split('.')[0]
                    if(slug_name != 'mnindex'):
                        print(slug_name)                        
            except Exception as e:
                print(e)

    def close(self):
        """
            Close FTP connection
        """
        try:
            self.ftp.quit()
        except Exception as e:
            print(e)
            self.ftp.close()

if __name__ == '__main__':
    working_dir = 'mnreports'
    dwn = FTPDownloader()
    dwn.change_directory(working_dir)
    dwn.monitor()
    dwn.close()