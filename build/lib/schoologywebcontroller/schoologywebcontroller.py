from selenium.webdriver.common.keys import Keys

from basewebcontroller import BaseWebController
from basewebcontroller.errors import AuthenticationError

import dateutil.parser
import re


class SchoologyController(BaseWebController):

    def login(self, username: str, password: str, school: str, school_id: str):
        """
        Logs into Schoology.
        :param username:
        :param password:
        :param school:
        :param school_id: The school id number.
        :return:
        """
        self.driver.get('https://app.schoology.com/login')
        self.driver.find_element_by_id('edit-mail').send_keys(username)
        self.driver.find_element_by_id('edit-pass').send_keys(password)
        self.driver.find_element_by_id('edit-school').send_keys(school)

        self.driver.execute_script("""document.getElementsByName('school_nid')[0].type = 'text';""")
        self.driver.find_element_by_id('edit-school-nid').send_keys(school_id)

        self.driver.find_element_by_id('edit-submit').click()

    def export_nids_to_csv(self, school: str, outfile_path: str):
        """
        Convenience function to export the school information.
        Returns more than one result so you can enter partial names.
        :param school: The partial or full name of the school whose ID you're looking for.
        :param outfile_path: The file to be created, must end in .csv.
        """
        if not outfile_path.endswith(".csv"):
            raise AttributeError("outfile_path must end with .csv.")

        import csv  # This function is for convenience, it will not be used often and we don't need to import csv for the rest of the module.
        import json
        import re

        school = school.replace(" ", "%20")
        self.driver.get(f'https://app.schoology.com/register/ajax/school?jq={school}&limit=40')

        data = json.loads(re.findall(r'(?<=white-space: pre-wrap;\">)[\[{\"A-Za-z0-9:, _.\\\/?=}\-()\]]+(?=</pre)', self.driver.page_source)[0])

        with open(outfile_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            header = True
            for school in data:
                if header:
                    csv_writer.writerow(school.keys())
                    header = False
                csv_writer.writerow(school.values())

    def request_usage(self, start_date: str, end_date: str):
        """Requests a usage report to be emailed to you."""
        start_date = dateutil.parser.parse(start_date).strftime("%m/%d/%Y")
        end_date = dateutil.parser.parse(end_date).strftime("%m/%d/%Y")

        self.driver.get('https://app.schoology.com/school_analytics')
        self.driver.find_element_by_xpath("//*[text()='Actions']").click()
        self.driver.find_element_by_xpath("//*[text()='Export Report']").click()

        start_field = self.driver.find_element_by_xpath("//input[@type='DATE_START']")
        start_field.send_keys(Keys.CONTROL, 'A', Keys.BACKSPACE)
        start_field.send_keys(start_date)

        end_field = self.driver.find_element_by_xpath("//input[@type='DATE_END']")
        end_field.send_keys(Keys.CONTROL, 'A', Keys.BACKSPACE)
        end_field.send_keys(end_date)

        self.driver.find_element_by_xpath("//*[text()='Next']").click()
        self.driver.find_element_by_xpath("//*[text()='Export Report']").click()

    def download_usage(self, link: str):
        """Downloads the usage report from the emailed link. If using a new browser, you may need to re-authenticate."""
        self.driver.get(link)
        link = re.sub(r"(?<=https://)[A-Za-z0-9]+(?=.schoology)", "app", link)[:-16]
        self.driver.get(link)