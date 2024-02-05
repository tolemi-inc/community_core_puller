from community_core_scraper import CommunityCoreScraper
from config import Config
from config_error import ConfigError
import json
import traceback
import argparse
import logging

parser = argparse.ArgumentParser(description="Process inputs for community core pulls")

parser.add_argument("--config", type=str, help="Path to config file")

args = parser.parse_args()

logging.getLogger().setLevel(logging.INFO)


def run(config):
    communityCoreScraper = CommunityCoreScraper(
        config.community_core_username,
        config.community_core_password,
        "https://app.communitycore.com",
    )
    access_token = communityCoreScraper.get_access_token()
    account_id = communityCoreScraper.get_account_id(access_token)
    jurisdiction_id = communityCoreScraper.get_jurisdiction_id(access_token, account_id)
    report_id = communityCoreScraper.get_report_id(
        access_token, config.dataset, account_id
    )
    communityCoreScraper.get_report_filters(
        access_token,
        account_id,
        jurisdiction_id,
        report_id,
        config.start_date,
        config.end_date,
    )

    headers_dict = communityCoreScraper.generate_report(
        access_token,
        account_id,
        jurisdiction_id,
        report_id,
        config.dataset,
        config.start_date,
        config.end_date,
    )

    output_object = {
        "status": "ok",
        "file_name": f"community_core_puller/data/{config.dataset.lower().replace(' ', '_')}.csv",
        "columns": headers_dict,
    }
    print("DONE", json.dumps(output_object))


def fail(error):
    result = {
        "status": "error",
        "error": """{}
         {}""".format(
            str(error), traceback.format_exc()
        ),
    }

    output_json = json.dumps(result)
    print("DONE", output_json)


def load_config(file_path):
    raw_config = load_json(file_path)

    sub_config = raw_config.get("config", {})

    dataset = sub_config.get("dataset", None)
    start_date = sub_config.get("start_date", None)
    end_date = sub_config.get("end_date", None)

    community_core_username = raw_config.get("env", None).get(
        "community_core_username", None
    )
    community_core_password = raw_config.get("env", None).get(
        "community_core_password", None
    )

    return Config(
        dataset, start_date, end_date, community_core_username, community_core_password
    )


def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        True
        print(f"File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        True
        print(f"JSON decoding error: {e}")
    except Exception as e:
        True
        print(f"An error occurred: {e}")


# Main Program
if __name__ == "__main__":
    try:
        config = load_config(args.config)
        run(config)
    except ConfigError as e:
        fail(e)
