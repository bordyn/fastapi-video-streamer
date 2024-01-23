import uvicorn
import os

if __name__ == "__main__":

    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=str)
    args = vars(parser.parse_args())

    os.environ["VIDEO_SOURCE"] = args["video"]

    uvicorn.run("api:app",host="0.0.0.0", port=8000, reload=False, workers=1)
