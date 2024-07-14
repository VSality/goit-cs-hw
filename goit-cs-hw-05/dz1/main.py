import os
import asyncio
import shutil
import aiofiles
from aiofiles.os import makedirs
from argparse import ArgumentParser
import logging

logging.basicConfig(level=logging.INFO)

async def read_folder(source_folder, output_folder):
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            tasks.append(asyncio.create_task(copy_file(file_path, output_folder)))
    await asyncio.gather(*tasks)

async def copy_file(file_path, output_folder):
    try:
        _, extension = os.path.splitext(file_path)
        extension = extension[1:].lower()  
        if not extension:
            extension = 'no_extension'

        target_folder = os.path.join(output_folder, extension)
        await makedirs(target_folder, exist_ok=True)

        target_path = os.path.join(target_folder, os.path.basename(file_path))
        async with aiofiles.open(file_path, 'rb') as src, aiofiles.open(target_path, 'wb') as dst:
            while True:
                data = await src.read(1024 * 1024)
                if not data:
                    break
                await dst.write(data)

        logging.info(f"Copied {file_path} to {target_path}")
    except Exception as e:
        logging.error(f"Failed to copy {file_path}: {e}")

def main():
    parser = ArgumentParser(description="Sort files based on their extensions")
    parser.add_argument('source_folder', type=str, help="Source folder to read files from")
    parser.add_argument('output_folder', type=str, help="Output folder to save sorted files")
    args = parser.parse_args()

    source_folder = os.path.abspath(args.source_folder)
    output_folder = os.path.abspath(args.output_folder)

    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()
