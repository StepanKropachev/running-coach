import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

import requests
from cryptography.fernet import Fernet
from dotenv import load_dotenv


@dataclass
class StravaCredentials:
    access_token: str
    refresh_token: str
    expires_at: int


class CredentialStore:
    def __init__(
        self,
        config_dir: Optional[Path] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        load_dotenv()  # Load environment variables from .env

        # Get credentials from parameters or environment
        self.client_id = client_id or os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("STRAVA_CLIENT_SECRET")

        # Validate credentials
        if not self.client_id or not self.client_secret:
            missing = []
            if not self.client_id:
                missing.append("STRAVA_CLIENT_ID")
            if not self.client_secret:
                missing.append("STRAVA_CLIENT_SECRET")
            raise ValueError(
                f"Missing required Strava credentials: {', '.join(missing)}. "
                "Please set them in .env file or pass directly to CredentialStore."
            )
        self.config_dir = config_dir or Path.home() / ".running_coach"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Initialize encryption key
        self.key_path = self.config_dir / ".key"
        self._init_encryption_key()
        self.fernet = Fernet(self._load_key())

    def _init_encryption_key(self) -> None:
        """Initialize encryption key if it doesn't exist"""
        if not self.key_path.exists():
            key = Fernet.generate_key()
            self.key_path.write_bytes(key)
            os.chmod(self.key_path, 0o600)  # Restrict access to user only

    def _load_key(self) -> bytes:
        """Load the encryption key"""
        return self.key_path.read_bytes()

    def save_strava_credentials(self, creds: StravaCredentials) -> None:
        """Save encrypted Strava credentials"""
        data = {
            "access_token": creds.access_token,
            "refresh_token": creds.refresh_token,
            "expires_at": creds.expires_at,
        }
        encrypted = self.fernet.encrypt(json.dumps(data).encode())

        creds_path = self.config_dir / "strava_creds"
        creds_path.write_bytes(encrypted)
        os.chmod(creds_path, 0o600)

    def load_strava_credentials(self) -> Optional[StravaCredentials]:
        """Load and decrypt Strava credentials"""
        creds_path = self.config_dir / "strava_creds"
        if not creds_path.exists():
            return None

        encrypted = creds_path.read_bytes()
        data = json.loads(self.fernet.decrypt(encrypted))

        return StravaCredentials(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=data["expires_at"],
        )

    def needs_refresh(self) -> bool:
        """Check if token needs refresh (buffer of 5 minutes)"""
        creds = self.load_strava_credentials()
        if not creds:
            return True
        return creds.expires_at <= int(time.time()) + 300  # 5 min buffer

    def refresh_token(self) -> Tuple[bool, Optional[str]]:
        """
        Refresh the access token using the refresh token
        Returns: (success, error_message)
        """
        if not self.client_id or not self.client_secret:
            return False, "Client ID and secret not configured"

        creds = self.load_strava_credentials()
        if not creds:
            return False, "No credentials found"

        response = requests.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": creds.refresh_token,
            },
        )

        if response.status_code != 200:
            return False, f"Token refresh failed: {response.text}"

        data = response.json()
        new_creds = StravaCredentials(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=data["expires_at"],
        )

        self.save_strava_credentials(new_creds)
        return True, None

    def get_valid_token(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get a valid access token, refreshing if necessary
        Returns: (token, error_message)
        """
        if self.needs_refresh():
            success, error = self.refresh_token()
            if not success:
                return None, error

        creds = self.load_strava_credentials()
        if not creds:
            return None, "No credentials found"

        return creds.access_token, None
