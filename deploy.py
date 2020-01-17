"""Run the gcloud command for AI Platform Job"""
import argparse
import subprocess
import textwrap


def parse():
    parser = argparse.ArgumentParser(
        prog='deploy',
        description=textwrap.dedent(
            """
            Command to run AI Platform jobs for training and prediction 
            via gcloud
            """
        )
    )
    sub_parsers = parser.add_subparsers(dest='action')

    train_parser = sub_parsers.add_parser('train')
    train_parser.add_argument(
        '--bucket',
        required=True,
        help='Specify the storage bucket for staging package and model files'
    )
    train_parser.add_argument(
        '--name',
        required=True,
        help='Name of the job for AI Platform Jobs'
    )

    predict_parser = sub_parsers.add_parser('predict')
    predict_parser.add_argument()

    return parser.parse_args()


def deploy_trainer(args: argparse.Namespace):
    command = [
        'powershell.exe',
        'gcloud', 'ai-platform',
        'jobs', 'submit', 'training',
        args.name,
        '--package-path', 'modeling',
        '--module-name', 'modeling.trainer.model',
        '--staging-bucket', f'gs://{args.bucket}',
        '--python-version', '3.7',
        '--runtime-version', '1.15',
        '--',
        f'--bucket={args.bucket}'
    ]

    result = subprocess.run(command)

    result.check_returncode()


def deploy_predictor(args: argparse.Namespace):
    command = [
        'powershell.exe',
        'gcloud', 'ai-platform',
        ''
    ]
    pass


def main():
    args = parse()
    if args.action == 'train':
        return deploy_trainer(args)
    elif args.action == 'predict':
        return deploy_predictor(args)
    raise ValueError(f'Unknown action "{args.action}"')


if __name__ == '__main__':
    main()
