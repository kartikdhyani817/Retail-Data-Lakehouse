from pathlib import Path


PROJECT_NAME = "Retail Data Lakehouse"

folders = [
    "data/raw",
    "data/bronze",
    "data/silver",
    "data/gold",
    "reports",
]


def create_folders() -> None:
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    create_folders()
    print(f"{PROJECT_NAME} setup completed successfully.")