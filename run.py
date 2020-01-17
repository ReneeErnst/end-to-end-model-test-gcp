"""Run the gcloud command for AI Platform Job"""
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(
        prog='run',
        description='Command to run AI Platform job via gcloud'
    )
    parser.add_argument(
        '--bucket',
        required=True,
        help='Specify the storage bucket for staging package and model files'
    )
    parser.add_argument(
        '--name',
        required=True,
        help='Name of the job for AI Platform Jobs'
    )

    args = parser.parse_args()

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


if __name__ == '__main__':
    main()
