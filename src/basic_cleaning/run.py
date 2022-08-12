#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info("Fetching input artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_local_path = artifact.file()

    logger.info("Reading dataframe")
    df = pd.read_csv(artifact_local_path)

    # Drop outliers 
    logger.info("Dropping Outliers")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    #filename = "processed_data.csv"
    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    logger.info("Logging artifact")
    run.log_artifact(artifact)

    os.remove(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type= str,
        help= "The input artifact which is the sample.csv",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type= str,
        help= "The output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type= str,
        help= "csv file format",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type= str,
        help= "The output artifact output_description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type= float,
        help= "The minimum price to consider",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type= float,
        help= "The maximum price to consider",
        required=True
    )


    args = parser.parse_args()

    go(args)
