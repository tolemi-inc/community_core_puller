import logging
import requests
import json
import io
import csv


class CommunityCoreScraper:
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url

    def make_api_call(self, method, url, headers, payload=None):
        try:
            if payload:
                response = requests.request(method, url, headers=headers, data=payload)
            else:
                response = requests.request(method, url, headers=headers)

            logging.info(
                "Response: " + str(response.status_code) + ", " + response.reason
            )

            if response.status_code == 200:
                return response

            else:
                logging.error("Api request returned a non-200 response")
                logging.error(response.json())
                raise Exception("Error making api request")

        except:
            raise Exception("Error making api request")

    def get_access_token(self):
        url = f"{self.base_url}/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        response = self.make_api_call("POST", url, headers, payload)
        logging.info("Successfully retrieved access token for Community Core")

        return response.json()["access_token"]

    def get_account_id(self, token):
        url = f"{self.base_url}/api/v1/account"
        headers = {"Authorization": f"Bearer {token}"}

        response = self.make_api_call("GET", url, headers)
        logging.info(f"Successfully found id for the city in Community Core")

        return response.json()["primaryOfficeId"]

    def get_jurisdiction_id(self, token, account_id):
        url = f"{self.base_url}/api/v1/office/{account_id}/jurisdiction"
        headers = {"Authorization": f"Bearer {token}"}

        response = self.make_api_call("GET", url, headers)
        logging.info(
            "Successfully found jurisdiction id for the city in Community Core"
        )

        return response.json()["Value"][0]["id"]

    def get_report_id(self, token, report_name, account_id):
        url = f"{self.base_url}/api/v1/office/{account_id}/report"
        headers = {"Authorization": f"Bearer {token}"}

        response = self.make_api_call("GET", url, headers)
        logging.info(f"Successfully found id for the {report_name} dataset")

        report_id = next(
            (
                category["id"]
                for category in response.json()["Value"]
                if category["name"].strip() == report_name
            ),
            None,
        )

        return report_id

    def get_report_filters(
        self, token, account_id, jurisdiction_id, report_id, start_date, end_date
    ):
        url = f"{self.base_url}/api/v1/office/{account_id}/report/{report_id}/filter-criteria"
        headers = {"Authorization": f"Bearer {token}"}

        response = self.make_api_call("GET", url, headers)

        filter_criteria_json = {"filterCriteria": [], "formatId": 2, "id": report_id}

        for filter in response.json():
            if filter["filterCriteriaId"] == 1:
                value = {"startDate": start_date, "endDate": end_date}
            if filter["filterCriteriaId"] == 3:
                value = {"jurisdictionId": jurisdiction_id}
            if filter["filterCriteriaId"] == 9:
                value = {"violationHistoryTypeIds": [1, 2, 3, 4, 5, 6, 7, 9]}

            filter_criteria_json["filterCriteria"].append(
                {
                    "filterCriteriaId": filter["filterCriteriaId"],
                    "value": json.dumps(value),
                }
            )

        return filter_criteria_json

    def create_csv(self, data, path):
        string_io = io.StringIO(data)
        csv_reader = csv.reader(string_io)
        headers = next(csv_reader)
        dict_data = [dict(zip(headers, row)) for row in csv_reader]

        with open(f"{path}", "w", newline="") as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(dict_data)

        return headers

    def generate_report(
        self,
        token,
        account_id,
        jurisdiction_id,
        dataset_id,
        start_date,
        end_date,
        dataset
    ):
        url = f"{self.base_url}/api/v1/office/{account_id}/report/{dataset_id}/run"
        headers = {
            "Authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

        payload = self.get_report_filters(
            token, account_id, jurisdiction_id, dataset_id, start_date, end_date
        )

        response = self.make_api_call("PUT", url, headers, json.dumps(payload))

        csv_file_path = dataset
        headers = self.create_csv(response.text, csv_file_path)

        headers_dict = [{"name": header, "type": "VARCHAR"} for header in headers]
        return headers_dict
