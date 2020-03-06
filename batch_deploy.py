"""Run the gcloud command for AI Platform Job"""
import argparse
import subprocess
import textwrap


def parse():
    """
    Arguments to be passed in the gcloud commands
    :return: parser for needed arguments
    """
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

    # Required even though this deploy functionality doesn't need arguments
    # passed in
    # noinspection PyUnusedLocal
    local_train_parser = sub_parsers.add_parser('local_train')
    local_train_parser.add_argument(
        '--project',
        required=True,
        help='Name of BigQuery project'
    )
    local_train_parser.add_argument(
        '--dataset_table',
        required=True,
        help='Name of BigQuery dataset and table, in form of dataset.table'
    )

    train_parser = sub_parsers.add_parser('train')
    train_parser.add_argument(
        '--bucket',
        required=True,
        help=textwrap.dedent(
            """
            Specify the storage bucket for staging package and outputting
            model files
            """
        )
    )
    train_parser.add_argument(
        '--name',
        required=True,
        help='Name of the job for AI Platform Jobs'
    )
    train_parser.add_argument(
        '--project',
        required=True,
        help='Name of BigQuery project'
    )
    train_parser.add_argument(
        '--dataset_table',
        required=True,
        help='Name of BigQuery dataset and table, in form of dataset.table'
    )
    # Prediction inputs
    predict_parser = sub_parsers.add_parser('predict')
    predict_parser.add_argument(
        '--version',
        required=True,
        help='Name of model version to create'
    )
    predict_parser.add_argument(
        '--model',
        required=True,
        help='Name of already created model'
    )
    predict_parser.add_argument(
        '--origin',
        required=True,
        help='Path to model directory in cloud storage'
    )
    predict_parser.add_argument(
        '--package-path',
        required=True,
        help=textwrap.dedent(
            """
            Path to package/tarball in GCS - If multiple should be comma
            separated list
            """
        )
    )

    return parser.parse_args()


# noinspection PyUnusedLocal
def deploy_local_train(args: argparse.Namespace):
    """
    Run command to test training job locally
    :param args: args needed to run the command
    :return: output from running the command
    """
    command = [
        'powershell.exe',
        'gcloud', 'ai-platform', 'local', 'train',
        '--package-path', 'modeling',
        '--module-name', 'modeling.trainer.batch_model',
        '--job-dir', 'local-training-output',
        '--',
        '--run_location=local',
        '--bucket=None',
		f'--project={args.project}',
		f'--dataset_table={args.dataset_table}'
    ]
    result = subprocess.run(command)

    return result.check_returncode()


def deploy_trainer(args: argparse.Namespace):
    """
    Run command to run training job in AI Platform
    :param args: args needed to run the command
    :return: output from running the command
    """
    command = [
        'powershell.exe',
        'gcloud', 'ai-platform',
        'jobs', 'submit', 'training',
        args.name,
        '--package-path', 'modeling',
        '--module-name', 'modeling.trainer.batch_model',
        '--staging-bucket', f'gs://{args.bucket}',
        '--python-version', '3.7',
        '--runtime-version', '1.15',
        '--',
        f'--bucket={args.bucket}',
		f'--project={args.project}',
		f'--dataset_table={args.dataset_table}'
    ]

    result = subprocess.run(command)

    return result.check_returncode()


def deploy_predictor(args: argparse.Namespace):
    """
    Run command to create a model version in AI Platform
    :param args: args needed to run the command
    :return: output from running the command
    """
    command = [
        'powershell.exe',
        'gcloud', 'beta', 'ai-platform',
        'versions', 'create', f'{args.version}',
        '--model', f'{args.model}',
        '--runtime-version', '1.15',
        '--python-version', '3.7',
        '--origin', f'{args.origin}',
        '--package-uris', f'{args.package_path}',
        '--prediction-class', 'modeling.predictor.predictor.Predictor',
        '--verbosity=debug'
    ]
    result = subprocess.run(command)

    return result.check_returncode()


def main():
    """
    Run associated function based on action input
    :return: run action
    """
    args = parse()
    if args.action == 'local_train':
        return deploy_local_train(args)
    elif args.action == 'train':
        return deploy_trainer(args)
    elif args.action == 'predict':
        return deploy_predictor(args)
    raise ValueError(f'Unknown action "{args.action}"')


if __name__ == '__main__':
    main()
