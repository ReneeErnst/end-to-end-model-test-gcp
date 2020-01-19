"""Script to get predictions"""
import argparse
import json
import os

import googleapiclient.discovery as gapi


def parse():
    """
    Arguments needed for making predictions
    :return: arguments
    """
    parser = argparse.ArgumentParser(
        prog='prediction',
        description='Command to run prediction against deployed model'
        )

    parser.add_argument(
        '--credentials',
        required=True,
        help='Path to credentials file locally'
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Name of project model is associated with.'
    )
    parser.add_argument(
        '--model',
        required=True,
        help='Must specify model to make prediction with.'
    )
    parser.add_argument(
        '--version',
        required=False,
        help='Version of model to use for getting prediction.'
    )
    return parser.parse_args()


def predict_json(args: argparse.Namespace):
    """
    Get model predictions
    :param args:
    :return: Model prediction
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.credentials

    service = gapi.build('ml', 'v1')
    name = f'projects/{args.project}/models/{args.model}'

    if args.version is not None:
        name += f'/versions/{args.version}'

    with open('test_prediction.json') as f:
        body = json.load(f)
    response = service.projects().predict(
        name=name,
        body=body
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return print(response)


def main():
    args = parse()
    return predict_json(args)


if __name__ == '__main__':
    main()
